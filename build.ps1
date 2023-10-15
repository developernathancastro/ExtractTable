$exclude = @("venv", "ExtractTable.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "ExtractTable.zip" -Force