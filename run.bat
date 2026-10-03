@echo off
cd /d "%~dp0"
if not exist venv\Scripts\activate.bat (
    echo 首次运行：创建虚拟环境并安装 Kivy...
    python -m venv venv
    call venv\Scripts\activate.bat
    python -m pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)
echo 启动应用...
python main.py
pause
