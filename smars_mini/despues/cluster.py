"""Conjunto de servidores con verificacion de la version desplegada."""


class Cluster:
    """Reparte cada orden entre los nodos y verifica que todos sean iguales."""

    def __init__(self, nodos):
        self.nodos = nodos
        self._turno = 0
        self.verificar_despliegue()

    def verificar_despliegue(self):
        """Control ausente en 2012: exige una unica version en todo el conjunto."""
        versiones = {type(n).__module__ for n in self.nodos}
        if len(versiones) > 1:
            raise RuntimeError(
                f"despliegue inconsistente, versiones encontradas: {sorted(versiones)}"
            )

    def enrutar(self, simbolo, cantidad):
        """Entrega la orden al siguiente nodo del turno."""
        nodo = self.nodos[self._turno % len(self.nodos)]
        self._turno += 1
        nodo.enrutar(simbolo, cantidad)
        return nodo

    @property
    def ordenes_hijas(self):
        """Total de ordenes hijas emitidas por el conjunto."""
        return sum(len(n.enviadas) for n in self.nodos)
