Write-Host "Building python-version-manager executable..."

# Set production mode (INFO logging)
$env:PVM_DEV = "0"

uv run -m PyInstaller --onefile --clean --exclude-module tests --name pvm main.py
