"""Punto de entrada: extrae, limpia, valida y guarda el CSV."""
import argparse
import os

from src.cleaning import clean, validate
from src.scraper import scrape


def run(pages, delay, output):
    libros = scrape(pages=pages, delay=delay)
    df = clean(libros)
    validate(df)
    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
    df.to_csv(output, index=False, encoding="utf-8-sig", sep=";")
    print(f"Extracción finalizada. Total de libros: {len(df)} -> {output}")
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pages", type=int, default=int(os.getenv("PAGES", "2")))
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("--output", default="data/libros_panamericana.csv")
    args = parser.parse_args()
    run(args.pages, args.delay, args.output)


#Prueba Cristian