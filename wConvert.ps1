# Download and install cwebp if not already installed from https://storage.googleapis.com/downloads.webmproject.org/releases/webp/index.html
# Ensure cwebp is in your system PATH for this script to work.
# This script assumes cwebp is in system PATH.

$excludeRelativePath = "assets\img\favicons"
$excludeFullPath = $null

if (Test-Path $excludeRelativePath) {
    $excludeFullPath = (Resolve-Path $excludeRelativePath).Path
    Write-Host "Exclusion path found: $excludeFullPath"
} else {
    Write-Host "Exclusion path '$excludeRelativePath' not found. Script will not exclude any files."
}

$files = Get-ChildItem -Path "assets" -Recurse -Include "*.png", "*.jpg" | Where-Object {
    if ($excludeFullPath) {
        $_.Directory.FullName -notlike "$excludeFullPath*"
    } else {
        $true
    }
}

foreach ($file in $files) {
    $output_webp = Join-Path -Path $file.DirectoryName -ChildPath ($file.BaseName + ".webp")
    Write-Host "Processing: $($file.FullName) -> $output_webp"

    cwebp -metadata none -m 6 -q 75 $file.FullName -o $output_webp

    if ($LASTEXITCODE -eq 0) {
        Write-Host "Successfully converted '$($file.Name)'. Deleting original."
        Remove-Item $file.FullName
    } else {
        Write-Host "Failed to convert '$($file.Name)'. Exit code: $LASTEXITCODE. Keeping original."
    }
}
