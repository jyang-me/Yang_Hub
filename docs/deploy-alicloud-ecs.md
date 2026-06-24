# Linux 服务器部署 YangHub

本文档适用于 Ubuntu 服务器，当前线上域名为：

```text
http://jyang.online/
```

服务器当前项目路径约定为：

```text
/var/www/Yang_Hub
```

## 1. 服务器准备

推荐配置：

- Ubuntu 22.04 LTS 或 Ubuntu 24.04 LTS
- 1 核 2G 起步
- 安全组/防火墙开放 `22`、`80`、`443`

登录服务器：

```bash
ssh ubuntu@124.220.61.43
```

安装基础依赖：

```bash
sudo apt update
sudo apt install -y git nginx python3 python3-venv python3-pip nodejs npm
```

Vite 需要较新的 Node.js，建议升级到 Node 20：

```bash
sudo npm install -g n
sudo n 20
hash -r
node -v
npm -v
```

## 2. 拉取项目

```bash
sudo mkdir -p /var/www
sudo chown -R ubuntu:ubuntu /var/www
cd /var/www
git clone https://github.com/jyang-me/Yang_Hub.git Yang_Hub
cd Yang_Hub
```

如果 GitHub 连接不稳定，可以临时使用镜像：

```bash
git clone https://gh.llkk.cc/https://github.com/jyang-me/Yang_Hub.git Yang_Hub
```

## 3. 配置环境变量

创建 `/var/www/Yang_Hub/.env`：

```bash
cat > /var/www/Yang_Hub/.env <<'EOF'
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=replace-this-with-a-long-random-secret
DJANGO_ADMIN_PATH=manage-yanghub-9527/
DJANGO_ALLOWED_HOSTS=jyang.online,www.jyang.online,124.220.61.43,127.0.0.1,localhost
DJANGO_CORS_ALLOWED_ORIGINS=http://jyang.online,http://www.jyang.online,http://124.220.61.43
DJANGO_CSRF_TRUSTED_ORIGINS=http://jyang.online,http://www.jyang.online,http://124.220.61.43
DJANGO_SESSION_COOKIE_SECURE=False
DJANGO_CSRF_COOKIE_SECURE=False
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SECURE_HSTS_SECONDS=0
EOF
```

说明：

- 当前是 HTTP，Cookie Secure 相关配置保持 `False`
- 绑定 HTTPS 后再把 `DJANGO_SESSION_COOKIE_SECURE`、`DJANGO_CSRF_COOKIE_SECURE`、`DJANGO_SECURE_SSL_REDIRECT` 改为 `True`
- 后台入口由 `DJANGO_ADMIN_PATH` 控制

## 4. 部署后端

```bash
cd /var/www/Yang_Hub
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

cd backend
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser
```

## 5. 配置 systemd

```bash
sudo cp /var/www/Yang_Hub/deploy/systemd/yanghub.service /etc/systemd/system/yanghub.service
sudo systemctl daemon-reload
sudo systemctl enable yanghub
sudo systemctl start yanghub
sudo systemctl status yanghub
```

检查后端 API：

```bash
curl http://127.0.0.1:8000/api/
```

## 6. 构建前端

生产环境前端默认请求同域名 `/api`，不需要额外设置 `VITE_API_BASE_URL`。

```bash
cd /var/www/Yang_Hub/frontend
npm install
npm run build
```

构建产物：

```text
/var/www/Yang_Hub/frontend/dist
```

## 7. 配置 Nginx

复制配置：

```bash
sudo cp /var/www/Yang_Hub/deploy/nginx/yanghub.conf /etc/nginx/sites-available/yanghub
sudo ln -sf /etc/nginx/sites-available/yanghub /etc/nginx/sites-enabled/yanghub
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

当前 Nginx 配置要点：

```text
/                       -> Vue 前端
/api/                   -> Django API
/manage-yanghub-9527/   -> Django Admin
/admin/                 -> 404
/media/                 -> 上传文件
/static/                -> Django 静态文件
```

访问：

```text
http://jyang.online/
http://jyang.online/api/
http://jyang.online/manage-yanghub-9527/
```

## 8. 后续更新代码

更新前端：

```bash
cd /var/www/Yang_Hub
git pull

cd frontend
rm -rf dist
npm install
npm run build

sudo systemctl reload nginx
```

更新后端：

```bash
cd /var/www/Yang_Hub
git pull

source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
python manage.py migrate
python manage.py collectstatic --no-input

sudo systemctl restart yanghub
sudo systemctl reload nginx
```

## 9. 后台管理

后台入口：

```text
http://jyang.online/manage-yanghub-9527/
```

`/admin/` 已被 Nginx 禁用。

如果后台能打开但无法保存，优先检查：

```bash
cat /var/www/Yang_Hub/.env
sudo systemctl restart yanghub
sudo nginx -t
sudo systemctl reload nginx
```

当前 HTTP 阶段必须保持：

```text
DJANGO_SESSION_COOKIE_SECURE=False
DJANGO_CSRF_COOKIE_SECURE=False
```

## 10. 数据同步排查

后台更新项目或文章后，先检查 API：

```text
http://jyang.online/api/projects/
http://jyang.online/api/posts/
```

如果 API 是新数据，但前端页面没变：

```bash
cd /var/www/Yang_Hub/frontend
rm -rf dist
npm run build
sudo systemctl reload nginx
```

然后浏览器按 `Ctrl + F5`。

如果图片不显示，检查图片地址是否能访问：

```text
http://jyang.online/media/...
```

## 11. HTTPS

域名解析稳定后，可以申请证书：

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d jyang.online -d www.jyang.online
```

HTTPS 正常后再修改 `.env`：

```text
DJANGO_CORS_ALLOWED_ORIGINS=https://jyang.online,https://www.jyang.online
DJANGO_CSRF_TRUSTED_ORIGINS=https://jyang.online,https://www.jyang.online
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_SECURE_SSL_REDIRECT=True
```

重启：

```bash
sudo systemctl restart yanghub
sudo systemctl reload nginx
```
