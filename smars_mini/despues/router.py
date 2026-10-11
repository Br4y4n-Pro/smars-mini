"""Enrutador de ordenes, version corregida y sin funcionalidad obsoleta."""

from smars_mini.despues.config import FLAG_RUTA_MINORISTA, LOTE_MAXIMO, token_operacion


class Enrutador:
    """Divide una orden en ordenes hijas y las envia al mercado."""

    def __init__(self, nodo):
        self.nodo = nodo
        self.enviadas = []
        self.token = token_operacion()

    def esta_autenticado(self):
        """La credencial proviene del entorno de ejecucion."""
        return bool(self.token)

    def enrutar(self, simbolo, cantidad):
        """Envia la orden por la ruta minorista."""
        if not FLAG_RUTA_MINORISTA:
            raise RuntimeError("la ruta minorista esta desactivada en este nodo")
        return self._enrutar_minorista(simbolo, cantidad)

    def _enrutar_minorista(self, simbolo, cantidad):
        """Acumula lo ejecutado y se detiene al completar la cantidad pedida."""
        acumulado = 0
        while acumulado < cantidad:
            lote = min(LOTE_MAXIMO, cantidad - acumulado)
            self.enviadas.append((simbolo, lote))
            acumulado += lote
        return acumulado
