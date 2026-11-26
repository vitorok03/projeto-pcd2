"""Baixa camadas do SoilGrids 2.0 (produto agregado de 1 km) recortadas para o Brasil.

Diferenças em relação ao script original:
  - 6 profundidades (0-5, 5-15, 15-30, 30-60, 60-100, 100-200 cm), não só 3
  - propriedades extras: cfvo, nitrogen, ocd, wv0010, wv1500 e ocs (só 0-30 cm)
  - estatísticas escolhidas por --stats: mean, Q05, Q50, Q95 (e uncertainty, se existir)
  - para cada estatística tenta mais de um padrão de nome no servidor (ex.: Q05 e Q0.05)
  - pula o que já foi baixado, tenta de novo em falha de rede e não aborta tudo
    se uma camada não existir (a falha é listada no final)

Uso:
  python baixar_soilgrids_completo.py data/raw/soil                        # tudo, só a média
  python baixar_soilgrids_completo.py data/raw/soil --stats mean Q05 Q50 Q95
  python baixar_soilgrids_completo.py data/raw/soil --props wv0033 wv1500 --profs 0-5cm 5-15cm

A incerteza por pixel pode ser calculada depois: (Q95 - Q05) / Q50 (definição do ISRIC),
então não é preciso baixar a camada "uncertainty".

Nome de saída: {prop}_{prof}_{estatística}.tif (o nome vira a coluna em solo.py).
NÃO TESTADO com acesso real à rede: confira o resumo de falhas no final.
"""
import argparse
import time
from pathlib import Path

import rasterio
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds

BASE = "https://files.isric.org/soilgrids/latest/data_aggregated/1000m"
PROPRIEDADES = ["bdod", "cec", "cfvo", "clay", "nitrogen", "ocd", "phh2o",
                "sand", "silt", "soc", "wv0010", "wv0033", "wv1500", "ocs"]
PROFUNDIDADES = ["0-5cm", "5-15cm", "15-30cm", "30-60cm", "60-100cm", "100-200cm"]
BRASIL_LONLAT = (-74.5, -34.5, -28.0, 6.0)   # (oeste, sul, leste, norte), com folga

# nome local -> nomes que o servidor pode usar (o ISRIC usa Q05 nos arquivos de 250 m)
ESTATISTICAS = {
    "mean": ["mean"],
    "Q05": ["Q0.05", "Q05"],
    "Q50": ["Q0.5", "Q50"],
    "Q95": ["Q0.95", "Q95"],
    "uncertainty": ["uncertainty"],
}


def _nao_existe(msg):
    return "404" in msg or "not recognized as a supported" in msg


def baixar(prop, prof, stat, destino, tentativas=3):
    saida = destino / f"{prop}_{prof}_{stat}.tif"
    if saida.exists():
        return "existe"
    erro = ""
    for nome in ESTATISTICAS.get(stat, [stat]):
        url = f"/vsicurl/{BASE}/{prop}/{prop}_{prof}_{nome}_1000.tif"
        for t in range(1, tentativas + 1):
            try:
                with rasterio.open(url) as src:
                    caixa = transform_bounds("EPSG:4326", src.crs, *BRASIL_LONLAT)
                    janela = from_bounds(*caixa, transform=src.transform).round_offsets().round_lengths()
                    dados = src.read(1, window=janela)
                    perfil = src.profile | dict(
                        driver="GTiff", height=dados.shape[0], width=dados.shape[1],
                        transform=src.window_transform(janela),
                        compress="deflate", tiled=True, blockxsize=512, blockysize=512,
                    )
                tmp = saida.with_name(saida.name + ".tmp")      # evita arquivo pela metade
                with rasterio.open(tmp, "w", **perfil) as dst:
                    dst.write(dados, 1)
                tmp.replace(saida)
                return f"ok via '{nome}' ({dados.shape[1]}x{dados.shape[0]} px)"
            except Exception as e:                               # noqa: BLE001
                msg = str(e)
                erro = msg.splitlines()[0][:120]
                if _nao_existe(msg):                             # tenta o próximo nome possível
                    break
                time.sleep(5 * t)
    return f"falhou: {erro}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("destino", nargs="?", default="data/raw/soil")
    ap.add_argument("--props", nargs="+", default=PROPRIEDADES)
    ap.add_argument("--profs", nargs="+", default=PROFUNDIDADES)
    ap.add_argument("--stats", nargs="+", default=["mean"])
    args = ap.parse_args()

    destino = Path(args.destino)
    destino.mkdir(parents=True, exist_ok=True)
    falhas = []

    with rasterio.Env(GDAL_HTTP_TIMEOUT=120, GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR",
                      GDAL_HTTP_MAX_RETRY=3, GDAL_HTTP_RETRY_DELAY=5):
        for prop in args.props:
            profs = ["0-30cm"] if prop == "ocs" else args.profs   # ocs só existe em 0-30 cm
            for stat in args.stats:
                for prof in profs:
                    resultado = baixar(prop, prof, stat, destino)
                    print(f"{prop}_{prof}_{stat}: {resultado}", flush=True)
                    if resultado.startswith("falhou"):
                        falhas.append(f"{prop}_{prof}_{stat}")

    print(f"\nConcluído. {len(falhas)} falha(s).")
    for f in falhas:
        print("  -", f)


if __name__ == "__main__":
    main()
