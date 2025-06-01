param (
    [Parameter(Mandatory = $true)]
    [string]$BuildNumber
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

Write-Host "Patching with build number: $BuildNumber"

$PATCHER = "flash-patcher"
$SWF_FILE_PATH = "."

# Create the patch file dynamically
$patchFile = "noncheat\add_build_number.patch"
Remove-Item $patchFile -ErrorAction SilentlyContinue

@"
# Add the build number to the hack. Required for speedrun timer and input display.
add frame_1/DoAction.as end
begin-patch
_root.build_number = $BuildNumber;
end-patch
"@ | Out-File -FilePath $patchFile -Encoding UTF8

# Patch all hacks
& $PATCHER --inputswf "$SWF_FILE_PATH\SMF_Base_Hack.swf" --folder . --stagefile "stagefiles/fullgame.stage" --outputswf "SMF-Fullgame-Build-$BuildNumber.swf"
& $PATCHER --inputswf "$SWF_FILE_PATH\SMF_Base_Hack.swf" --folder . --stagefile "stagefiles/level.stage" --outputswf "SMF-IL-Build-$BuildNumber.swf"
& $PATCHER --inputswf "$SWF_FILE_PATH\SMF_Base_Hack.swf" --folder . --stagefile "stagefiles/cheat.stage" --outputswf "SMF-Cheat-Build-$BuildNumber.swf"

# Zip the results
$zipName = "SMF-Hacks-Build-$BuildNumber.zip"
$zipFiles = @(
    "SMF-Fullgame-Build-$BuildNumber.swf",
    "SMF-IL-Build-$BuildNumber.swf",
    "SMF-Cheat-Build-$BuildNumber.swf",
    "patch-notes.txt"
)

if (Test-Path $zipName) {
    Remove-Item $zipName -Force
}

Compress-Archive -Path $zipFiles -DestinationPath $zipName

# Move ZIP to destination path
Move-Item -Path $zipName -Destination $SWF_FILE_PATH -Force

# Clean up individual SWF files
Remove-Item "SMF-Fullgame-Build-$BuildNumber.swf","SMF-IL-Build-$BuildNumber.swf","SMF-Cheat-Build-$BuildNumber.swf" -Force

Write-Host "All hacks patched."
