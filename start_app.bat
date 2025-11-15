@echo off
chcp 65001 >nul
echo ========================================
echo   Sepsis风险评分计算器
echo ========================================
echo.
echo 正在启动Web应用...
echo.
echo 应用将在浏览器中自动打开
echo 如果没有自动打开，请访问: http://localhost:8501
echo.
echo 按 Ctrl+C 停止应用
echo.
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
pause

