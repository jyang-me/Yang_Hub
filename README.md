# YangHub

YangHub 是一个前后端分离的个人技术网站，用于展示首页简介、技术博客、项目作品和联系留言。

## 当前访问地址

域名 `jyang.online` 目前处于备案流程中，备案完成前暂时使用服务器公网 IP 访问。

线上访问地址：

```text
前端网站：http://124.220.61.43/
后端 API：http://124.220.61.43/api/
后台入口：http://124.220.61.43/manage-yanghub-9527/
```

备案完成并完成域名解析后，计划使用：

```text
前端网站：http://jyang.online/
后端 API：http://jyang.online/api/
后台入口：http://jyang.online/manage-yanghub-9527/
```

说明：

- `/admin/` 已由 Nginx 返回 404，不作为公开后台入口。
- Django Admin 仍需要管理员账号登录。
- 当前还未启用 HTTPS，后台登录和管理建议尽快在备案完成后配置 HTTPS。

## 技术栈

前端：

- Vue 3 + Composition API
- Vite
- Vue Router
- Pinia
- Axios
- Tailwind CSS
- markdown-it、highlight.js、DOMPurify

后端：

- Django 5
- Django REST Framework
- DRF Token Authentication
- django-cors-headers
- WhiteNoise
- Gunicorn
- SQLite，后续可迁移到 PostgreSQL

部署：

- Ubuntu Linux 服务器
- Nginx 托管前端静态文件，并反向代理后端接口
- systemd 守护 Django Gunicorn 服务

## 架构

```text
Browser
  |
  | http://124.220.61.43/
  v
Nginx
  |-- /                      -> frontend/dist
  |-- /api/                  -> Gunicorn/Django 127.0.0.1:8000/api/
  |-- /manage-yanghub-9527/  -> Gunicorn/Django hidden admin path
  |-- /media/                -> backend/media/
  |-- /static/               -> backend/staticfiles/
  '-- /admin/                -> 404
```

## 目录结构

```text
Yang_Hub
├── backend/
│   ├── accounts/
│   ├── blog/
│   ├── contact/
│   ├── portfolio/
│   ├── backend/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── router/
│   │   ├── stores/
│   │   └── views/
│   ├── package.json
│   └── vite.config.js
├── deploy/
│   ├── nginx/yanghub.conf
│   └── systemd/yanghub.service
├── docs/
│   └── deploy-alicloud-ecs.md
├── .env.example
└── README.md
```

## 功能模块

- 首页：Hero、技能矩阵、统计数据、最近动态
- 博客：列表、详情、Markdown 渲染、代码高亮
- 项目：列表、详情、封面图、技术栈、GitHub 链接
- 留言板：公开提交留言，管理员管理
- 后台：Django Admin 管理文章、项目、分类、标签、留言

## API

```text
GET    /api/posts/
GET    /api/posts/<id-or-slug>/
GET    /api/projects/
GET    /api/projects/<id-or-slug>/
POST   /api/messages/
GET    /api/stats/
POST   /api/auth/token/
GET    /api/auth/me/
```

生产环境前端默认请求同域名 `/api`，图片和上传文件默认走同域名 `/media/...`。

## 本地运行

后端：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend\requirements.txt
cd backend
python manage.py migrate
python manage.py runserver
```

前端：

```powershell
cd frontend
npm install
npm run dev
```

本地访问：

```text
前端：http://127.0.0.1:5173/
后端：http://127.0.0.1:8000/api/
后台：http://127.0.0.1:8000/admin/
```

## 线上部署

服务器项目路径：

```text
/var/www/Yang_Hub
```

后端服务：

```bash
sudo systemctl status yanghub
sudo systemctl restart yanghub
sudo journalctl -u yanghub -f
```

Nginx：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

前端更新：

```bash
cd /var/www/Yang_Hub
git pull
cd frontend
rm -rf dist
npm install
npm run build
sudo systemctl reload nginx
```

后端更新：

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

## 生产环境变量

参考 `.env.example`：

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=change-me-to-a-long-random-secret
DJANGO_ADMIN_PATH=manage-yanghub-9527/
DJANGO_ALLOWED_HOSTS=jyang.online,www.jyang.online,124.220.61.43,127.0.0.1,localhost
DJANGO_CORS_ALLOWED_ORIGINS=http://jyang.online,http://www.jyang.online,http://124.220.61.43
DJANGO_CSRF_TRUSTED_ORIGINS=http://jyang.online,http://www.jyang.online,http://124.220.61.43
DJANGO_SESSION_COOKIE_SECURE=False
DJANGO_CSRF_COOKIE_SECURE=False
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SECURE_HSTS_SECONDS=0
```

当前仍是 HTTP 阶段，所以 `DJANGO_SESSION_COOKIE_SECURE` 和 `DJANGO_CSRF_COOKIE_SECURE` 保持 `False`。配置 HTTPS 后再改为 `True`。

## 数据同步说明

后台新增或修改文章/项目后：

1. 后端数据库立即更新。
2. 前端页面刷新后重新请求 `/api/...`。
3. 项目页可点击“刷新”按钮重新拉取数据。

如果前端没有同步，先检查接口：

```text
http://124.220.61.43/api/projects/
http://124.220.61.43/api/posts/
```

如果 API 已经是新数据，但页面没变：

- 浏览器按 `Ctrl + F5`。
- 确认服务器已经重新构建前端。
- 确认前端不是旧 JS 缓存。

如果图片不显示，检查：

```text
http://124.220.61.43/media/...
```

并确认 Nginx 有：

```nginx
location /media/ {
    alias /var/www/Yang_Hub/backend/media/;
}
```

## HTTPS 计划

备案完成、域名解析稳定后：

1. 使用 Certbot 为 `jyang.online` 和 `www.jyang.online` 配置 HTTPS。
2. 将 `.env` 中的来源从 `http` 改为 `https`。
3. 将 Cookie Secure 配置改为 `True`。

示例：

```text
DJANGO_CORS_ALLOWED_ORIGINS=https://jyang.online,https://www.jyang.online
DJANGO_CSRF_TRUSTED_ORIGINS=https://jyang.online,https://www.jyang.online
DJANGO_SESSION_COOKIE_SECURE=True
DJANGO_CSRF_COOKIE_SECURE=True
DJANGO_SECURE_SSL_REDIRECT=True
```

## 常用测试

后端：

```powershell
cd backend
..\.venv\Scripts\python.exe manage.py check
```

前端：

```powershell
cd frontend
npm run build
```
