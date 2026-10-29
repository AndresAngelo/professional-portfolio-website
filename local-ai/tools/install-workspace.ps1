Set-Location -LiteralPath "c:\dev\andres-webapp-professional\personal-website-portfolio"
& npm.cmd install *> "local-ai\tools\npm-install-output.txt"
"exit=$LASTEXITCODE" | Add-Content "local-ai\tools\npm-install-output.txt"
