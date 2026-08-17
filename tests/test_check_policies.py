import os
import sys
from unittest.mock import patch

# Adiciona a raiz do projeto ao path para conseguir importar o seu script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.check_policies import check_forbidden_files, check_required_files


class TestCheckPolicies:

    @patch('os.path.exists')
    def test_check_required_files_sucesso(self, mock_exists):
        """Testa o cenário onde todos os arquivos obrigatórios existem."""
        # Finge que qualquer arquivo procurado existe (Retorna True)
        mock_exists.return_value = True
        assert check_required_files()

    @patch('os.path.exists')
    def test_check_required_files_falha(self, mock_exists):
        """Testa o cenário onde os arquivos obrigatórios não existem."""
        # Finge que os arquivos procurados não existem (Retorna False)
        mock_exists.return_value = False
        assert not check_required_files()

    @patch('os.walk')
    def test_check_forbidden_files_sucesso(self, mock_walk):
        """Testa o cenário onde nenhum arquivo proibido é encontrado."""
        # Simula uma pasta que só tem arquivos permitidos
        mock_walk.return_value = [
            ('.', ('dir',), ('README.md', 'main.py', 'CHANGELOG.md')),
        ]
        assert check_forbidden_files()

    @patch('os.walk')
    def test_check_forbidden_files_falha(self, mock_walk):
        """Testa o cenário onde um arquivo proibido existe."""
        # Simula uma pasta onde alguém colocou um arquivo .env
        mock_walk.return_value = [
            ('.', ('dir',), ('README.md', '.env')),
        ]
        assert not check_forbidden_files()