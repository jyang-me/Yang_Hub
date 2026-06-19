# 阿里云 ECS 部署 YangHub

本文档适用于一台 Linux 服务器同时部署前端和后端：

- Nginx：对外提供网站、静态文件和反向代理
- Vue 3/Vite：构建为静态文件，由 Nginx 托管
- Django/DRF：由 Gunicorn 运行在 `127.0.0.1:8000`
- SQLite：可用于轻量个人站点；长期生产建议迁移 PostgreSQL

## 1. 购买服务器建议

阿里云 ECS 推荐选择：

- 系统：Ubuntu 22.04 LTS 或 Ubuntu 24.04 LTS
- 规格：个人网站可从 1 核 2G 起步
- 带宽：1Mbps 到 3Mbps 起步，后续按访问量升级
- 安全组：放行 `22`、`80`、`443`

如果暂时没有域名，可以先用公网 IP 访问。后续绑定域名后再配置 HTTPS。

## 2. 安装基础环境

登录服务器：

```bash
ssh root@你的服务器公网IP
```

安装依赖：

```bash
apt update
apt install -y git nginx python3 python3-venv python3-pip nodejs npm
```

建议安装 Node.js 20：

```bash
npm install -g n
n 20
hash -r
node -v
npm -v
```

## 3. 拉取项目

```bash
mkdir -p /var/www
cd /var/www
git clone https://github.com/jyang-me/Yang_Hub.git yanghub
cd yanghub
```

## 4. 配置后端环境变量

在 `/var/www/yanghub/.env` 创建生产配置：

```bash
nano /var/www/yanghub/.env
```

示例：

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=换成一个很长的随机字符串
DJANGO_ALLOWED_HOSTS=你的域名,你的服务器公网IP
DJANGO_CORS_ALLOWED_ORIGINS=http://你的域名,http://你的服务器公网IP
DJANGO_CSRF_TRUSTED_ORIGINS=http://你的域名,http://你的服务器公网IP
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SECURE_HSTS_SECONDS=0
```

如果暂时只有公网 IP，就把域名部分换成公网 IP。

## 5. 部署 Django 后端

```bash
cd /var/www/yanghub
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

cd backend
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser
```

配置权限：

```bash
chown -R www-data:www-data /var/www/yanghub
```

## 6. 配置 systemd 后端服务

复制服务文件：

```bash
cp /var/www/yanghub/deploy/systemd/yanghub.service /etc/systemd/system/yanghub.service
systemctl daemon-reload
systemctl enable yanghub
systemctl start yanghub
systemctl status yanghub
```

查看日志：

```bash
journalctl -u yanghub -f
```

## 7. 构建前端

如果前后端使用同一个域名，前端不需要额外设置 `VITE_API_BASE_URL`，生产环境会默认请求同域名 `/api`。

```bash
cd /var/www/yanghub/frontend
npm install
npm run build
```

## 8. 配置 Nginx

复制 Nginx 配置：

```bash
cp /var/www/yanghub/deploy/nginx/yanghub.conf /etc/nginx/sites-available/yanghub
```

编辑域名或公网 IP：

```bash
nano /etc/nginx/sites-available/yanghub
```

把：

```text
server_name your-domain.com www.your-domain.com;
```

改成：

```text
server_name 你的域名 你的服务器公网IP;
```

启用站点：

```bash
ln -s /etc/nginx/sites-available/yanghub /etc/nginx/sites-enabled/yanghub
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx
```

现在可以访问：

```text
http://你的服务器公网IP/
http://你的服务器公网IP/admin/
http://你的服务器公网IP/api/
```

## 9. 配置 HTTPS

域名解析到 ECS 公网 IP 后，可以使用 Certbot：

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d 你的域名
```

HTTPS 配好后，把 `.env` 中的来源改成 `https`：

```text
DJANGO_ALLOWED_HOSTS=你的域名
DJANGO_CORS_ALLOWED_ORIGINS=https://你的域名
DJANGO_CSRF_TRUSTED_ORIGINS=https://你的域名
DJANGO_SECURE_SSL_REDIRECT=True
```

然后重启后端：

```bash
systemctl restart yanghub
systemctl reload nginx
```

## 10. 更新代码

后续更新网站：

```bash
cd /var/www/yanghub
git pull

source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend
python manage.py migrate
python manage.py collectstatic --no-input

cd ../frontend
npm install
npm run build

systemctl restart yanghub
systemctl reload nginx
```

## 常见问题

### 后台打不开

检查 Django 服务：

```bash
systemctl status yanghub
journalctl -u yanghub -n 100
```

### 首页能打开，但接口报错

检查 Nginx 反向代理：

```bash
nginx -t
curl http://127.0.0.1:8000/api/
curl http://127.0.0.1/api/
```

### 上传图片无法显示

确认 Nginx 配置中存在：

```nginx
location /media/ {
    alias /var/www/yanghub/backend/media/;
}
```

### 服务器安全组

阿里云 ECS 安全组需要放行：

- `22`：SSH 登录
- `80`：HTTP
- `443`：HTTPS
