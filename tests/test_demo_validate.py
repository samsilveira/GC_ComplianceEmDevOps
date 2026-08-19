from pathlib import Path

from scripts.demo_validate import (
    executable_command,
    local_markdown_link_failures,
    validate_controlled_policy_failure,
    write_report,
)


def test_local_markdown_link_failures_accepts_existing_target(
    tmp_path: Path,
) -> None:
    target = tmp_path / "target.md"
    target.write_text("# Destino\n", encoding="utf-8")
    source = tmp_path / "source.md"
    source.write_text("[Destino](target.md)\n", encoding="utf-8")

    assert local_markdown_link_failures(tmp_path) == []


def test_local_markdown_link_failures_reports_missing_target(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.md"
    source.write_text("[Ausente](missing.md)\n", encoding="utf-8")

    assert local_markdown_link_failures(tmp_path) == ["source.md:1 -> missing.md"]


def test_controlled_policy_failure_is_expected() -> None:
    result = validate_controlled_policy_failure()

    assert result.passed
    assert ".env" in result.output
    assert "[ NÃO CONFORME ]" in result.output


def test_executable_command_finds_virtual_environment_binary(
    tmp_path: Path,
    monkeypatch,
) -> None:
    python = tmp_path / "python"
    tool = tmp_path / "ruff"
    python.touch()
    tool.touch()
    monkeypatch.setattr("scripts.demo_validate.sys.executable", str(python))

    assert executable_command("ruff", "check", ".") == [
        str(tool),
        "check",
        ".",
    ]


def test_write_report_accepts_path_outside_project(tmp_path: Path) -> None:
    report = tmp_path / "summary.md"

    write_report(report, "local", [])

    assert report.is_file()
    assert "Modo: `local`" in report.read_text(encoding="utf-8")
