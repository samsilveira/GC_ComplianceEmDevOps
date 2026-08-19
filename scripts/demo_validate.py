#!/usr/bin/env python3
"""Executa e resume as validações usadas na demonstração do projeto."""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPOSITORY = "samsilveira/GC_ComplianceEmDevOps"
DEFAULT_WORKFLOW = "compliance.yml"
HISTORICAL_RUNS = (
    (31809146741, "success", "Aprovação inicial"),
    (31955024357, "failure", "Bloqueio de segredo sintético"),
    (32040521363, "failure", "Bloqueio de arquivo .env"),
    (32062843662, "success", "Aprovação após correção"),
)
SKIPPED_DIRECTORIES = frozenset({".git", ".venv", "venv", "node_modules", "reports"})


@dataclass(frozen=True)
class CheckResult:
    """Resultado normalizado de uma validação da demonstração."""

    name: str
    passed: bool
    summary: str
    duration_seconds: float = 0.0
    output: str = ""
    skipped: bool = False

    @property
    def status(self) -> str:
        if self.skipped:
            return "SKIP"
        return "PASS" if self.passed else "FAIL"


def combined_output(process: subprocess.CompletedProcess[str]) -> str:
    """Combina stdout e stderr sem perder mensagens relevantes."""

    parts = [part.strip() for part in (process.stdout, process.stderr) if part.strip()]
    return "\n".join(parts)


def executable_command(name: str, *arguments: str) -> list[str]:
    """Localiza uma ferramenta instalada ao lado do Python ou no PATH."""

    suffix = ".exe" if os.name == "nt" else ""
    sibling = Path(sys.executable).parent / f"{name}{suffix}"
    if sibling.is_file():
        return [str(sibling), *arguments]

    executable = shutil.which(name)
    if executable:
        return [executable, *arguments]

    return [name, *arguments]


def run_command(
    name: str,
    command: list[str],
    *,
    expected_codes: Iterable[int] = (0,),
    cwd: Path = PROJECT_ROOT,
) -> CheckResult:
    """Executa um comando e converte seu código de saída em CheckResult."""

    print(f"\n[RUN ] {name}")
    print(f"       {' '.join(command)}")
    started = time.monotonic()
    try:
        process = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as error:
        duration = time.monotonic() - started
        result = CheckResult(
            name=name,
            passed=False,
            summary=f"Comando não encontrado: {error.filename}",
            duration_seconds=duration,
            output=str(error),
        )
        print_result(result)
        return result

    duration = time.monotonic() - started
    output = combined_output(process)
    passed = process.returncode in set(expected_codes)
    result = CheckResult(
        name=name,
        passed=passed,
        summary=f"código de saída {process.returncode}",
        duration_seconds=duration,
        output=output,
    )
    if output:
        print(output)
    print_result(result)
    return result


def print_result(result: CheckResult) -> None:
    """Imprime uma linha curta, adequada para apresentação e gravação."""

    print(
        f"[{result.status:<4}] {result.name} — {result.summary} "
        f"({result.duration_seconds:.2f}s)"
    )


def validate_api_contract() -> CheckResult:
    """Exercita as duas rotas sem iniciar servidor ou processo em background."""

    print("\n[RUN ] Contrato HTTP da API")
    started = time.monotonic()
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    try:
        from app.main import app

        with app.test_client() as client:
            index_response = client.get("/")
            health_response = client.get("/health")
            index_payload = index_response.get_json()
            health_payload = health_response.get_json()

        failures: list[str] = []
        if index_response.status_code != 200:
            failures.append(f"GET / retornou {index_response.status_code}")
        if not index_payload or index_payload.get("version") != "1.0.0":
            failures.append("GET / não informou version=1.0.0")
        if health_response.status_code != 200:
            failures.append(f"GET /health retornou {health_response.status_code}")
        if not health_payload or health_payload.get("status") != "up":
            failures.append("GET /health não informou status=up")
        if not health_payload or health_payload.get("healthy") is not True:
            failures.append("GET /health não informou healthy=true")

        passed = not failures
        summary = "rotas / e /health aprovadas" if passed else "; ".join(failures)
        output = json.dumps(
            {"/": index_payload, "/health": health_payload},
            ensure_ascii=False,
            indent=2,
        )
    except Exception as error:  # pragma: no cover - proteção operacional
        passed = False
        summary = f"erro ao exercitar a API: {error}"
        output = repr(error)

    result = CheckResult(
        name="Contrato HTTP da API",
        passed=passed,
        summary=summary,
        duration_seconds=time.monotonic() - started,
        output=output,
    )
    print(output)
    print_result(result)
    return result


