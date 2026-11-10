"""Genera el sitio estático (producción simulada) que publica GitHub Pages."""
import argparse
import html
import os

import pandas as pd


def build_site(csv_path, out_dir):
    df = pd.read_csv(csv_path, sep=";", encoding="utf-8-sig")
    os.makedirs(out_dir, exist_ok=True)
    filas = "".join(
        "<tr><td>{}</td><td><a href='{}'>{}</a></td><td>${:,.0f}</td></tr>".format(
            html.escape(str(r["Código"])),
            html.escape(str(r["URL"])),
            html.escape(str(r["Nombre"])),
            r["Valor"],
        )
        for _, r in df.iterrows()
    )
    pagina = (
        "<!doctype html><html lang='es'><meta charset='utf-8'>"
        "<title>Libros más vendidos - Panamericana</title>"
        "<h1>Libros más vendidos (Panamericana)</h1>"
        f"<p>{len(df)} libros. <a href='libros.csv'>Descargar CSV</a></p>"
        "<table border='1' cellpadding='6'><tr><th>Código</th><th>Título</th>"
        f"<th>Precio (COP)</th></tr>{filas}</table></html>"
    )
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina)
    df.to_csv(os.path.join(out_dir, "libros.csv"), index=False,
              encoding="utf-8-sig", sep=";")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--csv", default="data/libros_panamericana.csv")
    p.add_argument("--out", default="site")
    a = p.parse_args()
    build_site(a.csv, a.out)
