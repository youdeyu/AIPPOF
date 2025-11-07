# 🚀 AIPPOF 前后端部署指南

## 问题诊断

### ❌ 原问题
- 从本地电脑访问服务器网址 `aippof-0w0.lthero.com`
- 前端正常显示，但数据加载失败
- 原因：前端JavaScript在浏览器执行时，`localhost:8000` 指向访问者的本地电脑，而不是服务器！

### ✅ 解决方案
使用环境变量区分开发环境和生产环境的后端地址。

---

## 📁 文件配置

### 1. `.env.development`（本地开发）
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 2. `.env.production`（服务器部署）
```env
# 使用服务器域名+端口
VITE_API_BASE_URL=http://aippof-0w0.lthero.com:8000
```

### 3. `src/config.ts`（已修改）
```typescript
const getApiBaseUrl = () => {
  // 1. 优先使用环境变量（构建时注入）
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }
  
  // 2. 开发模式：自动检测
  const currentHost = window.location.hostname
  if (currentHost !== 'localhost' && currentHost !== '127.0.0.1') {
    return `http://${currentHost}:8000`
  }
  
  // 3. 默认本地
  return 'http://localhost:8000'
}
```

---

## 🛠️ 部署步骤

### 本地开发（使用本地后端）

1. **启动后端**
```bash
cd backend
python main.py
# 后端运行在 http://localhost:8000
```

2. **启动前端**
```bash
npm run dev
# 前端运行在 http://localhost:5173
# 自动读取 .env.development，连接本地后端
```

---

### 服务器部署（使用服务器后端）

#### 方案A：前后端分离部署

1. **服务器启动后端**
```bash
cd backend
python main.py
# 后端运行在 http://aippof-0w0.lthero.com:8000
```

2. **本地构建前端**
```bash
npm run build
# 自动读取 .env.production
# 生成 dist/ 目录
```

3. **上传 dist/ 到服务器**
```bash
# 使用 FTP、SCP 或 Git 上传
scp -r dist/* user@server:/var/www/aippof/
```

4. **服务器配置 Nginx**
```nginx
server {
    listen 80;
    server_name aippof-0w0.lthero.com;
    
    # 前端静态文件
    location / {
        root /var/www/aippof;
        try_files $uri $uri/ /index.html;
    }
    
    # 后端API代理（可选，推荐）
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 方案B：服务器直接构建

1. **上传源代码到服务器**
```bash
git clone https://github.com/youdeyu/AIPPOF.git
cd AIPPOF/08_AIPPOF网页应用
```

2. **服务器构建**
```bash
npm install
npm run build
# 生成 dist/
```

3. **配置 Nginx**（同方案A）

---

## ⚙️ 高级配置：使用 Nginx 反向代理（推荐）

### 优点
- 前后端统一域名，避免跨域问题
- HTTPS 加密
- 隐藏后端端口

### Nginx 配置
```nginx
server {
    listen 443 ssl;
    server_name aippof-0w0.lthero.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    # 前端
    location / {
        root /var/www/aippof;
        try_files $uri $uri/ /index.html;
    }
    
    # 后端API（反向代理）
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 修改 `.env.production`
```env
# 使用反向代理后，前后端统一域名
VITE_API_BASE_URL=https://aippof-0w0.lthero.com/api
```

---

## 🔍 调试技巧

### 1. 检查当前API地址
打开浏览器控制台（F12），查看：
```
🔧 API Base URL: http://aippof-0w0.lthero.com:8000
🌍 Environment: production
```

### 2. 测试后端连接
```bash
# 在浏览器或命令行测试
curl http://aippof-0w0.lthero.com:8000/api/test
```

### 3. 检查跨域问题
如果出现 CORS 错误，在后端 `main.py` 中添加：
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境改为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 三种部署模式对比

| 模式 | 前端地址 | 后端地址 | 适用场景 |
|------|---------|---------|---------|
| **本地开发** | `localhost:5173` | `localhost:8000` | 开发调试 |
| **服务器直连** | `aippof-0w0.lthero.com` | `aippof-0w0.lthero.com:8000` | 快速部署 |
| **Nginx代理** | `aippof-0w0.lthero.com` | `aippof-0w0.lthero.com/api` | 生产环境（推荐） |

---

## ✅ 检查清单

- [ ] 修改 `.env.production` 为服务器地址
- [ ] 构建前端：`npm run build`
- [ ] 上传 `dist/` 到服务器
- [ ] 启动后端：`python main.py`
- [ ] 配置 Nginx（可选）
- [ ] 测试访问：打开 `aippof-0w0.lthero.com`
- [ ] 检查控制台：确认 API 地址正确
- [ ] 测试功能：PathA 和 PathB 数据加载

---

## 🆘 常见问题

### Q1: 本地能访问，服务器不能？
A: 检查服务器防火墙是否开放 8000 端口
```bash
sudo ufw allow 8000
```

### Q2: 数据加载失败？
A: 
1. 打开浏览器控制台，查看 API 请求地址
2. 确认后端服务已启动
3. 检查跨域配置

### Q3: 构建后API地址还是 localhost？
A: 
1. 确认 `.env.production` 文件存在
2. 重新构建：`npm run build`
3. 检查 `dist/assets/*.js` 文件中的 API 地址

---

**最后更新：** 2024-11-07
**维护者：** AIPPOF Team
