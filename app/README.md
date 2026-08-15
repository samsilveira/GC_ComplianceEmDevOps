# API do Experimento (Aplicação Mínima)

Esta aplicação foi desenvolvida com o objetivo exclusivo de servir como objeto de testes para o pipeline de conformidade em DevOps.

## Decisões e Limitações

- **Escopo Reduzido:** A API possui apenas duas rotas (`/` e `/health`). Ela não se conecta a bancos de dados, cache ou serviços de mensageria. Isso é proposital, para garantir que as falhas e os bloqueios no pipeline sejam resultantes das políticas de conformidade (testes, lint, segurança), e não de instabilidade ou complexidade da própria aplicação.
- **Ausência de Autenticação/Autorização:** Não foram implementados controles de acesso, pois o foco não é a segurança da aplicação, mas a validação de código e dependências.
- **Determinismo:** As respostas das rotas são totalmente determinísticas, permitindo que os testes unitários sejam rápidos e robustos, sem falsos positivos.

## Instalação e Inicialização

Para preparar e iniciar a aplicação a partir de um clone limpo, utilize:

```sh
git clone https://github.com/samsilveira/GC_ComplianceEmDevOps.git
cd GC_ComplianceEmDevOps

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

flask --app app.main run
```

No Windows PowerShell, ative o ambiente virtual com `.venv\Scripts\Activate.ps1` antes de instalar as dependências.

E para realizar requisições de teste localmente:

```sh
curl http://127.0.0.1:5000/
curl http://127.0.0.1:5000/health
```

## Testes Automatizados

Para instalar a dependência de teste e executar a suíte:

```sh
python -m pip install -r requirements-dev.txt
pytest
```

O pytest cria o relatório JUnit em `reports/junit.xml`.
