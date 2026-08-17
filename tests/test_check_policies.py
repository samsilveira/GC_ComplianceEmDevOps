from pathlib import Path

import pytest

from scripts.check_policies import (
    IGNORED_DIRECTORIES,
    REQUIRED_FILES,
    check_forbidden_files,
    check_required_files,
    main,
)


def create_required_files(project_root: Path) -> None:
    for relative_path in REQUIRED_FILES:
        file_path = project_root / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.touch()


def test_check_required_files_succeeds_with_regular_files(tmp_path: Path) -> None:
    create_required_files(tmp_path)

    assert check_required_files(tmp_path)


def test_check_required_files_fails_when_file_is_missing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    create_required_files(tmp_path)
    (tmp_path / "CHANGELOG.md").unlink()

    assert not check_required_files(tmp_path)
    assert "CHANGELOG.md" in capsys.readouterr().out


def test_check_required_files_rejects_directory_with_file_name(
    tmp_path: Path,
) -> None:
    create_required_files(tmp_path)
    (tmp_path / "CHANGELOG.md").unlink()
    (tmp_path / "CHANGELOG.md").mkdir()
    (tmp_path / "CHANGELOG.md/placeholder.txt").touch()

    assert not check_required_files(tmp_path)


@pytest.mark.parametrize(
    "relative_path",
    (
        Path(".env"),
        Path("credentials.json"),
        Path("config/.env"),
        Path(".github/credentials.json"),
        Path("__pycache__/credentials.json"),
        Path("venv/credentials.json"),
        Path("venv-backup/credentials.json"),
    ),
)
def test_check_forbidden_files_fails_at_any_repository_path(
    tmp_path: Path, relative_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    forbidden_path = tmp_path / relative_path
    forbidden_path.parent.mkdir(parents=True, exist_ok=True)
    forbidden_path.touch()

    assert not check_forbidden_files(tmp_path)
    assert relative_path.as_posix() in capsys.readouterr().out


def test_check_forbidden_files_ignores_only_git_metadata(tmp_path: Path) -> None:
    directory = next(iter(IGNORED_DIRECTORIES))
    ignored_file = tmp_path / directory / "credentials.json"
    ignored_file.parent.mkdir(parents=True)
    ignored_file.touch()

    assert check_forbidden_files(tmp_path)


def test_main_returns_zero_for_compliant_repository(tmp_path: Path) -> None:
    create_required_files(tmp_path)

    assert main(tmp_path) == 0


def test_main_returns_one_for_policy_violation(tmp_path: Path) -> None:
    create_required_files(tmp_path)
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github/credentials.json").touch()

    assert main(tmp_path) == 1
