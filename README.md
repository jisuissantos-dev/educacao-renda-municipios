# Projeto de Banco de Dados - Educação e renda dos municípios

Disciplina: Banco de Dados I | Prof.: Pedro Paz | Fase 01 | Ano de referência: 2023

Equipe: Maria de Jesus, Ravi, Felipe, Gabriel Alves, Mayke

## 1. Tema e subtema

**Tema:** Educação e renda dos municípios.

**Subtema:** Infraestrutura escolar x desempenho (IDEB).

**Pergunta central:** escolas com mais infraestrutura têm melhor IDEB, mesmo em municípios com menos renda?

## 2. Fluxo do trabalho executado

0. **Storytelling:** escolas bem equipadas costumam ter melhores resultados. Mas isso vale mesmo em municípios com menos renda? Queremos descobrir se a infraestrutura escolar acompanha o desempenho no IDEB.
1. **Fontes:** IDEB 2023 e Censo Escolar 2023 (INEP); PIB 2023 e população do Censo 2022 (IBGE). A chave para juntar tudo é o código do município, com 7 dígitos.
2. **Análise preliminar:** colunas, tipos, valores vazios, duplicados, valores estranhos e conferência dos códigos de município. Os problemas e as entidades estão no arquivo [dicionario_de_dados.md](dicionario_de_dados.md).
3. **Subtema:** escolhido o subtema 1 (infraestrutura escolar x desempenho), porque usa as duas bases que já temos (IDEB e Censo Escolar) e cruza estrutura, desempenho e renda. As outras opções eram: (2) municípios que fogem do padrão e (3) desigualdade entre escolas do mesmo município.

### Principais números da análise preliminar

- **IDEB 2023:** 40.682 linhas, das quais 6.343 (15,6%) sem valor.
- **Censo Escolar 2023:** 217.625 escolas em 5.570 municípios. O recorte usado é de escolas públicas em atividade: 137.914 escolas.
- **Cruzamento IDEB x Censo:** 40.674 das 40.682 linhas do IDEB (99,98%) têm infraestrutura correspondente.
- **Linhas sem infraestrutura (8):** 6 de Boa Esperança do Norte (MT), município novo, instalado em 2025 e por isso fora do Censo 2023, e 2 de ensino médio federal (Pontão, RS, e Campo Verde, MT).
- **Origem dos vazios de infraestrutura:** vêm das 37.395 escolas paralisadas ou extintas, que não respondem essa parte do Censo. Entre as 180.230 escolas em atividade, nenhuma tem biblioteca vazia.
- **Infraestrutura por região (escolas públicas em atividade):** internet em 63,4% das escolas do Norte e 98,8% das do Sul; biblioteca em 19,5% e 55,1%; laboratório de ciências em 5,2% e 19,6%.

## 3. Divisão de responsabilidades

| Pessoa | Nome | Responsabilidade |
|---|---|---|
| 1 | Ravi | IDEB (INEP) |
| 2 | Gabriel Alves | Censo Escolar (INEP) |
| 3 | Felipe | IBGE (API, PIB e população) |
| 4 | Mayke | Dicionário, problemas e conferência de códigos |
| 5 | Maria de Jesus Silva dos Santos | Slide, README, GitHub e Classroom |

## 4. Relatório das reuniões

A equipe não fez reuniões presenciais. O trabalho foi combinado por conversas no grupo de WhatsApp, nos dias abaixo. Nessas conversas foram escolhidos o tema e o subtema, divididas as tarefas entre as 5 pessoas e definido o ano de referência (2023).

| Data | Quem participou |
|---|---|
| 28/10 | Equipe (grupo de WhatsApp) |
| 29/10 | Equipe (grupo de WhatsApp) |
| 31/10 | Equipe (grupo de WhatsApp) |
| 01/11 | Equipe (grupo de WhatsApp) |
| 04/11 | Equipe (grupo de WhatsApp) |
| 06/11 | Equipe (grupo de WhatsApp) |
| 07/11 | Equipe (grupo de WhatsApp) |
| 09/11 | Equipe (grupo de WhatsApp) |
| 10/11 | Equipe (grupo de WhatsApp) |

## 5. Limitações

- População de 2022 (Censo) usada com PIB de 2023, porque o IBGE não tem população de 2023 na tabela usada.
- A rede "Pública" do IDEB é o total das redes estadual, municipal e federal. Para não contar o mesmo município várias vezes, a comparação entre municípios deve usar uma etapa e uma rede (por exemplo, anos iniciais, rede municipal).
- Infraestrutura calculada para todas as escolas da rede, não só da etapa.
- Parte das linhas do IDEB sem valor, e cobertura diferente por etapa e rede.
- Boa Esperança do Norte (MT) tem IDEB, mas não tem Censo 2023.
- No recorte do Censo, 993 escolas têm `QT_MAT_BAS` vazio. O significado ainda precisa ser confirmado no dicionário do INEP.
- O INEP só oferece download de arquivos, sem API. Os dados do INEP foram baixados manualmente.

## 6. Uso de IA

Os códigos foram feitos com ajuda de IA: Claude (Anthropic), pelas pessoas 1, 2 e 4, e Gemini (Google), pela pessoa 3. Cada código tem o aviso de uso de IA no começo do arquivo.

Links públicos das conversas:

- Pessoa 1 (Ravi): https://claude.ai/share/3904e71b-da5e-4db7-ae24-465ed95c43ff
- Pessoa 2 (Gabriel): https://claude.ai/share/4d22b9eb-d65e-4051-b71e-a570c3ea2d7e e https://claude.ai/share/849dd1f8-9da4-4213-ba8e-b8cf5ae26ddc
- Pessoa 3 (Felipe): https://gemini.google.com/share/50c034864713?social_preview=true&skid=dba2e784-3362-4839-ab71-3e77498e2eec
- Pessoa 4 (Mayke): https://claude.ai/share/a88c159c-d46c-4053-a9cb-1d2ad63ea564

## 7. Estrutura do repositório

```
README.md
dicionario_de_dados.md
codigos/            códigos de exploração e análise (pessoas 1 a 4)
dados/
  originais/        dados baixados do INEP e do IBGE (o Censo Escolar está compactado em .zip)
  organizados/      dados limpos e cruzados, gerados pelos códigos
slide/              slide da apresentação em PDF
```

O arquivo original do Censo Escolar (`microdados_ed_basica_2023.csv`, cerca de 210 MB) passa do limite de 100 MB do GitHub, por isso fica compactado em `.zip` em `dados/originais/`. Para rodar o código do Censo, descompacte o arquivo na mesma pasta.

## 8. Como rodar os códigos

Os códigos usam Python e a biblioteca pandas. Rode a partir da raiz do repositório e confira, no começo de cada arquivo, as instruções e os parâmetros de cada um:

- `codigos/explorar_ideb_2023.py`: exploração do IDEB 2023 (pessoa 1).
- `codigos/explorar_censo_escolar.py`: exploração do Censo Escolar 2023 (pessoa 2).
- `codigos/analise_resp4.py`: conferência dos códigos de município e cruzamento do IDEB com o Censo (pessoa 4).
