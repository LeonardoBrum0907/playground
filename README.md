# playground

## Automacao de planilha (1 clique)

Este projeto agora possui um fluxo simples para transformar o CSV exportado em um Excel padrao com:

- Aba **Dados** com as colunas:
  - Atividade
  - Horas Apontadas
  - Apontado por
  - Data de Início Real
  - Data de Fim Real
- Aba **Resumo** com total de horas por colaborador (somatorio automatico via formula).

### 1) Instalar dependencia (uma vez)

```bash
python3 -m pip install openpyxl
```

### 2) Colocar o CSV na pasta de entrada

```bash
mkdir -p entrada saida
```

Coloque o arquivo `.csv` em `./entrada`.

### 3) Rodar em 1 comando

```bash
./executar_automacao.sh
```

Isso processa o CSV mais recente da pasta `entrada` e gera o arquivo final em `./saida`.

### Acumular diariamente (sem apagar historico)

Use este modo para ir adicionando os dias no mesmo arquivo final:

```bash
./executar_automacao.sh --arquivo "/caminho/arquivo_do_dia.csv" --acumular-em "saida/historico_apontamentos.xlsx"
```

Se executar novamente com o mesmo arquivo, o script nao duplica linhas identicas.

### Opcoes uteis

Processar um arquivo especifico:

```bash
./executar_automacao.sh --arquivo "/caminho/arquivo.csv"
```

Processar todos os CSVs da pasta `entrada`:

```bash
./executar_automacao.sh --todos
```

Processar todos os arquivos da pasta e acumular em um unico historico:

```bash
./executar_automacao.sh --todos --acumular-em "saida/historico_apontamentos.xlsx"
```
