#!/usr/bin/sh

echo "Usage: ./patch-all.sh [build number]"

export PATCHER="../patcher/flash-patcher.py"
export SWF_FILE_PATH=".."

# Dynamically update the build number
rm -rf noncheat/add-build-number.patch

touch noncheat/add-build-number.patch
echo "# Add the build number to the hack. Required for speedrun timer and input display." >> noncheat/add-build-number.patch
echo "add frame_1/DoAction.as end" >> noncheat/add-build-number.patch
echo "_root.build_number = $1;" >> noncheat/add-build-number.patch
echo "end-patch" >> noncheat/add-build-number.patch

# Patch all hacks
$PATCHER $SWF_FILE_PATH/SMF_Base_Hack.swf . fullgame.stage SMF-Fullgame-Build-$1.swf
$PATCHER $SWF_FILE_PATH/SMF_Base_Hack.swf . level.stage SMF-IL-Build-$1.swf
$PATCHER $SWF_FILE_PATH/SMF_Base_Hack.swf . cheat.stage SMF-Cheat-Build-$1.swf

# Bundle as a .zip for export
zip SMF-Hacks-Build-$1 SMF-Fullgame-Build-$1.swf SMF-IL-Build-$1.swf SMF-Cheat-Build-$1.swf patch-notes.txt
mv SMF-Hacks-Build-$1.zip $SWF_FILE_PATH

rm SMF-Cheat-Build-$1.swf
rm SMF-IL-Build-$1.swf
rm SMF-Fullgame-Build-$1.swf

echo "All hacks patched"
