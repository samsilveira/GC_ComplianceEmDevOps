import os
import sys

# Definindo as políticas
REQUIRED_FILES = [
    "README.md",
    "CHANGELOG.md",
    "docs/04-politicas.md"
]

FORBIDDEN_FILES = [
    ".env",
    "credentials.json"
]

def check_required_files():
    """Verifica se os arquivos obrigatórios existem."""
    missing_files = []
    for file_path in REQUIRED_FILES:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("[ ERRO ] Os seguintes arquivos obrigatórios estão ausentes:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("[ SUCESSO ] Todos os arquivos obrigatórios foram encontrados.")
    return True

def check_forbidden_files():
    """Verifica se arquivos proibidos foram adicionados ao repositório."""
    found_forbidden = []
    # Usando os.walk para procurar em subdiretórios, ignorando pastas comuns de ambiente
    for root, dirs, files in os.walk("."):
        if ".git" in root or "__pycache__" in root or "venv" in root:
            continue
            
        for file in files:
            if file in FORBIDDEN_FILES:
                found_forbidden.append(os.path.join(root, file))
                
    if found_forbidden:
        print("[ ERRO ] Arquivos PROIBIDOS foram encontrados no repositório!")
        for file in found_forbidden:
            print(f"  - {file}")
        return False
        
    print("[ SUCESSO ] Nenhum arquivo proibido foi encontrado.")
    return True

def main():
    print("--- Iniciando Verificação de Políticas de Conformidade ---\n")
    
    required_passed = check_required_files()
    print("") # Linha em branco para separar os logs
    forbidden_passed = check_forbidden_files()
    
    print("\n--- Resultado Final ---")
    if required_passed and forbidden_passed:
        print("[ CONFORME ] Todas as verificações passaram com sucesso!")
        sys.exit(0) # Retorna 0 (sucesso) para o pipeline
    else:
        print("[ NÃO CONFORME ] Foram encontradas violações nas políticas.")
        sys.exit(1) # Retorna 1 (falha) para o pipeline bloquear o merge

if __name__ == "__main__":
    main()