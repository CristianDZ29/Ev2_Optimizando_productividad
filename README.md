# Scraping Panamericana — Flujo DevOps (EA2)

Proyecto de la asignatura *Programación para Análisis de Datos* (IU Digital).
Extrae los libros más vendidos de Librería Panamericana (código, título, precio y URL),
los limpia, valida y publica en GitHub Pages (producción simulada) con CI/CD.

## Estructura
```
src/        scraper.py (extracción) · cleaning.py (limpieza/validación) · main.py · publish.py
tests/      pruebas unitarias con HTML de ejemplo (sin red)
.github/workflows/ci-cd.yml   pipeline lint → test (matriz) → scrape → deploy
Dockerfile  contenedor de la extracción
docs/       notebook de la EA1
```

## Ejecutar localmente
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python -m src.main --pages 2 --output data/libros_panamericana.csv
python -m src.publish --csv data/libros_panamericana.csv --out site
```

## Pruebas y lint
```bash
flake8 src tests
pytest --cov=src
```

## Docker
```bash
docker build -t scraping-panamericana .
docker run --rm -v "$PWD/data:/app/data" scraping-panamericana
```

## Pipeline (GitHub Actions)
| Job | Cuándo | Qué hace |
|---|---|---|
| lint | push / PR | flake8 (PEP 8) |
| test | push / PR | pytest en Python 3.10, 3.11 y 3.12 en paralelo |
| scrape | solo `main` (push, lunes 12:00 UTC o manual) | extrae, limpia, valida y genera `site/` |
| deploy | tras `scrape` | publica en GitHub Pages, entorno `production` |

Configuración en GitHub: *Settings → Pages → Source: GitHub Actions*; opcional, variable
`PAGES` (*Settings → Variables*) y aprobación manual en *Settings → Environments → production*.

## Flujo de ramas
`main` (estable) ← `develop` ← `feature/scraper`, `feature/limpieza`. Los cambios entran a `main` por pull request con CI en verde.

## Rollback
`git revert <commit>` + push a `main` (el pipeline vuelve a desplegar la versión anterior), o re-ejecutar el workflow sobre un commit previo.
