from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path

DEFAULT_FOLDERS = [
    ".conda",
    ".anaconda",
    ".continuum",
    ".android",
    ".cache",
    ".gradle",
    ".matplotlib",
    ".ollama",
    ".qiskit",
    ".VirtualBox",
    ".vscode",
    ".insightface",
    ".venv",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Move selected user-profile folders to another drive and replace them with directory symlinks."
    )
    parser.add_argument(
        "--target-root",
        default=r"E:\UsersData",
        help="Destination root for moved folders. Default: E:\\UsersData",
    )
    parser.add_argument(
        "--folders",
        nargs="*",
        default=DEFAULT_FOLDERS,
        help="Folder names inside USERPROFILE to move. Default: common heavy dev/tool folders.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually move folders and create symlinks. Without this flag the command is a dry-run.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip interactive confirmation when --apply is used.",
    )
    return parser.parse_args()


def ensure_safe_destination(user_profile: Path, target_root: Path) -> None:
    user_profile_resolved = user_profile.resolve()
    target_resolved = target_root.resolve() if target_root.exists() else target_root.absolute()

    if target_resolved == user_profile_resolved or user_profile_resolved in target_resolved.parents:
        raise ValueError("target-root must not be inside USERPROFILE; this would create unsafe recursive moves.")

    if target_resolved.drive.upper() == user_profile_resolved.drive.upper():
        print(
            "Warning: target-root is on the same drive as USERPROFILE. "
            "This may not free space on the system drive."
        )


def planned_operations(user_profile: Path, target_root: Path, folders: list[str]) -> list[tuple[Path, Path]]:
    operations: list[tuple[Path, Path]] = []
    for folder in folders:
        src = user_profile / folder
        dst = target_root / folder
        if not src.exists():
            print(f"Skip missing: {src}")
            continue
        if src.is_symlink():
            print(f"Skip symlink: {src}")
            continue
        if dst.exists():
            print(f"Skip existing destination: {dst}")
            continue
        operations.append((src, dst))
    return operations


def confirm(operations: list[tuple[Path, Path]]) -> bool:
    print("\nPlanned changes:")
    for src, dst in operations:
        print(f"  MOVE {src} -> {dst}")
        print(f"  LINK {src} -> {dst}")

    answer = input("\nApply these filesystem changes? Type YES to continue: ")
    return answer == "YES"


def create_directory_symlink(src: Path, dst: Path) -> None:
    subprocess.run(
        ["cmd", "/c", "mklink", "/D", str(src), str(dst)],
        check=True,
    )


def apply_operations(target_root: Path, operations: list[tuple[Path, Path]]) -> None:
    target_root.mkdir(parents=True, exist_ok=True)

    for src, dst in operations:
        print(f"Moving: {src} -> {dst}")
        shutil.move(str(src), str(dst))
        print(f"Creating symlink: {src} -> {dst}")
        create_directory_symlink(src, dst)


def main() -> None:
    args = parse_args()
    user_profile = Path(os.environ["USERPROFILE"])
    target_root = Path(args.target_root)

    ensure_safe_destination(user_profile, target_root)
    operations = planned_operations(user_profile, target_root, args.folders)

    if not operations:
        print("No operations to perform.")
        return

    if not args.apply:
        print("Dry-run only. Add --apply to move folders and create symlinks.\n")
        for src, dst in operations:
            print(f"Would move: {src} -> {dst}")
            print(f"Would link: {src} -> {dst}")
        return

    if not args.yes and not confirm(operations):
        print("Aborted.")
        return

    apply_operations(target_root, operations)
    print("Done.")


if __name__ == "__main__":
    main()
