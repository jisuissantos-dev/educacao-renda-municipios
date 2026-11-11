"""
Exploração do IDEB 2023 por município (INEP) - Fase 01, Pessoa 1.
Uso: python explorar_ideb_2023.py <pasta_com_os_xlsx> <pasta_saida>
Obs.: script escrito com apoio de IA (Claude) - informar isso na entrega.
"""
import sys, glob, os
import pandas as pd

pasta, saida = sys.argv[1], sys.argv[2]
os.makedirs(saida, exist_ok=True)

ARQ = {"Anos Iniciais": "*anos_iniciais_municipios*.xlsx",
       "Anos Finais": "*anos_finais_municipios*.xlsx",
       "Ensino Médio": "*ensino_medio_municipios*.xlsx"}

def carregar(caminho):
    # Linhas 0-8 são cabeçalho institucional; a linha 9 tem os nomes técnicos das colunas.
    # dtype=str para não perder zeros nem converter "-" automaticamente.
    df = pd.read_excel(caminho, header=9, dtype=str)
    # Remove notas de rodapé: linhas sem código de município numérico.
    df = df[df["CO_MUNICIPIO"].str.fullmatch(r"\d{7}", na=False)].copy()
    return df

relatorio, tidy = [], []
for etapa, padrao in ARQ.items():
    caminho = glob.glob(os.path.join(pasta, padrao))[0]
    df = carregar(caminho)
    cols23 = [c for c in df.columns if c.endswith("_2023")]
    base = ["SG_UF", "CO_MUNICIPIO", "NO_MUNICIPIO", "REDE"]
    d = df[base + cols23].copy()

    # Valores estranhos: "-" (sem dado), "ND", "--", vazio.
    for c in cols23:
        s = d[c]
        relatorio.append({
            "etapa": etapa, "coluna": c,
            "n_linhas": len(s),
            "traco_'-'": int((s.str.strip() == "-").sum()),
            "ND_ou_'--'": int(s.str.strip().isin(["ND", "--"]).sum()),
            "nulos_reais": int(s.isna().sum()),
        })
        # Converte para número; o que não for número vira NaN.
        d[c] = pd.to_numeric(s.replace({"-": None, "--": None, "ND": None}), errors="coerce")

    # Duplicados na chave (município + rede)
    dup = d.duplicated(["CO_MUNICIPIO", "REDE"]).sum()
    relatorio.append({"etapa": etapa, "coluna": "DUPLICADOS (CO_MUNICIPIO+REDE)", "n_linhas": len(d),
                      "traco_'-'": dup, "ND_ou_'--'": 0, "nulos_reais": 0})
    d.insert(0, "ETAPA", etapa)
    tidy.append(d)

rel = pd.DataFrame(relatorio)
rel.to_csv(os.path.join(saida, "relatorio_qualidade_ideb_2023.csv"), index=False)

# Base organizada: IDEB observado 2023 em formato longo
final = pd.concat(tidy, ignore_index=True)
final.to_csv(os.path.join(saida, "ideb_2023_municipios_organizado.csv"), index=False)

# Cobertura do IDEB 2023 por etapa e rede
cob = (final.assign(tem_ideb=final["VL_OBSERVADO_2023"].notna())
       .groupby(["ETAPA", "REDE"]).agg(linhas=("tem_ideb", "size"), com_ideb=("tem_ideb", "sum"),
                                        municipios=("CO_MUNICIPIO", "nunique")))
cob["pct_com_ideb"] = (cob["com_ideb"] / cob["linhas"] * 100).round(1)
cob.to_csv(os.path.join(saida, "cobertura_ideb_2023.csv"))
print(cob.to_string())
print(rel[rel.coluna.isin(["VL_OBSERVADO_2023", "DUPLICADOS (CO_MUNICIPIO+REDE)"])].to_string())
print("Municípios distintos (código 7 dígitos):", final["CO_MUNICIPIO"].nunique())
print("Faixa do IDEB 2023:", final["VL_OBSERVADO_2023"].min(), "a", final["VL_OBSERVADO_2023"].max())
