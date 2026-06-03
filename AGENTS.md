# AGENTS.md

Guia para agentes de desenvolvimento neste repositório.

## Visão geral

Este repositório (`playground`) é um **espaço de trabalho pessoal**, não um monorepo com aplicações web ou serviços. Contém:

- Documentação de estudo (ArecoID, plano BruumHost)
- Assets de apresentação (HTML, PDF, PPTX, planilhas)
- Dois scripts Python que **geram apresentações PowerPoint** via `python-pptx`

Não há `docker-compose`, `package.json`, solução .NET ou testes automatizados neste repo.

## Cursor Cloud specific instructions

### Dependências

- **Python 3.12+** (já disponível na VM)
- **`python-pptx`** — instalado pelo update script na VM startup

Não há `requirements.txt` no repositório; a dependência é instalada diretamente via pip.

### O que executar (funcionalidade principal)

Os únicos “aplicativos” executáveis são os geradores de PPT:

```bash
python3 create_pdi_supervisor_ppt.py      # → PDI_evolucao_supervisor.pptx
python3 create_pdi_justificativas_ppt.py  # → PDI_supervisor_justificativas.pptx
```

Os scripts gravam os arquivos `.pptx` na raiz do repositório (`/workspace`).

### Serviços

| Componente | Necessário? | Notas |
|---|---|---|
| Nenhum serviço de rede | — | Não há API, banco ou frontend para subir |
| Python + python-pptx | Sim (para regenerar PPTs) | Comandos acima |
| Servidor HTTP (opcional) | Não | Para visualizar HTML estático: `python3 -m http.server 8080` |

### Lint / testes / build

- **Lint:** não configurado (sem ESLint, Ruff, etc.)
- **Test($testes):** não há suite de testes
- **Build:** não aplicável; os scripts Python são executados diretamente

### Documentação de referência

- `guia-estudo-arecoid.md` — guia de arquitetura ArecoID (.NET)
- `plano-bruumhost-arecoid.md` — plano de migração BruumHost (stack planejada, **não implementada aqui**)

Para testar ArecoID ou BruumHost de ponta a ponta, use os repositórios externos referenciados nesses documentos.
