# MICRONAUT ORCHESTRATOR (SCO/1 projection only)

$Root = Split-Path $MyInvocation.MyCommand.Path
$IO = Join-Path $Root "io"
$Chat = Join-Path $IO "chat.txt"
$Stream = Join-Path $IO "stream.txt"
$State = Join-Path $Root "trace/scxq2.trace"

Write-Host "Micronaut online."

$lastSize = 0

function cm1_verify {
    param(
        [Parameter(Mandatory = $true)][string]$Entry
    )

    if ([string]::IsNullOrWhiteSpace($Entry)) {
        return $false
    }

    return $true
}

function Invoke-KUHUL-TSG {
    param(
        [Parameter(Mandatory = $true)][string]$Input
    )

    return $Input
}

function Invoke-SCXQ2-Infer {
    param(
        [Parameter(Mandatory = $true)][string]$Signal
    )

    return "t=$([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()) ctx=@π mass=0.0`n[projection-only]"
}

while ($true) {
    if (Test-Path $Chat) {
        $size = (Get-Item $Chat).Length
        if ($size -gt $lastSize) {
            $entry = Get-Content $Chat -Raw
            $lastSize = $size

            if (-not (cm1_verify $entry)) {
                Write-Host "CM-1 violation"
                continue
            }

            $signal = Invoke-KUHUL-TSG -Input $entry
            $response = Invoke-SCXQ2-Infer -Signal $signal

            Add-Content $Stream ">> $response"
            Add-Content $State "append: $([DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds())"
        }
    }
    Start-Sleep -Milliseconds 200
}
