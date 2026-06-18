# YangHub

YangHub 是一个前后端分离的个人网站项目，用于展示个人简介、技术博客、项目作品和联系留言。项目以前端 Vue 3 + Vite 为交互入口，后端使用 Django REST Framework 提供 REST API，SQLite 作为本地开发数据库。

## 技术栈

**前端**

- Vue 3：使用 Composition API 编写页面组件
- Vite：前端构建与开发服务器
- Vue Router：页面路由管理
- Pinia：登录状态与 Token 状态管理
- Axios：统一封装后端 API 请求
- Tailwind CSS：响应式布局与样式系统
- markdown-it、highlight.js、DOMPurify：Markdown 渲染、代码高亮与 HTML 安全处理

**后端**

- Django 5：后端工程与管理后台
- Django REST Framework：REST API、Serializer、ViewSet
- DRF Token Authentication：管理员登录与接口鉴权
- django-cors-headers：解决前后端不同端口的跨域请求
- Pillow：图片上传字段支持
- SQLite：本地开发数据库

## 项目架构

```text
YangHub
├── backend/                 # Django + DRF 后端
│   ├── accounts/            # 自定义用户模型与当前用户接口
│   ├── blog/                # 分类、标签、博客文章
│   ├── portfolio/           # 项目作品展示
│   ├── contact/             # 联系留言
│   ├── backend/             # Django 项目配置、URL、认证配置
│   ├── media/               # 本地上传图片目录
│   ├── db.sqlite3           # SQLite 数据库
│   └── manage.py
├── frontend/                # Vue 3 + Vite 前端
│   ├── src/
│   │   ├── api/             # Axios 请求实例
│   │   ├── router/          # Vue Router 路由配置
│   │   ├── stores/          # Pinia 状态管理
│   │   ├── views/           # 页面组件
│   │   └── style.css        # Tailwind 与全局样式
│   ├── public/
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 功能模块

**首页**

- 科技风格 Hero 首屏
- 打字机身份标签
- 技能矩阵
- 后端统计数据概览
- 最近博客和项目动态

**技术博客**

- 博客列表与博客详情
- 文章支持分类、标签、封面图、摘要、发布时间
- Markdown 原文存储在后端，前端负责渲染和代码高亮

**项目作品**

- 项目列表卡片流
- 项目详情页
- 支持项目封面、技术栈、GitHub 链接、演示链接

**留言板**

- 访客可以提交留言
- 管理员可以查看和删除留言

**后台管理**

- 使用 Django Admin 管理用户、文章、标签、分类、项目和留言
- 后台语言已配置为中文

## 后端设计

后端按业务域拆分为多个 Django app：

- `accounts.User`：继承 `AbstractUser`，扩展头像、个人简介、GitHub、LinkedIn、个人网站字段
- `blog.Category`：博客分类
- `blog.Tag`：博客标签
- `blog.Post`：博客文章，支持 Markdown 内容、状态、精选、封面图和发布时间
- `portfolio.Project`：项目作品，支持排序、精选、封面图、演示地址和源码地址
- `contact.Message`：联系留言，记录姓名、邮箱、主题、内容和是否已读

API 使用 DRF Router 统一注册：

```text
/api/categories/
/api/tags/
/api/posts/
/api/projects/
/api/messages/
/api/stats/
/api/auth/token/
/api/auth/me/
```

## 权限与认证

项目当前使用 DRF Token Authentication，并兼容前端常见的 Bearer Token 请求头格式。

前端登录后会把 Token 存入 Pinia 和 `localStorage`，Axios 请求拦截器会自动添加：

```http
Authorization: Bearer <token>
```

权限策略：

- 博客文章、分类、标签、项目：所有人可读，管理员可新增、修改、删除
- 留言：所有人可提交，只有管理员可查看、修改、删除
- 统计接口：公开读取
- 当前用户接口：需要登录

## 前端路由

```text
/                 首页
/blog             博客列表
/blog/:id         博客详情
/projects         项目列表
/projects/:id     项目详情
/messages         留言板
/login            管理员登录
```

前端通过 `src/api/request.js` 统一请求后端 API，默认后端地址为：

```text
http://127.0.0.1:8000/api
```

可通过环境变量覆盖：

```text
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

## 本地运行

### 1. 启动后端

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r backend\requirements.txt

cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

后端地址：

```text
http://127.0.0.1:8000/
```

