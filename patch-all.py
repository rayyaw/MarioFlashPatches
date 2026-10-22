
#!/usr/bin/env python3

import argparse
import hashlib
import subprocess
import sys
import zipfile
from pathlib import Path

PATCHER = "flash-patcher"
SWF_FILE_PATH = Path(".")
VERSION = "DEBUG_RUNNER"

BASE_SWF = SWF_FILE_PATH / "SMF_Base_Hack.swf"
PATCH_FILE = Path("noncheat/add_build_number.patch")
STAGE_FILES = Path("stagefiles")
PATCH_NOTES = Path("patch-notes.txt")

CHECKSUM = {
    'SMF-Fullgame-Build-DEBUG_RUNNER.swf': 'b10ff97988c4646d62662a59ee47973f5305fb08d2833ce95f721e4a1d1b92a41e17b2099760e3f06b8c9350340c972ec95475ef0612d0d7cfb81131397e2fd4',
    'SMF-IL-Build-DEBUG_RUNNER.swf': 'e738e3119becf481415a892751baa1153f33ed392db0eabaf54bf99209025f052dc42aeee720aeca8e25738338bdc08fefbbe57548f90d945364431919c20ae5',
    'SMF-Cheat-Build-DEBUG_RUNNER.swf': '8b3c89469a40ee885ac9bbbfbb81b9b4f40c169d8e1f5ed5ddb4b003739f8e291e5d369fd5fdbc85aca40db73de2c364d6195ce397c85fcc18de895afab01d63',
}

global EXIT_CODE
EXIT_CODE = 0

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

            # Compute the BLAKE2b checksum (equivalent to b2sum).
            hasher = hashlib.blake2b()

            with open(str(output), "rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    hasher.update(chunk)

            checksum = hasher.hexdigest()

            print(f"{checksum}  {str(output)}")

            if (checksum != CHECKSUM[str(output)]):
                print("Warning! Checksum did not match expected value!")
                print("This is fine when developing locally but it will fail the build!")
                EXIT_CODE = 1

        # Create a reproducible ZIP archive.
        with zipfile.ZipFile(zip_file, "w") as archive:
            for path in [*outputs, PATCH_NOTES]:
                archive.write(path, path.name)

        print("All hacks patched")

    finally:
        # Remove intermediate SWF files, even if a command fails.
        for output in outputs:
            output.unlink(missing_ok=True)

if __name__ == "__main__":
    try:
        main()
        sys.exit(EXIT_CODE)
    except subprocess.CalledProcessError as exc:
        print(f"Error: command failed with exit code {exc.returncode}", file=sys.stderr)
        sys.exit(exc.returncode)