def local_markdown_link_failures(root: Path = PROJECT_ROOT) -> list[str]:
    """Retorna links Markdown relativos cujo destino não existe."""

    failures: list[str] = []
    link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

    for markdown_file in sorted(root.rglob("*.md")):
        relative_parts = markdown_file.relative_to(root).parts
        if any(part in SKIPPED_DIRECTORIES for part in relative_parts):
            continue

        text = markdown_file.read_text(encoding="utf-8")
        for match in link_pattern.finditer(text):
            raw_target = match.group(1).strip().strip("<>")
            if not raw_target or raw_target.startswith(
                ("#", "http://", "https://", "mailto:")
            ):
                continue

            target = raw_target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue

            resolved = (markdown_file.parent / unquote(target)).resolve()
            if not resolved.exists():
                line = text.count("\n", 0, match.start()) + 1
                relative_file = markdown_file.relative_to(root).as_posix()
                failures.append(f"{relative_file}:{line} -> {raw_target}")

    return failures


def validate_local_links() -> CheckResult:
    """Verifica a navegação Markdown local usada no modo contingência."""

    print("\n[RUN ] Links Markdown locais")
    started = time.monotonic()
    failures = local_markdown_link_failures()
    result = CheckResult(
        name="Links Markdown locais",
        passed=not failures,
        summary=(
            "nenhum destino relativo quebrado"
            if not failures
            else f"{len(failures)} link(s) quebrado(s)"
        ),
        duration_seconds=time.monotonic() - started,
        output="\n".join(failures),
    )
    if failures:
        print(result.output)
    print_result(result)
    return result


def validate_controlled_policy_failure() -> CheckResult:
    """Demonstra uma não conformidade somente em diretório temporário."""

    print("\n[RUN ] Bloqueio controlado de arquivo .env")
    started = time.monotonic()
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))

    from scripts.check_policies import REQUIRED_FILES, main

    with tempfile.TemporaryDirectory(prefix="compliance-demo-") as directory:
        demo_root = Path(directory)
        for relative_path in REQUIRED_FILES:
            file_path = demo_root / relative_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()
        (demo_root / ".env").touch()

        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            return_code = main(demo_root)
        output = captured.getvalue().strip()

    passed = return_code == 1 and ".env" in output and "[ NÃO CONFORME ]" in output
    result = CheckResult(
        name="Bloqueio controlado de arquivo .env",
        passed=passed,
        summary=(
            "violação temporária bloqueada como esperado"
            if passed
            else f"resultado inesperado, código {return_code}"
        ),
        duration_seconds=time.monotonic() - started,
        output=output,
    )
    print(output)
    print_result(result)
    return result


def skipped_result(name: str, summary: str) -> CheckResult:
    result = CheckResult(
        name=name,
        passed=True,
        summary=summary,
        skipped=True,
    )
    print_result(result)
    return result


def run_local_suite(*, offline: bool) -> list[CheckResult]:
    """Executa as verificações locais do mesmo contrato usado no CI."""

    reports_directory = PROJECT_ROOT / "reports"
    reports_directory.mkdir(exist_ok=True)

    results = [
        run_command(
            "Testes automatizados",
            [
                sys.executable,
                "-m",
                "pytest",
                "--junitxml=reports/demo-junit.xml",
            ],
        ),
        run_command(
            "Qualidade de código com Ruff",
            executable_command(
                "ruff",
                "check",
                ".",
                "--output-format=json",
                "--output-file=reports/demo-ruff.json",
            ),
        ),
    ]

    if offline:
        results.append(
            skipped_result(
                "Auditoria de dependências com pip-audit",
                "ignorada por --offline",
            )
        )
    else:
        results.append(
            run_command(
                "Auditoria de dependências com pip-audit",
                executable_command(
                    "pip-audit",
                    "--requirement",
                    "requirements.txt",
                    "--strict",
                    "--format=json",
                    "--output=reports/demo-pip-audit.json",
                ),
            )
        )

    results.extend(
        [
            run_command(
                "Políticas internas",
                [sys.executable, "scripts/check_policies.py"],
            ),
            validate_api_contract(),
            validate_local_links(),
            run_command("Integridade do diff", ["git", "diff", "--check"]),
        ]
    )
    return results