Django Admin：

```text
http://127.0.0.1:8000/admin/
```

API 根地址：

```text
http://127.0.0.1:8000/api/
```

### 2. 启动前端

```powershell
cd frontend
npm install
npm run dev
```

前端地址：

```text
http://127.0.0.1:5173/
```

### 3. 构建前端

```powershell
cd frontend
npm run build
```

构建产物会输出到：

```text
frontend/dist/
```

## 跨域配置

后端通过 `django-cors-headers` 允许本地前端端口访问：

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

线上部署时需要把前端正式域名加入环境变量：

```text
DJANGO_CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.com
```

## 数据与媒体文件

- 本地数据库：`backend/db.sqlite3`
- 本地上传目录：`backend/media/`
- 博客和项目封面图通过 Django media 文件服务在开发环境访问

## 部署方案

推荐采用前后端分离部署：

- 前端：部署到 Vercel、Netlify、Cloudflare Pages 或静态服务器
- 后端：部署到 Render、Railway、Fly.io、云服务器或其他 Python Web 服务平台
- 数据库：生产环境建议使用 PostgreSQL，不建议长期依赖 SQLite
- 媒体文件：生产环境建议使用对象存储，当前本地 `media/` 更适合开发环境

### 后端部署

后端入口目录是：

```text
backend/
```

构建命令：

```bash
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

如果平台支持脚本，也可以直接使用：

```bash
./build.sh
```

启动命令：

```bash
gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

如果平台从仓库根目录启动，可以使用根目录的 `Procfile`：

```text
web: cd backend && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT
```

后端生产环境变量示例见根目录 `.env.example`：

```text
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=change-me-to-a-long-random-secret
DJANGO_ALLOWED_HOSTS=your-backend-domain.com
DJANGO_CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.com
DJANGO_SECURE_SSL_REDIRECT=False
DJANGO_SECURE_HSTS_SECONDS=0
DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DBNAME
```

### 前端部署

前端入口目录是：

```text
frontend/
```

构建命令：

```bash
npm install
npm run build
```

构建输出目录：

```text
frontend/dist/
```

前端生产环境变量示例见 `frontend/.env.example`：

```text
VITE_API_BASE_URL=https://your-backend-domain.com/api
```

### Cloudflare Pages 部署前端

Cloudflare Pages 适合部署本项目的 Vue 前端。

在 Cloudflare Pages 中选择 GitHub 仓库后，配置如下：

```text
Framework preset: Vite
Root directory: frontend
Build command: npm run build
Build output directory: dist
Node.js version: 20 或更高
```

前端环境变量：

```text
VITE_API_BASE_URL=https://your-backend-domain.com/api
```

项目已在 `frontend/public/_redirects` 中配置：

```text
/* /index.html 200
```

这用于支持 Vue Router 的 history 模式，避免刷新详情页时出现 404。

注意：Cloudflare Pages 只能部署前端静态资源，不能直接运行 Django/DRF 后端。后端需要部署到 Render、Railway、Fly.io、VPS 等支持 Python 的平台，或者用 Cloudflare Tunnel 将服务器上的 Django 服务暴露出来。

### 部署顺序

1. 先部署后端，拿到后端正式域名
2. 在后端环境变量中配置 `DJANGO_ALLOWED_HOSTS`
3. 部署前端，并把 `VITE_API_BASE_URL` 指向后端 `/api`
4. 拿到前端正式域名后，回到后端配置 `DJANGO_CORS_ALLOWED_ORIGINS`
5. 在后端执行迁移并创建管理员账号
6. 进入 Django Admin 添加博客、项目和其他内容

生产环境注意事项：

- 将 SQLite 切换为 PostgreSQL 或 MySQL
- 使用对象存储管理上传文件
- 关闭 `DEBUG`
- 使用环境变量管理 `SECRET_KEY`、数据库连接和允许访问的域名
- 前端构建后交给 Nginx、静态站点服务或云平台托管

## 开发检查

后端测试：

```powershell
cd backend
..\.venv\Scripts\python.exe manage.py test
```

前端构建检查：

```powershell
cd frontend
npm run build
```

## 项目定位

YangHub 不是单纯的静态作品集，而是一个完整的个人技术内容平台。它把个人主页、博客系统、项目展示、留言互动和后台管理连接在一起，适合作为个人品牌网站、技术博客和项目作品集的长期维护基础。
