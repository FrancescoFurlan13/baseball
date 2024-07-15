import itertools

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.idMap = {}
        self._years = DAO.getYears()
        self._graph = nx.Graph()
        self._edges = []
        self._nodes = []

    def getTeams(self, year):
        self._allTeams = DAO.getTeams(year)

        for t in self._allTeams:
            self.idMap[t.ID] = t
        return self._allTeams

    def build_graph(self, year):
        self._graph.clear()
        if len(self._allTeams) == 0:
            print("Lista squadre vuota.")
            return

        self._graph.add_nodes_from(self._allTeams)

        myedges = list(itertools.combinations(self._allTeams, 2))

        self._graph.add_edges_from(myedges)

        # aggiungere i pesi qui!
        salariesOfTeams = DAO.getTeamsSalary(self.idMap, year)
        for e in self._graph.edges:
            self._graph[e[0]][e[1]]["weight"] = salariesOfTeams[e[0]] + salariesOfTeams[e[1]]


    def getDettagli(self, v0):
        vicini = self._graph.neighbors(v0)
        result = []
        for v in vicini:
            result.append( (v, self._graph[v0][v]["weight"]))

        result.sort(key=lambda x: x[1], reverse=True)  #questo serve per ordinare i
        # vicini in base al peso decrescente
        return result

    @property
    def years(self):
        return self._years
