# Super Mario Flash hack patches

## Requirements

- FFDec version 23.0.1: https://github.com/jindrapetrik/jpexs-decompiler/releases/tag/version23.0.1 (Later versions will not work)
- Riley's Flash Patcher: https://github.com/rayyaw/flash-patcher
- SMF Base Hack: https://marioflashcommunity.github.io/game-downloads

## Running

### MacOS / Linux

- Update the `SWF_FILE_PATH` and `PATCHER_PATH` in `patch_all.sh`
- Run `./patch-all.sh [build number]`

### Windows
- Run `.\patch-all.ps1 [build number]`.

If you encounter auth issues, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` to allow execution of .ps1 scripts.

The output will be saved in `SMF_Hacks_Build-[buildno].zip`.
