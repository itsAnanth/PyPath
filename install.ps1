# PVM Installer for Windows
# Downloads pvm.exe and adds it to user PATH

$url = "https://github.com/itsAnanth/pvm/releases/download/v1.0.0/pvm.exe"
$installDir = "$env:LOCALAPPDATA\.pvm"
$exePath = "$installDir\pvm.exe"

Write-Host "Installing PVM (Python Version Manager)..." -ForegroundColor Cyan

# Create installation directory
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
    Write-Host "Created directory: $installDir" -ForegroundColor Green
}

# Download pvm.exe
Write-Host "Downloading pvm.exe from $url..." -ForegroundColor Yellow
try {
    Invoke-WebRequest -Uri $url -OutFile $exePath -UseBasicParsing
    Write-Host "Downloaded successfully!" -ForegroundColor Green
} catch {
    Write-Host "Failed to download: $_" -ForegroundColor Red
    exit 1
}

# Add to user PATH if not already present
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$installDir*") {
    Write-Host "Adding $installDir to user PATH..." -ForegroundColor Yellow
    [Environment]::SetEnvironmentVariable(
        "Path",
        "$installDir;$userPath",
        "User"
    )
    Write-Host "Added to PATH successfully!" -ForegroundColor Green
    Write-Host "Please restart your terminal for PATH changes to take effect." -ForegroundColor Yellow
} else {
    Write-Host "$installDir is already in PATH" -ForegroundColor Green
}

Write-Host "`nInstallation complete! Run 'pvm' to get started." -ForegroundColor Cyan