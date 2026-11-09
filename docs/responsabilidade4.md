# Entrega da Responsabilidade 4 para a Pessoa 5

**Projeto:** Educação e renda dos municípios | **Fase 01** | **Ano de referência: 2023**

> Os números abaixo foram calculados nos arquivos reais enviados pela equipe (IDEB 2023 e Censo Escolar 2023). O script que os gera é `codigos/analise_resp4.py` e o resultado completo está em `codigos/resultado_resp4.txt`. **Pendente:** a conferência com o arquivo de municípios do IBGE (ver seção 3).

---

## 1. Texto pronto para o README: "Análise preliminar dos dados"

### Fontes e recorte

| Fonte | Conteúdo | Como foi obtida | Arquivo |
|---|---|---|---|
| INEP, IDEB 2023 | IDEB por município, etapa e rede | Download (XLSX), tratado em Python | `dados/organizados/ideb_2023_municipios_organizado.csv` |
| INEP, Censo Escolar 2023 | Infraestrutura das escolas | Download (CSV de microdados) | `dados/organizados/censo_escolar_2023_publicas.csv` |
| IBGE, PIB dos municípios | PIB (disponível até 2023) | API do IBGE | `[arquivo da pessoa 3]` |
| IBGE, população | Censo 2022 (não existe população de 2023 na tabela do IBGE) | API do IBGE | `[arquivo da pessoa 3]` |

**Recorte:** ano 2023; escolas públicas em atividade (137.914 de 217.625 escolas do Censo); IDEB das três etapas (anos iniciais, anos finais e ensino médio).

**Ano de referência:** IDEB 2023, Censo Escolar 2023 e PIB 2023 existem, então o ano é 2023. O plano B (2021, ano da pandemia) **não é necessário**. A única exceção é a população, que será do Censo 2022 (1 ano antes). Isso deve constar como limitação.

### Problemas encontrados nos dados

| # | Fonte | Problema | Quantidade | Tratamento |
|---|---|---|---|---|
| 1 | IDEB | IDEB sem valor (`-` na planilha original) | 6.343 de 40.682 linhas (15,6%): 2.642 nos anos iniciais, 2.263 nos finais, 1.438 no ensino médio | Convertido para nulo |
| 2 | IDEB | Notas de Matemática e Português com `ND` ou `--` | 149 (anos iniciais), 456 (finais) e 1.167 (ensino médio), em cada nota | Convertido para nulo |
| 3 | IDEB | A rede `Pública` é o **total** de Estadual + Municipal + Federal do município | 16.700 linhas (41% do arquivo) | Não somar as redes; escolher uma por análise |
| 4 | IDEB | Cobertura muito desigual por etapa e rede | Anos iniciais estaduais: 34,2% com IDEB; ensino médio municipal: 38,5% (só 104 linhas); ensino médio federal: 28,0% | Escolher etapa e rede com boa cobertura (ver seção 2) |
| 5 | IDEB | Linhas com nota Saeb mas sem IDEB (falta o indicador de rendimento) | 8 linhas | Manter sem IDEB |
| 6 | IDEB | IDEB igual a 10 (teto da escala) | 2 linhas | Conferir se é valor real |
| 7 | IDEB x Censo | Município no IDEB e fora do Censo | 1: Boa Esperança do Norte (MT, 5101837), com IDEB vazio nas 6 linhas dele | Registrar; conferir com a lista do IBGE |
| 8 | IDEB x Censo | Código do município é texto no IDEB e número no Censo | todas as linhas | Converter para texto de 7 dígitos antes de juntar |
| 9 | Censo | Escolas paralisadas ou extintas, sem dados de infraestrutura (nulos em `IN_*`) | 37.395 escolas (32.083 paralisadas + 5.312 extintas) | Excluídas pelo recorte (só em atividade) |
| 10 | Censo | `IN_BANDA_LARGA` vazio | 15.792 escolas, exatamente as que têm `IN_INTERNET` = 0 | Tratado como "não tem" |
| 11 | Censo | `QT_MAT_BAS` (matrículas) vazio em escolas em atividade | 993 (718 municipais e 275 estaduais) | Confirmar no dicionário do INEP |
| 12 | Censo | Arquivo original muito grande (mais de 400 colunas, 210 MB) | 217.625 escolas | Lidas só 15 colunas |
| 13 | IDEB x Censo | A infraestrutura do Censo cobre **todas as etapas** da escola, mas o IDEB é por etapa | todas as linhas | Registrar como limitação (ver seção 2) |
| 14 | IBGE | População de 2023 não existe na tabela (faltam 2007, 2010, 2022 e 2023) | | Usar o Censo 2022 |

