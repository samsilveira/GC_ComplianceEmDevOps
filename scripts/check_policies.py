import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    Path("README.md"),
    Path("CHANGELOG.md"),
    Path("docs/04-politicas.md"),
)

FORBIDDEN_FILES = frozenset({".env", "credentials.json"})
IGNORED_DIRECTORIES = frozenset({".git"})


def check_required_files(project_root: Path = PROJECT_ROOT) -> bool:
    """Verifica se todos os caminhos obrigatórios são arquivos regulares."""
    missing_files = [
        file_path.as_posix()
        for file_path in REQUIRED_FILES
        if not (project_root / file_path).is_file()
    ]

    if missing_files:
        print("[ ERRO ] Os seguintes arquivos obrigatórios estão ausentes:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False

    print("[ SUCESSO ] Todos os arquivos obrigatórios foram encontrados.")
    return True


def check_forbidden_files(project_root: Path = PROJECT_ROOT) -> bool:
    """Verifica se nomes de arquivos proibidos existem no repositório."""
    found_forbidden: list[str] = []

    for root, directories, files in os.walk(project_root):
        directories[:] = [
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        ]

        root_path = Path(root)
        for file_name in files:
            if file_name in FORBIDDEN_FILES:
                relative_path = (root_path / file_name).relative_to(project_root)
                found_forbidden.append(relative_path.as_posix())

    if found_forbidden:
        print("[ ERRO ] Arquivos PROIBIDOS foram encontrados no repositório!")
        for file_path in sorted(found_forbidden):
            print(f"  - {file_path}")
        return False

    print("[ SUCESSO ] Nenhum arquivo proibido foi encontrado.")
    return True


def main(project_root: Path = PROJECT_ROOT) -> int:
    """Executa os controles e retorna um código apropriado para o pipeline."""
    print("--- Iniciando Verificação de Políticas de Conformidade ---\n")

    required_passed = check_required_files(project_root)
    print()
    forbidden_passed = check_forbidden_files(project_root)

    print("\n--- Resultado Final ---")
    if required_passed and forbidden_passed:
        print("[ CONFORME ] Todas as verificações passaram com sucesso!")
        return 0

    print("[ NÃO CONFORME ] Foram encontradas violações nas políticas.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
