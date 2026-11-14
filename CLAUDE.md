# CLAUDE.md - NBA Data Platform Reconstruction

## Contexto
Projeto de portfólio de Data Engineering. Origem académica (2022, C# + Selenium + R + SQL Server), reconstruído em Python, FastAPI, PostgreSQL (Supabase), Render e GitHub Actions.

## Mentalidade de segurança
Atuar sempre com perspetiva de cybersecurity e integridade de dados:
- Antes de alterar código, identificar o risco (dados incorretos, segredos expostos, endpoints sem validação, queries não parametrizadas).
- Nunca commitar credenciais, strings de ligação, caminhos locais (C:\Users\..., /Users/...) ou dados pessoais.
- Qualquer métrica publicada (README, Notion, LinkedIn) deve ter um script ou teste que a reproduza.
- Relatórios de ferramentas (gitleaks, bandit, pip-audit) ficam fora do repositório (ex: ~/ ou scratchpad).

## Git
- Não fazer commit, push ou force-push sem confirmação explícita do owner.
- Mensagens de commit: Conventional Commits, em inglês, descrevendo o que mudou e porquê.
- Não incluir linhas de atribuição (Co-Authored-By, Claude-Session) nem menções a IA nas mensagens de commit.
- Não incluir o rodapé "Generated with Claude Code" nas descrições de PR.
- Trabalhar sempre em branch próprio. Nunca commitar diretamente na main.

## Escrita
- Não usar travessão (U+2014). Usar hífen "-".
- Comunicação com o owner em português europeu.
- Documentação técnica em inglês.
- Textos públicos (README, LinkedIn, CV) sem nomes de clientes ou empregadores.

## Dados
- Não publicar dados extraídos de fontes externas sem confirmar licenciamento e termos de utilização.
- Campeões e estatísticas legadas devem ser validadas contra fonte oficial antes de serem usadas em métricas.
