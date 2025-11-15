# PowerShell script to fix all URL routing issues in templates
# Campus Resource Hub - Routing Fix Script

Write-Host "Fixing URL routing issues in templates..." -ForegroundColor Cyan
Write-Host ""

$fixes = 0
$rootPath = "src\views"

# Fix 1: booking.detail with id= → booking_id=
Write-Host "Fixing booking.detail parameter..." -ForegroundColor Yellow
$files = Get-ChildItem -Path $rootPath -Filter *.html -Recurse
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $newContent = $content -replace "url_for\('booking\.detail',\s*id=booking\.id\)", "url_for('booking.detail', booking_id=booking.booking_id)"
    $newContent = $newContent -replace "url_for\('booking\.detail',\s*booking_id=booking\.id\)", "url_for('booking.detail', booking_id=booking.booking_id)"
    if ($content -ne $newContent) {
        Set-Content -Path $file.FullName -Value $newContent -NoNewline
        Write-Host "  ✓ Fixed $($file.Name)" -ForegroundColor Green
        $fixes++
    }
}

# Fix 2: booking.approve with id= → booking_id=
Write-Host "Fixing booking.approve parameter..." -ForegroundColor Yellow
$files = Get-ChildItem -Path $rootPath -Filter *.html -Recurse
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $newContent = $content -replace "url_for\('booking\.approve',\s*id=booking\.id\)", "url_for('booking.approve', booking_id=booking.booking_id)"
    if ($content -ne $newContent) {
        Set-Content -Path $file.FullName -Value $newContent -NoNewline
        Write-Host "  ✓ Fixed $($file.Name)" -ForegroundColor Green
        $fixes++
    }
}

# Fix 3: booking.reject with id= → booking_id=
Write-Host "Fixing booking.reject parameter..." -ForegroundColor Yellow
$files = Get-ChildItem -Path $rootPath -Filter *.html -Recurse
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $newContent = $content -replace "url_for\('booking\.reject',\s*id=booking\.id\)", "url_for('booking.reject', booking_id=booking.booking_id)"
    if ($content -ne $newContent) {
        Set-Content -Path $file.FullName -Value $newContent -NoNewline
        Write-Host "  ✓ Fixed $($file.Name)" -ForegroundColor Green
        $fixes++
    }
}

# Fix 4: booking.cancel with id= → booking_id=
Write-Host "Fixing booking.cancel parameter..." -ForegroundColor Yellow
$files = Get-ChildItem -Path $rootPath -Filter *.html -Recurse
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $newContent = $content -replace "url_for\('booking\.cancel',\s*id=booking\.id\)", "url_for('booking.cancel', booking_id=booking.booking_id)"
    if ($content -ne $newContent) {
        Set-Content -Path $file.FullName -Value $newContent -NoNewline
        Write-Host "  ✓ Fixed $($file.Name)" -ForegroundColor Green
        $fixes++
    }
}

# Fix 5: message.thread with message_id= → thread_id=
Write-Host "Fixing message.thread parameter..." -ForegroundColor Yellow
$files = Get-ChildItem -Path $rootPath -Filter *.html -Recurse
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $newContent = $content -replace "url_for\('message\.thread',\s*message_id=message\.id\)", "url_for('message.thread', thread_id=message.thread_id)"
    if ($content -ne $newContent) {
        Set-Content -Path $file.FullName -Value $newContent -NoNewline
        Write-Host "  ✓ Fixed $($file.Name)" -ForegroundColor Green
        $fixes++
    }
}

# Fix 6: message.reply with message_id= → thread_id=
Write-Host "Fixing message.reply parameter..." -ForegroundColor Yellow
$files = Get-ChildItem -Path $rootPath -Filter *.html -Recurse
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    $newContent = $content -replace "url_for\('message\.reply',\s*message_id=thread\[0\]\.id\)", "url_for('message.reply', thread_id=thread_id)"
    if ($content -ne $newContent) {
        Set-Content -Path $file.FullName -Value $newContent -NoNewline
        Write-Host "  ✓ Fixed $($file.Name)" -ForegroundColor Green
        $fixes++
    }
}

Write-Host ""
Write-Host "✓ Completed! Fixed $fixes template files." -ForegroundColor Green
Write-Host ""
Write-Host "Next: Run 'python run.py' to test the application." -ForegroundColor Cyan
