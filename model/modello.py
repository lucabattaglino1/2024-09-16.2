
from database.DAO import DAO
import networkx as nx




class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = []
        self._idMapAO = {}

    def getRangeCoordinate(self):
        return DAO.getRangeCoordinate()

    # MODEL
    def getShape(self):
        return DAO.getAllShape()

    def buildGraph(self, lat, lng, shape):
        self._graph.clear()
        self._nodes = DAO.getAllNodes(lat, lng, shape)
        self._idMapAO = {}
        for n in self._nodes:
            self._idMapAO[n.id] = n

        self._graph.add_nodes_from(self._nodes)
        self.addEdges(shape)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def addEdges(self, shape):
        DurateMap = {}
        for id, peso in DAO.getDurate(shape):
            DurateMap[id] = peso

        for n1, n2 in DAO.getCoppie(self._idMapAO):
            v1 = DurateMap.get(n1.id, 0)
            v2 = DurateMap.get(n2.id, 0)
            peso = v1 + v2
            self._graph.add_edge(n1, n2, weight=peso)

    def getNumEdges(self):
        return len(self._graph.edges)

    # stampare i 5 archi di peso maggiore
    def getTopArchi(self):

        archi = []
        for u, v, dati in self._graph.edges(data=True):
            archi.append((u, v, dati["weight"]))

        # Ordina per peso decrescente
        archi.sort(key=lambda x: x[2], reverse=True)
        return archi[:5]

    # stampare i 5 archi di grado maggiore
    def getTopNodi(self):
        nodi = []
        for n in self._graph.nodes:
            nodi.append((n, self._graph.degree(n)))
        nodi.sort(key=lambda x: x[1], reverse=True)
        return nodi[:5]


