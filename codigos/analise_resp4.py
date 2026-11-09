# ======================================================================
# Projeto de Banco de Dados I - Fase 01
# Tema: Educação e renda dos municípios
# Parte: Responsabilidade 4 - conferência entre fontes, problemas e cruzamento
#
# Este código foi feito com ajuda de IA (Claude, da Anthropic) e revisado pela equipe.
# Link público da conversa: [colar aqui o link]
#
# O que faz:
#   1. Confere os códigos de município entre IDEB 2023 e Censo Escolar 2023.
#   2. Levanta problemas do IDEB (rede "Pública" repetida, cobertura, notas vazias).
#   3. Cruza IDEB x infraestrutura por município e rede (Estadual/Municipal/Federal/Pública).
#   4. Salva dados/organizados/ideb_infra_municipio_2023.csv e codigos/resultado_resp4.txt.
#
# Uso (na raiz do projeto):  python codigos/analise_resp4.py [municipios_ibge.csv ou .json] [coluna_codigo]
# O arquivo do IBGE é opcional: se for informado, a conferência de códigos inclui o IBGE.
# ======================================================================
import os, sys, json
import pandas as pd

raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
org = os.path.join(raiz, "dados", "organizados")
pd.set_option("display.width", 160); pd.set_option("display.max_columns", None)

txt = open(os.path.join(raiz, "codigos", "resultado_resp4.txt"), "w", encoding="utf-8")
def mostrar(t=""):
    print(t); txt.write(str(t) + "\n")

# --- Leitura: código do município SEMPRE como texto de 7 dígitos (no Censo ele vem como número) ---
ideb = pd.read_csv(os.path.join(org, "ideb_2023_municipios_organizado.csv"), dtype={"CO_MUNICIPIO": str})
censo = pd.read_csv(os.path.join(org, "censo_escolar_2023_publicas.csv"))
censo["CO_MUNICIPIO"] = censo["CO_MUNICIPIO"].astype(str)

mostrar("RESPONSABILIDADE 4 - CONFERÊNCIA ENTRE FONTES (ano 2023)")

# 1. Códigos de município
mostrar("\n1. CÓDIGOS DE MUNICÍPIO (IDEB x CENSO)")
mi, mc = set(ideb.CO_MUNICIPIO), set(censo.CO_MUNICIPIO)
mostrar(f"Municípios no IDEB: {len(mi)} | no Censo (recorte público): {len(mc)}")
mostrar(f"Códigos com 7 dígitos: IDEB {(ideb.CO_MUNICIPIO.str.len()==7).all()} | Censo {(censo.CO_MUNICIPIO.str.len()==7).all()}")
so_ideb = sorted(mi - mc); so_censo = sorted(mc - mi)
mostrar(f"No IDEB e fora do Censo: {len(so_ideb)} -> " + str(ideb[ideb.CO_MUNICIPIO.isin(so_ideb)][["CO_MUNICIPIO","NO_MUNICIPIO","SG_UF"]].drop_duplicates().values.tolist()))
mostrar(f"No Censo e fora do IDEB: {len(so_censo)}")
if len(sys.argv) >= 2:   # conferência opcional com o IBGE
    arq = sys.argv[1]; col = sys.argv[2] if len(sys.argv) > 2 else "id"
    ib = pd.json_normalize(json.load(open(arq, encoding="utf-8"))) if arq.endswith(".json") else pd.read_csv(arq, dtype=str)
    mb = set(ib[col].astype(str).str.replace(r"\.0$", "", regex=True))
    mostrar(f"IBGE: {len(mb)} municípios | IDEB fora do IBGE: {len(mi-mb)} | Censo fora do IBGE: {len(mc-mb)} | IBGE fora do Censo: {len(mb-mc)}")
else:
    mostrar("(Arquivo do IBGE não informado: conferência com o IBGE pendente.)")

# 2. Problemas do IDEB
mostrar("\n2. PROBLEMAS NO IDEB")
mostrar("Linhas por rede: " + str(ideb.REDE.value_counts().to_dict()))
mostrar("A rede 'Pública' é o TOTAL (estadual + municipal + federal) do município: não somar com as outras.")
cob = (ideb.assign(tem=ideb.VL_OBSERVADO_2023.notna()).groupby(["ETAPA", "REDE"])
       .agg(linhas=("tem", "size"), com_ideb=("tem", "sum")))
cob["pct_com_ideb"] = (cob.com_ideb / cob.linhas * 100).round(1)
mostrar("Cobertura do IDEB observado por etapa e rede:"); mostrar(cob)
mostrar(f"IDEB vazio: {ideb.VL_OBSERVADO_2023.isna().sum()} de {len(ideb)} linhas")
so_nota = ideb[ideb.VL_OBSERVADO_2023.isna() & ideb.VL_NOTA_MEDIA_2023.notna()]
mostrar(f"IDEB vazio mas com nota Saeb: {len(so_nota)} linhas (falta o indicador de rendimento)")
mostrar(f"IDEB igual a 10 (teto da escala): {(ideb.VL_OBSERVADO_2023==10).sum()} linhas")

# 3. Infraestrutura por município e rede (o Censo tem uma linha por escola; o IDEB, por município)
mostrar("\n3. CRUZAMENTO IDEB x INFRAESTRUTURA")
infra = ["IN_BIBLIOTECA", "IN_INTERNET", "IN_BANDA_LARGA", "IN_LABORATORIO_INFORMATICA", "IN_LABORATORIO_CIENCIAS"]
censo["REDE"] = censo.TP_DEPENDENCIA.map({1: "Federal", 2: "Estadual", 3: "Municipal"})
def por_municipio(df, rede):
    # Nulo vira 0 (não tem). Banda larga vazia = escola sem internet (confirmado nos dados).
    a = (df[infra].fillna(0).groupby(df.CO_MUNICIPIO).mean() * 100).round(1).add_prefix("PCT_")
    a["N_ESCOLAS"] = df.groupby("CO_MUNICIPIO").size()
    a["REDE"] = rede
    return a.reset_index()
partes = [por_municipio(g, r) for r, g in censo.groupby("REDE")] + [por_municipio(censo, "Pública")]
infra_mun = pd.concat(partes)
j = ideb.merge(infra_mun, on=["CO_MUNICIPIO", "REDE"], how="left")
j["TEM_INFRA"] = j.N_ESCOLAS.notna()
mostrar("Linhas do IDEB com infraestrutura correspondente no Censo: "
        f"{j.TEM_INFRA.sum()} de {len(j)}")
util = j[j.VL_OBSERVADO_2023.notna() & j.TEM_INFRA]
mostrar("Linhas com IDEB E infraestrutura (utilizáveis), por etapa e rede:")
mostrar(util.groupby(["ETAPA", "REDE"]).size().unstack().fillna(0).astype(int))
j.to_csv(os.path.join(org, "ideb_infra_municipio_2023.csv"), index=False, encoding="utf-8")
mostrar("Arquivo salvo: dados/organizados/ideb_infra_municipio_2023.csv")
txt.close()
