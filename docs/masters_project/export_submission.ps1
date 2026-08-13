param(
    [Parameter(Mandatory = $true)]
    [string]$DocxPath,

    [Parameter(Mandatory = $true)]
    [string]$PdfPath
)

$ErrorActionPreference = 'Stop'
$word = $null
$document = $null

try {
    $docx = [System.IO.Path]::GetFullPath($DocxPath)
    $pdf = [System.IO.Path]::GetFullPath($PdfPath)
    [System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($pdf)) | Out-Null

    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0

    $document = $word.Documents.Open($docx, $false, $false)

    foreach ($field in $document.Fields) {
        [void]$field.Update()
    }
    foreach ($toc in $document.TablesOfContents) {
        $toc.Update()
    }
    foreach ($tableOfFigures in $document.TablesOfFigures) {
        $tableOfFigures.Update()
    }

    $document.Repaginate()
    $document.Save()
    $document.ExportAsFixedFormat($pdf, 17)
}
finally {
    if ($null -ne $document) {
        try { $document.Close(0) } catch { }
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($document)
    }
    if ($null -ne $word) {
        try { $word.Quit() } catch { }
        [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($word)
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
