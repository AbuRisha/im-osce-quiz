# Re-apply all peds patches in the correct order.
# patch_peds_gallery.py is idempotent via backup-restore, so the other
# patches (case-39 table, export-answers) must run AFTER it each time.
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONDONTWRITEBYTECODE = "1"

$Repo = "C:\Users\erick\AppData\Local\Temp\opencode\im-osce-quiz"

Write-Host "[1/3] peds gallery patch..."
python "$Repo\patch_peds_gallery.py"

Write-Host "`n[2/3] case 39 comparison table..."
python "$Repo\patch_case39_table.py"

Write-Host "`n[3/3] Export My Answers button..."
python "$Repo\patch_export_answers.py"

Write-Host "`n--- verify ---"
$h = Get-Content "$Repo\index.html" -Raw
foreach ($m in 'data-peds-gallery','data-cmp-table-39','data-export-answers','window.exportAllAnswers','#peds-lb{','.cmp-wrap{') {
    $c = ([regex]::Matches($h, [regex]::Escape($m))).Count
    Write-Host "  $m`: $c"
}
Write-Host "  total: $($h.Length) bytes"
