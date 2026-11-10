"""Extracción (web scraping) de los libros más vendidos de Librería Panamericana.

Los datos se leen de los bloques JSON-LD (<script type="application/ld+json">)
incrustados en el HTML, igual que en la Evidencia de aprendizaje 1.
"""
import json
import os
import time

import requests
from bs4 import BeautifulSoup

BASE_URL = os.getenv("BASE_URL", "https://www.panamericana.com.co")
CATEGORY_URL = os.getenv(
    "CATEGORY_URL",
    BASE_URL + "/13331?map=productClusterIds&order=OrderByTopSaleDESC",
)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}
NO_DISPONIBLE = "No disponible"


def parse_products(html, base_url=BASE_URL):
    """Convierte el HTML de una página de catálogo en una lista de diccionarios."""
    soup = BeautifulSoup(html, "html.parser")
    libros = []
    for script in soup.find_all("script", type="application/ld+json"):
        contenido = script.get_text(strip=True)
        if not contenido:
            continue
        try:
            datos = json.loads(contenido)
        except json.JSONDecodeError:
            continue
        if not isinstance(datos, dict):
            continue
        if datos.get("@type") != "ItemList" or "itemListElement" not in datos:
            continue
        for wrapper in datos["itemListElement"]:
            producto = wrapper.get("item", {})
            if not producto:
                continue
            url = producto.get("@id") or producto.get("url") or NO_DISPONIBLE
            if url != NO_DISPONIBLE and not url.startswith("http"):
                url = base_url + url
            ofertas = producto.get("offers", {})
            precio = None
            if isinstance(ofertas, dict):
                precio = (
                    ofertas.get("highPrice")
                    or ofertas.get("lowPrice")
                    or ofertas.get("price")
                )
            libros.append(
                {
                    "Código": producto.get("sku", producto.get("id", NO_DISPONIBLE)),
                    "Nombre": producto.get("name", NO_DISPONIBLE),
                    "Valor": precio,
                    "URL": url,
                }
            )
    return libros


def fetch_page(url, session=None, timeout=15):
    """Descarga una página; devuelve None si el servidor no responde 200."""
    getter = session.get if session else requests.get
    respuesta = getter(url, headers=HEADERS, timeout=timeout)
    if respuesta.status_code != 200:
        print(f"Error {respuesta.status_code} en {url}, se omite.")
        return None
    return respuesta.content


def scrape(pages=2, delay=1.0, category_url=CATEGORY_URL):
    """Recorre `pages` páginas del catálogo con una pausa entre solicitudes."""
    libros = []
    for pagina in range(1, pages + 1):
        print(f"Leyendo página {pagina}...")
        html = fetch_page(f"{category_url}&page={pagina}")
        if html:
            libros.extend(parse_products(html))
        time.sleep(delay)
    return libros
# Verificacion de cambio