def gh_json(arguments: list[str]) -> tuple[int, object | None, str]:
    """Executa gh esperando JSON e preserva mensagem de erro legível."""

    try:
        process = subprocess.run(
            ["gh", *arguments],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as error:
        return 127, None, str(error)

    output = combined_output(process)
    if process.returncode != 0:
        return process.returncode, None, output
    try:
        return 0, json.loads(process.stdout), output
    except json.JSONDecodeError as error:
        return 1, None, f"JSON inválido retornado pelo gh: {error}\n{output}"


def validate_historical_run(
    run_id: int,
    expected_conclusion: str,
    label: str,
    repository: str,
) -> CheckResult:
    """Confirma os identificadores imutáveis usados no roteiro histórico."""

    print(f"\n[RUN ] {label} — run {run_id}")
    started = time.monotonic()
    code, payload, output = gh_json(
        [
            "run",
            "view",
            str(run_id),
            "--repo",
            repository,
            "--json",
            "databaseId,headSha,event,status,conclusion,url",
        ]
    )
    conclusion = payload.get("conclusion") if isinstance(payload, dict) else None
    passed = code == 0 and conclusion == expected_conclusion
    summary = (
        f"conclusão {conclusion} conforme esperado"
        if passed
        else f"esperado {expected_conclusion}, observado {conclusion or 'indisponível'}"
    )
    normalized_output = (
        json.dumps(payload, ensure_ascii=False, indent=2)
        if payload is not None
        else output
    )
    result = CheckResult(
        name=f"{label} — run {run_id}",
        passed=passed,
        summary=summary,
        duration_seconds=time.monotonic() - started,
        output=normalized_output,
    )
    print(normalized_output)
    print_result(result)
    return result


def run_github_suite(repository: str) -> list[CheckResult]:
    """Consulta, sem alterar o remoto, os quatro runs do roteiro auditável."""

    results = [
        run_command(
            "Autenticação do GitHub CLI",
            ["gh", "auth", "status"],
        )
    ]
    results.extend(
        validate_historical_run(run_id, conclusion, label, repository)
        for run_id, conclusion, label in HISTORICAL_RUNS
    )
    return results


def validate_release(repository: str, workflow: str) -> list[CheckResult]:
    """Valida tag anotada, GitHub Release e pipeline do commit entregue."""

    results: list[CheckResult] = []
    print("\n[RUN ] Tag anotada v1.0.0")
    started = time.monotonic()
    code, reference, output = gh_json(
        ["api", f"repos/{repository}/git/ref/tags/v1.0.0"]
    )
    object_data = reference.get("object", {}) if isinstance(reference, dict) else {}
    object_type = object_data.get("type")
    tag_object_sha = object_data.get("sha")
    annotated = code == 0 and object_type == "tag" and bool(tag_object_sha)
    tag_result = CheckResult(
        name="Tag anotada v1.0.0",
        passed=annotated,
        summary=(
            "referência aponta para objeto Git do tipo tag"
            if annotated
            else f"tipo observado: {object_type or 'indisponível'}"
        ),
        duration_seconds=time.monotonic() - started,
        output=(
            json.dumps(reference, ensure_ascii=False, indent=2)
            if reference is not None
            else output
        ),
    )
    print_result(tag_result)
    results.append(tag_result)

    commit_sha: str | None = None
    if annotated:
        code, tag_object, output = gh_json(
            ["api", f"repos/{repository}/git/tags/{tag_object_sha}"]
        )
        target = tag_object.get("object", {}) if isinstance(tag_object, dict) else {}
        commit_sha = target.get("sha") if target.get("type") == "commit" else None
        target_result = CheckResult(
            name="Commit entregue pela tag",
            passed=code == 0 and bool(commit_sha),
            summary=commit_sha or "objeto final não é um commit",
            output=(
                json.dumps(tag_object, ensure_ascii=False, indent=2)
                if tag_object is not None
                else output
            ),
        )
    else:
        target_result = skipped_result(
            "Commit entregue pela tag",
            "tag anotada ainda não disponível",
        )
    print_result(target_result) if not target_result.skipped else None
    results.append(target_result)

    print("\n[RUN ] GitHub Release v1.0.0")
    started = time.monotonic()
    code, release, output = gh_json(
        [
            "release",
            "view",
            "v1.0.0",
            "--repo",
            repository,
            "--json",
            "isDraft,isPrerelease,tagName,targetCommitish,url",
        ]
    )
    release_valid = (
        code == 0
        and isinstance(release, dict)
        and release.get("tagName") == "v1.0.0"
        and release.get("isDraft") is False
        and release.get("isPrerelease") is False
    )
    release_result = CheckResult(
        name="GitHub Release v1.0.0",
        passed=release_valid,
        summary=(
            "publicada, não draft e não prerelease"
            if release_valid
            else "release final não encontrada ou ainda pendente"
        ),
        duration_seconds=time.monotonic() - started,
        output=(
            json.dumps(release, ensure_ascii=False, indent=2)
            if release is not None
            else output
        ),
    )
    print_result(release_result)
    results.append(release_result)

    if commit_sha:
        print("\n[RUN ] Pipeline do commit entregue")
        started = time.monotonic()
        code, runs, output = gh_json(
            [
                "run",
                "list",
                "--repo",
                repository,
                "--workflow",
                workflow,
                "--commit",
                commit_sha,
                "--json",
                "databaseId,headSha,event,status,conclusion,url",
            ]
        )
        successful_runs = (
            [
                run
                for run in runs
                if isinstance(run, dict)
                and run.get("headSha") == commit_sha
                and run.get("conclusion") == "success"
            ]
            if isinstance(runs, list)
            else []
        )
        pipeline_result = CheckResult(
            name="Pipeline do commit entregue",
            passed=code == 0 and bool(successful_runs),
            summary=(
                f"{len(successful_runs)} execução(ões) aprovada(s)"
                if successful_runs
                else "nenhuma execução verde encontrada para o SHA"
            ),
            duration_seconds=time.monotonic() - started,
            output=(
                json.dumps(runs, ensure_ascii=False, indent=2)
                if runs is not None
                else output
            ),
        )
    else:
        pipeline_result = skipped_result(
            "Pipeline do commit entregue",
            "SHA final ainda indisponível",
        )
    print_result(pipeline_result) if not pipeline_result.skipped else None
    results.append(pipeline_result)
    return results


def write_report(path: Path, mode: str, results: list[CheckResult]) -> None:
    """Persiste um resumo Markdown sem modificar arquivos versionados."""

    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Resumo da demonstração de compliance",
        "",
        f"- Gerado em: {datetime.now(timezone.utc).isoformat()}",
        f"- Modo: `{mode}`",
        f"- Python: `{sys.version.split()[0]}`",
        "",
        "| Verificação | Estado | Duração | Resumo |",
        "| --- | --- | ---: | --- |",
    ]
    for result in results:
        safe_summary = result.summary.replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {result.name} | {result.status} | "
            f"{result.duration_seconds:.2f}s | {safe_summary} |"
        )

    for result in results:
        if not result.output:
            continue
        lines.extend(
            [
                "",
                f"## {result.name}",
                "",
                "```text",
                result.output[:8000],
                "```",
            ]
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        display_path = path.relative_to(PROJECT_ROOT)
    except ValueError:
        display_path = path
    print(f"\nRelatório salvo em {display_path}")


def print_summary(results: list[CheckResult]) -> int:
    """Exibe o placar final e retorna o código adequado para automação."""

    passed = sum(result.passed and not result.skipped for result in results)
    failed = sum(not result.passed for result in results)
    skipped = sum(result.skipped for result in results)
    final_status = "APROVADO" if failed == 0 else "NÃO CONFORME"
    print("\n" + "=" * 72)
    print(f"RESULTADO: {final_status} | PASS={passed} | FAIL={failed} | SKIP={skipped}")
    print("=" * 72)
    return 0 if failed == 0 else 1


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa validações locais, históricas e de release.",
    )
    parser.add_argument(
        "mode",
        nargs="?",
        default="local",
        choices=("local", "policy-failure", "github", "release", "all"),
        help="conjunto de verificações a executar (padrão: local)",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="no modo local, ignora apenas a consulta do pip-audit",
    )
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPOSITORY,
        help=f"repositório GitHub (padrão: {DEFAULT_REPOSITORY})",
    )
    parser.add_argument(
        "--workflow",
        default=DEFAULT_WORKFLOW,
        help=f"workflow oficial (padrão: {DEFAULT_WORKFLOW})",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=PROJECT_ROOT / "reports" / "demo-summary.md",
        help="caminho do relatório Markdown",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="não grava o resumo em reports/",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    if arguments.offline and arguments.mode in {"github", "release"}:
        print("--offline só pode ser usado com os modos local ou all.", file=sys.stderr)
        return 2

    print("Compliance em DevOps — validação para demonstração")
    print(f"Raiz: {PROJECT_ROOT}")
    print(f"Modo: {arguments.mode}")

    results: list[CheckResult] = []
    if arguments.mode in {"local", "all"}:
        results.extend(run_local_suite(offline=arguments.offline))
    if arguments.mode in {"policy-failure", "all"}:
        results.append(validate_controlled_policy_failure())
    if arguments.mode in {"github", "all"}:
        if arguments.offline:
            results.append(
                skipped_result("Evidências históricas no GitHub", "modo offline")
            )
        else:
            results.extend(run_github_suite(arguments.repo))
    if arguments.mode in {"release", "all"}:
        if arguments.offline:
            results.append(skipped_result("Validação da release", "modo offline"))
        else:
            results.extend(validate_release(arguments.repo, arguments.workflow))

    if not arguments.no_report:
        report_path = arguments.report
        if not report_path.is_absolute():
            report_path = PROJECT_ROOT / report_path
        write_report(report_path, arguments.mode, results)
    return print_summary(results)


if __name__ == "__main__":
    raise SystemExit(main())
