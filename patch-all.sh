#!/usr/bin/bash
set -euo pipefail

echo "Usage: ./patch-all.sh [build number]"

export PATCHER="flash-patcher"
export SWF_FILE_PATH="."

# Dynamically update the build number
rm -rf noncheat/add_build_number.patch

touch noncheat/add_build_number.patch
echo "# Add the build number to the hack. Required for speedrun timer and input display." >> noncheat/add_build_number.patch
echo "add frame_1/DoAction.as end" >> noncheat/add_build_number.patch
echo "begin-patch" >> noncheat/add_build_number.patch
echo "_root.build_number = $1;" >> noncheat/add_build_number.patch
echo "end-patch" >> noncheat/add_build_number.patch

# Patch all hacks
$PATCHER --inputswf $SWF_FILE_PATH/SMF_Base_Hack.swf --folder . --stagefile stagefiles/fullgame.stage --outputswf SMF-Fullgame-Build-$1.swf
$PATCHER --inputswf $SWF_FILE_PATH/SMF_Base_Hack.swf --folder . --stagefile stagefiles/level.stage --outputswf SMF-IL-Build-$1.swf
$PATCHER --inputswf $SWF_FILE_PATH/SMF_Base_Hack.swf --folder . --stagefile stagefiles/cheat.stage --outputswf SMF-Cheat-Build-$1.swf

# Bundle as a .zip for export
zip SMF-Hacks-Build-$1 SMF-Fullgame-Build-$1.swf SMF-IL-Build-$1.swf SMF-Cheat-Build-$1.swf patch-notes.txt

if [ "$SWF_FILE_PATH" != "." ]; then
    mv SMF-Hacks-Build-$1.zip $SWF_FILE_PATH
fi

rm SMF-Cheat-Build-$1.swf
rm SMF-IL-Build-$1.swf
rm SMF-Fullgame-Build-$1.swf

echo "All hacks patched"
