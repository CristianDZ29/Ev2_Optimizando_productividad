"""Limpieza y validación básica de los datos extraídos."""
import pandas as pd

COLUMNAS = ["Código", "Nombre", "Valor", "URL"]


def clean(libros):
    """Devuelve un DataFrame limpio: sin duplicados, sin vacíos, precio numérico."""
    df = pd.DataFrame(libros, columns=COLUMNAS)
    df = df.dropna(subset=["Nombre", "Valor"])
    df = df[df["Nombre"].astype(str).str.strip() != ""]
    df["Nombre"] = df["Nombre"].astype(str).str.strip()
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")
    df = df.dropna(subset=["Valor"])
    df = df[df["Valor"] > 0]
    df = df.drop_duplicates(subset=["Nombre"]).reset_index(drop=True)
    return df


def validate(df):
    """Lanza ValueError si el DataFrame no cumple las reglas de integridad."""
    if df.empty:
        raise ValueError("El DataFrame está vacío: la extracción no devolvió datos.")
    faltantes = [c for c in COLUMNAS if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas: {faltantes}")
    if df["Nombre"].duplicated().any():
        raise ValueError("Existen títulos duplicados.")
    if (df["Valor"] <= 0).any() or df["Valor"].isna().any():
        raise ValueError("Existen precios nulos o no positivos.")
    if not df["URL"].astype(str).str.startswith("http").all():
        raise ValueError("Existen URL inválidas.")
    return True
#prueba kevin
