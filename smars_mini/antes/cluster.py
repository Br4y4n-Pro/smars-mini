"""Conjunto de ocho servidores sobre los que se despliega el enrutador."""


class Cluster:
    """Reparte cada orden entrante entre los nodos, por turno rotativo."""

    def __init__(self, nodos):
        self.nodos = nodos
        self._turno = 0

    def enrutar(self, simbolo, cantidad):
        nodo = self.nodos[self._turno % len(self.nodos)]
        self._turno += 1
        nodo.enrutar(simbolo, cantidad)
        return nodo

    @property
    def ordenes_hijas(self):
        return sum(len(n.enviadas) for n in self.nodos)
