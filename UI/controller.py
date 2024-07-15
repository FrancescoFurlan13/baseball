import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._selectedTeam = None



    def fillDD(self):
        for y in self._model.years:
            self._view.ddAnno.options.append(ft.dropdown.Option(y))

    def handleTeam(self, e):
        self._view._txtOutSquadre.controls.clear()
        teams = self._model.getTeams(self._view.ddAnno.value)
        self._view._txtOutSquadre.controls.append(ft.Text(f"Squadre presenti nell'anno "
                                                          f"{self._view.ddAnno.value}: {len(teams)}"))
        for t in teams:
            self._view._txtOutSquadre.controls.append(ft.Text(f"{t.teamCode} ({t.name})"))
            self._view.ddSquadra.options.append(ft.dropdown.Option(data = t,
                                   text = f"{t.teamCode} ({t.name})", on_click=self.readDDTeams))

        self._view.update_page()





    def handleCreaGrafo(self, e):
        print(f"Debug: year={self._view.ddAnno.value}")  # Aggiungi questa linea per il debug
        self._model.build_graph(self._view.ddAnno.value)
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(ft.Text(f"Creato grafo con {len(self._model._graph.nodes)} nodi"
                                                       f" e {len(self._model._graph.edges)} archi"))

        self._view.update_page()

    def handleDettagli(self, e):
        dettagli = self._model.getDettagli(self._selectedTeam)
        self._view._txt_result.controls.clear()

        self._view._txt_result.controls.append(ft.Text(f"Adiacenti per la squadra {self._selectedTeam}"))
        for d in dettagli:
            self._view._txt_result.controls.append(ft.Text(f"{d[0]} - {d[1]}"))

        self._view.update_page()


    def handlePercorso(self, e):
        pass

    def readDDTeams(self, e):
        if e.control.data is None:
            self._selectedTeam = None
        else:
            self._selectedTeam = e.control.data
        print(f"readDDTeams called -- {self._selectedTeam}" )