### Conferência da chave de junção (código do município)

- Todos os códigos têm 7 dígitos, nas duas fontes.
- Municípios distintos: IDEB **5.571** | Censo **5.570**.
- Códigos do Censo que não estão no IDEB: **0**.
- Códigos do IDEB que não estão no Censo: **1** (Boa Esperança do Norte, MT).
- **Conclusão:** o IDEB e o Censo se cruzam pelo código do município. Das 40.682 linhas do IDEB, **40.674 (99,98%)** encontraram infraestrutura correspondente no Censo. As 8 que não encontraram são as 6 de Boa Esperança do Norte e 2 do ensino médio federal.
- **Pendente:** conferir com a lista de municípios do IBGE (pessoa 3).

### Entidades preliminares

Região, Estado, Município, Escola, Infraestrutura da escola e Indicador IDEB.
Relações: Região 1:N Estado, Estado 1:N Município, Município 1:N Escola, Escola 1:1 Infraestrutura (por ano), Município 1:N IDEB (por etapa e rede).
O dicionário completo está em `dicionario_de_dados.md`.

## 2. O que os dados permitem (para o grupo escolher o subtema)

Linhas com **IDEB e infraestrutura juntos** (utilizáveis para o cruzamento), por etapa e rede:

| Etapa | Estadual | Municipal | Pública (total) |
|---|---|---|---|
| Anos iniciais | 1.190 | **5.241** | **5.430** |
| Anos finais | 3.554 | 3.195 | **5.382** |
| Ensino médio | **5.063** | 40 | **5.065** |

- Os melhores recortes são **anos iniciais municipal**, **anos finais (rede pública total)** e **ensino médio estadual**.
- Evitem ensino médio municipal e federal (poucas linhas) e anos iniciais estaduais (34% de cobertura).
- **Limitação:** a infraestrutura é calculada sobre todas as escolas públicas da rede no município, não só as que oferecem a etapa analisada. Para ficar mais preciso, a pessoa 2 pode incluir no recorte as colunas de etapa do Censo (por exemplo `IN_COMUM_FUND_AI`, `IN_COMUM_FUND_AF` e `IN_COMUM_MED`, *confirmar os nomes no dicionário do INEP*).
- A renda (PIB e população) entra quando a pessoa 3 enviar os arquivos.

## 3. Pendências

- [ ] Arquivo de municípios do IBGE (pessoa 3) para a conferência final dos códigos: `python codigos/analise_resp4.py arquivo_ibge.json id`
- [ ] Arquivos de PIB 2023 e população (Censo 2022) da pessoa 3, com a tabela e as variáveis da SIDRA usadas
- [ ] Perguntar ao professor se pode misturar população do Censo 2022 com PIB de 2023
- [ ] Pessoa 1: o `explorar_ideb_2023.py` não tem o **link público da conversa com a IA** no cabeçalho (o Censo tem). O professor exige isso.
- [ ] Confirmar `VL_NOTA_MEDIA_2023` e `QT_MAT_BAS` no dicionário/nota técnica do INEP

## 4. Para o slide (bloco 2, Análise preliminar)

- **Problemas:** 15,6% das linhas do IDEB sem valor; rede "Pública" é o total das outras (não somar); infraestrutura vazia só em escolas paralisadas ou extintas; população de 2023 inexistente no IBGE (usar Censo 2022).
- **Cruzamento IDEB x Censo:** 99,98% das linhas do IDEB têm infraestrutura correspondente (5.570 municípios em comum).
- **Entidades:** Região, Estado, Município, Escola, Infraestrutura, IDEB.

## 5. Para o README: divisão de responsabilidades e uso de IA

| Pessoa | Responsabilidade | Status |
|---|---|---|
| 1 | IDEB (INEP) | feito |
| 2 | Censo Escolar (INEP) | feito |
| 3 | IBGE (API, PIB e população) | PIB ok; população e municípios pendentes |
| 4 | Dicionário, problemas, entidades e conferência de códigos | feito, falta a conferência com o IBGE |
| 5 | Slide, README, GitHub, reuniões e Classroom | em andamento |

> O script `codigos/analise_resp4.py` e o dicionário de dados foram elaborados com ajuda de IA (Claude, da Anthropic) e revisados pela equipe. Link público da conversa: `[colar o link]`.

## 6. Onde colocar cada arquivo no repositório

- `codigos/analise_resp4.py`, `codigos/resultado_resp4.txt`
- `dados/organizados/ideb_infra_municipio_2023.csv` (junto com os dois CSVs que a equipe já tem)
- `dicionario_de_dados.md` e este arquivo, na raiz ou em `docs/`
