"""Configuracion del enrutador, version corregida."""

import os

# Identificador propio de la funcionalidad nueva: no se reutiliza ninguno.
FLAG_RUTA_MINORISTA = True

LOTE_MAXIMO = 100


def token_operacion():
    """La credencial se lee del entorno, no viaja en el codigo fuente."""
    return os.environ.get("SMARS_TOKEN", "")
