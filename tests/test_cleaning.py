from pathlib import Path

import pandas as pd
import pytest

from src.cleaning import clean, validate
from src.publish import build_site
from src.scraper import parse_products

HTML = (Path(__file__).parent / "fixtures" / "catalogo.html").read_text(encoding="utf-8")


def test_clean_elimina_duplicados_y_registros_sin_precio():
    df = clean(parse_products(HTML))
    assert list(df["Nombre"]) == ["Libro Uno", "Libro Dos"]


def test_clean_precio_es_numerico():
    assert pd.api.types.is_numeric_dtype(clean(parse_products(HTML))["Valor"])


def test_validate_acepta_datos_limpios():
    assert validate(clean(parse_products(HTML))) is True


def test_validate_rechaza_dataframe_vacio():
    with pytest.raises(ValueError):
        validate(clean([]))


def test_validate_rechaza_precio_no_positivo():
    df = clean(parse_products(HTML))
    df.loc[0, "Valor"] = 0
    with pytest.raises(ValueError):
        validate(df)


def test_build_site_genera_index_y_csv(tmp_path):
    csv = tmp_path / "in.csv"
    clean(parse_products(HTML)).to_csv(csv, index=False, sep=";", encoding="utf-8-sig")
    build_site(str(csv), str(tmp_path / "site"))
    assert (tmp_path / "site" / "index.html").exists()
    assert (tmp_path / "site" / "libros.csv").exists()
