
#!/usr/bin/env python3

import argparse
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

PATCHER = "flash-patcher"
SWF_FILE_PATH = Path(".")
VERSION = 30

BASE_SWF = SWF_FILE_PATH / "SMF_Base_Hack.swf"
PATCH_FILE = Path("noncheat/add_build_number.patch")
STAGE_FILES = Path("stagefiles")
PATCH_NOTES = Path("patch-notes.txt")

CHECKSUM = "1fc2f21f69f1e210e0884db1398bebcdfe3612bba7aca97ca48976636486d048b3fa906cbd3325eaeb5dce8449f4db96021f5aca53d8ba0323d61659c3925538"

def run_command(command):
    """Run a command and exit if it fails."""
    subprocess.run(command, check=True)


def main():
    # Dynamically update the build number patch.
    PATCH_FILE.parent.mkdir(parents=True, exist_ok=True)
    PATCH_FILE.write_text(
        "# Add the build number to the hack. Required for speedrun timer "
        "and input display.\n"
        "add frame_1/DoAction.as end\n"
        "begin-patch\n"
        f"_root.build_number = {VERSION};\n"
        "end-patch\n",
        encoding="utf-8",
    )

    # Define the output files.
    outputs = [
        Path(f"SMF-Fullgame-Build-{VERSION}.swf"),
        Path(f"SMF-IL-Build-{VERSION}.swf"),
        Path(f"SMF-Cheat-Build-{VERSION}.swf"),
    ]

    stages = [
        STAGE_FILES / "fullgame.stage",
        STAGE_FILES / "level.stage",
        STAGE_FILES / "cheat.stage",
    ]

    zip_file = Path(f"SMF-Hacks-Build-{VERSION}.zip")

    try:
        # Patch all hacks.
        for stage, output in zip(stages, outputs):
            run_command([
                PATCHER,
                "--inputswf", str(BASE_SWF),
                "--folder", ".",
                "--stagefile", str(stage),
                "--outputswf", str(output),
            ])

        # Create a reproducible ZIP archive.
        with zipfile.ZipFile(
            zip_file,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            for path in [*outputs, PATCH_NOTES]:
                info = zipfile.ZipInfo(
                    filename=path.name,
                    date_time=(2020, 1, 1, 0, 0, 0),
                )
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16

                archive.writestr(
                    info,
                    path.read_bytes(),
                    compress_type=zipfile.ZIP_DEFLATED,
                    compresslevel=9,
                )

        print("All hacks patched")

    finally:
        # Remove intermediate SWF files, even if a command fails.
        for output in outputs:
            output.unlink(missing_ok=True)

    # Compute the BLAKE2b checksum (equivalent to b2sum).
    hasher = hashlib.blake2b()

    with zip_file.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)

    checksum = hasher.hexdigest()
    print(f"{checksum}  {zip_file}")

    if (checksum != CHECKSUM):
        print("Warning! Checksum did not match expected value!")
        print("This is fine when developing locally but it will fail the build!")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f"Error: command failed with exit code {exc.returncode}", file=sys.stderr)
        sys.exit(exc.returncode)
