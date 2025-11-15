@echo off
chcp 65001 >nul
echo ========================================
echo   Sepsis风险评分计算器 (网络访问版)
echo ========================================
echo.
echo 正在启动Web应用...
echo.
echo 获取本机IP地址...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    set IP=%%a
    set IP=!IP:~1!
    goto :found
)
:found
echo.
echo ========================================
echo   访问地址:
echo ========================================
echo   本机访问: http://localhost:8501
echo   局域网访问: http://%IP%:8501
echo.
echo   其他设备请使用局域网IP地址访问
echo   确保设备在同一网络下
echo.
echo ========================================
echo.
echo 正在启动应用...
echo 按 Ctrl+C 停止应用
echo.
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
pause

