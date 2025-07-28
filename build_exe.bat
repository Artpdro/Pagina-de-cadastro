@echo off
REM — Navega até a pasta do projeto
cd /d "%~dp0Pagina-de-cadastro"

REM — Exclui builds anteriores (opcional)
rmdir /s /q build dist __pycache__

REM — Gera o executável
pyinstaller --onefile --windowed ^
  --add-data "logo.png;." ^
  --add-data "view.py;." ^
  --add-data "contadores_novo.db;." ^
  --add-data "contadores.db;." ^
  --add-data "empresas.db;." ^
  --add-data "relacionamentos.db;." ^
  --add-data "repis.db;." ^
  --add-data "pdf_mapping.py;." ^
  main.py

echo.
echo ===== Build concluído! =====
echo Verifique a pasta dist\main.exe
pause
