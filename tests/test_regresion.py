"""Pruebas de regresion sobre el enrutador, antes y despues de la correccion."""

import pytest

from smars_mini.antes import router as antes
from smars_mini.antes.cluster import Cluster as ClusterAntes
from smars_mini.despues import router as despues
from smars_mini.despues.cluster import Cluster as ClusterDespues

NODOS = 8
ORDENES = 8
CANTIDAD = 500
HIJAS_ESPERADAS = ORDENES * (CANTIDAD // 100)


# --------------------------------------------------------------- ANTES
@pytest.mark.antes
def test_una_orden_genera_solo_las_hijas_necesarias_antes():
    enrutador = antes.Enrutador("nodo-8")
    enrutador.enrutar("KCG", CANTIDAD)
    assert len(enrutador.enviadas) == CANTIDAD // 100


@pytest.mark.antes
def test_cluster_con_un_nodo_sin_actualizar_antes():
    nodos = [despues.Enrutador("nodo-%d" % i) for i in range(1, NODOS)]
    nodos.append(antes.Enrutador("nodo-8"))
    cluster = ClusterAntes(nodos)
    for _ in range(ORDENES):
        cluster.enrutar("KCG", CANTIDAD)
    assert cluster.ordenes_hijas == HIJAS_ESPERADAS


@pytest.mark.antes
def test_no_queda_funcionalidad_obsoleta_expuesta_antes():
    assert not hasattr(antes.Enrutador, "_power_peg")
    assert not hasattr(antes, "calcular_prima_legacy")


# -------------------------------------------------------------- DESPUES
@pytest.mark.despues
def test_una_orden_genera_solo_las_hijas_necesarias_despues():
    enrutador = despues.Enrutador("nodo-8")
    enrutador.enrutar("KCG", CANTIDAD)
    assert len(enrutador.enviadas) == CANTIDAD // 100


@pytest.mark.despues
def test_cluster_homogeneo_respeta_la_cantidad_pedida_despues():
    nodos = [despues.Enrutador("nodo-%d" % i) for i in range(1, NODOS + 1)]
    cluster = ClusterDespues(nodos)
    for _ in range(ORDENES):
        cluster.enrutar("KCG", CANTIDAD)
    assert cluster.ordenes_hijas == HIJAS_ESPERADAS


@pytest.mark.despues
def test_cluster_rechaza_versiones_mezcladas_despues():
    nodos = [despues.Enrutador("nodo-%d" % i) for i in range(1, NODOS)]
    nodos.append(antes.Enrutador("nodo-8"))
    with pytest.raises(RuntimeError, match="despliegue inconsistente"):
        ClusterDespues(nodos)


@pytest.mark.despues
def test_no_queda_funcionalidad_obsoleta_expuesta_despues():
    assert not hasattr(despues.Enrutador, "_power_peg")
    assert not hasattr(despues, "calcular_prima_legacy")


@pytest.mark.despues
def test_la_credencial_se_lee_del_entorno_despues(monkeypatch):
    monkeypatch.delenv("SMARS_TOKEN", raising=False)
    assert despues.Enrutador("nodo-1").esta_autenticado() is False
    monkeypatch.setenv("SMARS_TOKEN", "token-de-prueba")
    assert despues.Enrutador("nodo-1").esta_autenticado() is True
