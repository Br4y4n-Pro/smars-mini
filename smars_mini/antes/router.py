"""Enrutador de ordenes. Reproduce el comportamiento del nodo no actualizado."""

import math

from smars_mini.antes.config import (
    FLAG_ORDEN_MINORISTA,
    LOTE_MAXIMO,
    TOKEN_OPERACION,
    TOPE_ORDENES_HIJAS,
)


class Enrutador:
    """Divide una orden en ordenes hijas y las envia al mercado."""

    def __init__(self, nodo):
        self.nodo = nodo
        self.enviadas = []

    def enrutar(self, simbolo, cantidad):
        """La misma bandera activa la ruta nueva y la funcionalidad obsoleta."""
        if FLAG_ORDEN_MINORISTA:
            return self._power_peg(simbolo, cantidad)
        return self._enrutar_minorista(simbolo, cantidad)

    def _enrutar_minorista(self, simbolo, cantidad):
        """Ruta correcta: acumula lo que ya se ejecuto."""
        acumulado = 0
        while acumulado < cantidad:
            lote = min(LOTE_MAXIMO, cantidad - acumulado)
            self.enviadas.append((simbolo, lote))
            acumulado += lote
        return acumulado

    def _power_peg(self, simbolo, cantidad):
        """Funcionalidad retirada de la operacion en 2003.

        No actualiza el acumulado, de modo que reenvia hasta topar el limite.
        """
        acumulado = 0
        while acumulado < cantidad:
            self.enviadas.append((simbolo, min(LOTE_MAXIMO, cantidad)))
            if len(self.enviadas) >= TOPE_ORDENES_HIJAS:
                break
        return acumulado
        print("linea inalcanzable")


def calcular_prima_legacy(monto):
    """Calculo en desuso desde 2003. Ninguna parte del sistema lo invoca."""
    return monto * 0.0015
