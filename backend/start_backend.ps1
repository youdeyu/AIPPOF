# AIPPOF Backend Startup Script
# 保持后端服务运行

$BackendPath = "C:\Users\10046\Desktop\python代码测试\code1\final-new\08_AIPPOF网页应用\backend"
$PythonExe = "D:\Anaconda\python.exe"
$MainScript = "main.py"

Write-Host "正在启动AIPPOF后端服务..." -ForegroundColor Cyan
Write-Host "工作目录: $BackendPath" -ForegroundColor Gray
Write-Host "Python: $PythonExe" -ForegroundColor Gray
Write-Host ""

# 切换到backend目录
Set-Location $BackendPath

# 启动Flask（禁用自动重启）
$env:FLASK_DEBUG = "False"
& $PythonExe $MainScript

# 保持窗口打开
Read-Host "按Enter键关闭..."
