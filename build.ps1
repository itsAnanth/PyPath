Write-Host "Buildiing python-version-manager executable..."
uv run -m PyInstaller --onefile --clean --name pvm main.py
