from pathlib import Path

from src.scraper import parse_products

HTML = (Path(__file__).parent / "fixtures" / "catalogo.html").read_text(encoding="utf-8")


def test_extrae_todos_los_items_del_itemlist():
    assert len(parse_products(HTML)) == 4


def test_url_relativa_se_completa_con_base():
    libros = parse_products(HTML, base_url="https://www.panamericana.com.co")
    assert libros[0]["URL"] == "https://www.panamericana.com.co/libro-uno/p"


def test_url_absoluta_se_conserva():
    assert parse_products(HTML)[1]["URL"].startswith("https://www.panamericana")


def test_precio_prioriza_highprice():
    assert parse_products(HTML)[0]["Valor"] == 45000


def test_json_invalido_se_ignora_sin_error():
    assert parse_products("<script type='application/ld+json'>{mal</script>") == []


def test_html_sin_scripts_devuelve_lista_vacia():
    assert parse_products("<html></html>") == []
