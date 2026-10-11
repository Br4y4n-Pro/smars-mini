# smars-mini

Proyecto de prueba para pruebas de calidad hechas en un mini proyecto de Python.

Banco de pruebas construido para el curso de Calidad de Sistemas de Información
(Corporación Universitaria Iberoamericana). Reproduce, a escala reducida, los
defectos que provocaron el incidente de Knight Capital Group del 1 de agosto de
2012, documentado por la Securities and Exchange Commission.

## Estructura

| Carpeta | Contenido |
|---|---|
| `smars_mini/antes/` | Código con los defectos documentados en el caso. |
| `smars_mini/despues/` | El mismo código después de aplicar las correcciones. |
| `tests/` | Pruebas de regresión para ambas versiones. |
| `evidencias/` | Salidas originales de cada herramienta sobre ambas versiones. |

## Defectos reproducidos

1. Una bandera de configuración reutilizada que activa dos funcionalidades distintas.
2. Una funcionalidad obsoleta (`_power_peg`) que quedó en el código y vuelve a ejecutarse.
3. Un despliegue con versiones mezcladas entre los nodos del conjunto.
4. Una credencial escrita directamente en el código fuente.

## Puesta en marcha

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install pytest pytest-cov ruff vulture pylint bandit
```

## Herramientas aplicadas

Los comandos se ejecutan desde la raíz del proyecto.

| Herramienta | Versión | Comando |
|---|---|---|
| Ruff | 0.16.9 | `ruff check smars_mini/antes --output-format concise` |
| Pylint | 4.0.9 | `pylint smars_mini/antes` |
| Vulture | 2.16 | `vulture smars_mini/antes tests --min-confidence 60` |
| Bandit | 1.9.4 | `bandit -r smars_mini/antes` |
| Pytest | 9.1.1 | `pytest -m antes -q` |
| Pytest + Coverage | 9.1.1 | `pytest -m despues -q --cov=smars_mini/despues --cov-report=term-missing` |

Reemplazando `antes` por `despues` se obtienen los resultados de la versión corregida.

## Resultados

| Herramienta | Versión con defectos | Versión corregida |
|---|---|---|
| Ruff | 2 hallazgos | 0 |
| Pylint | 6 hallazgos · 8,57/10 | 0 · 10,00/10 |
| Vulture | 4 hallazgos | 0 |
| Bandit | 1 incidencia (B105) | 0 |
| Pytest | 3 pruebas fallidas | 5 aprobadas · 98 % de cobertura |

La prueba que resume el ejercicio compara las órdenes hijas emitidas contra las
esperadas cuando uno de los ocho nodos quedó sin actualizar:

```
assert cluster.ordenes_hijas == HIJAS_ESPERADAS
E   assert 5035 == 40
```

## Nota sobre la credencial

El valor `TOKEN_OPERACION` en `smars_mini/antes/config.py` es un marcador de
prueba creado a propósito para que Bandit lo detecte. No corresponde a ninguna
credencial real.
