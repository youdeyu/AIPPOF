# AIPPOF 一键启动脚本
# 拯救10000只小猫 🐱🐱🐱

Write-Host "🚀 AIPPOF 服务启动中..." -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray

# 设置项目根目录
$ProjectRoot = $PSScriptRoot
Set-Location $ProjectRoot

# 步骤1：检查Node.js和Python
Write-Host "`n📋 步骤1: 检查环境..." -ForegroundColor Yellow
$env:Path = "C:\Program Files\nodejs;" + $env:Path

try {
    $nodeVersion = & node --version 2>&1
    $npmVersion = & npm --version 2>&1
    Write-Host "  ✅ Node.js: $nodeVersion" -ForegroundColor Green
    Write-Host "  ✅ npm: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Node.js未找到！请安装Node.js" -ForegroundColor Red
    exit 1
}

try {
    $pythonVersion = & python --version 2>&1
    Write-Host "  ✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Python未找到！请安装Python" -ForegroundColor Red
    exit 1
}

# 步骤2：启动后端服务器
Write-Host "`n📋 步骤2: 启动后端Flask服务器..." -ForegroundColor Yellow
$backendPath = Join-Path $ProjectRoot "backend"

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd '$backendPath' ; Write-Host '🔧 后端服务器启动中...' -ForegroundColor Cyan ; python main.py"
) -WindowStyle Normal

Write-Host "  ✅ 后端服务器启动中 (http://localhost:8000)" -ForegroundColor Green
Start-Sleep -Seconds 3

# 步骤3：启动前端服务器
Write-Host "`n📋 步骤3: 启动前端Vite服务器..." -ForegroundColor Yellow

Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "`$env:Path = 'C:\Program Files\nodejs;' + `$env:Path ; cd '$ProjectRoot' ; Write-Host '🎨 前端服务器启动中...' -ForegroundColor Cyan ; npm run dev"
) -WindowStyle Normal

Write-Host "  ✅ 前端服务器启动中 (http://localhost:5173)" -ForegroundColor Green
Start-Sleep -Seconds 5

# 步骤4：测试服务器连接
Write-Host "`n📋 步骤4: 测试服务器连接..." -ForegroundColor Yellow

try {
    $backendTest = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 5
    Write-Host "  ✅ 后端API正常: $($backendTest.Content)" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️ 后端API未就绪，可能需要更多时间..." -ForegroundColor Yellow
}

try {
    $frontendTest = Invoke-WebRequest -Uri "http://localhost:5173" -Method GET -TimeoutSec 5
    Write-Host "  ✅ 前端页面正常" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️ 前端页面未就绪，可能需要更多时间..." -ForegroundColor Yellow
}

# 步骤5：打开浏览器
Write-Host "`n📋 步骤5: 打开浏览器..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
Start-Process "http://localhost:5173"
Write-Host "  ✅ 浏览器已打开" -ForegroundColor Green

# 完成
Write-Host "`n" + "=" * 60 -ForegroundColor Gray
Write-Host "🎉 所有服务已启动！" -ForegroundColor Green
Write-Host ""
Write-Host "📍 访问地址：" -ForegroundColor Cyan
Write-Host "   前端应用: http://localhost:5173" -ForegroundColor White
Write-Host "   后端API:  http://localhost:8000" -ForegroundColor White
Write-Host "   API文档:  http://localhost:8000/" -ForegroundColor White
Write-Host ""
Write-Host "💡 提示：" -ForegroundColor Yellow
Write-Host "   - 前端和后端在独立窗口运行" -ForegroundColor Gray
Write-Host "   - 关闭时请在各自窗口按 Ctrl+C" -ForegroundColor Gray
Write-Host "   - 代码修改会自动热重载" -ForegroundColor Gray
Write-Host ""
Write-Host "🐱 已成功拯救10000只小猫！" -ForegroundColor Magenta
Write-Host "=" * 60 -ForegroundColor Gray

# 保持窗口打开
Write-Host "`n按任意键退出主控制台..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
