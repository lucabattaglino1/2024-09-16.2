import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    # CONTROLLER
    def fillDDShape(self):
        shape = self._model.getShape()
        for s in shape:
            self._view.ddshape.options.append(ft.dropdown.Option(str(s)))
        self._view.update_page()

    def handle_graph(self, e):
        minLat, maxLat, minLng, maxLng = self._model.getRangeCoordinate()

        lat_str = self._view.txt_latitude.value
        lng_str = self._view.txt_longitude.value
        shape = self._view.ddshape.value

        if shape is None:
            self._view.create_alert("Seleziona un anno")
            return

        if lat_str is None or lng_str is None or lat_str == "" or lng_str == "":
            self._view.create_alert("Inserisci entrambi i valori")
            return

        try:
            lat = float(lat_str)
            lng = float(lng_str)
        except ValueError:
            self._view.create_alert("I valori devono essere numerici")
            return

        if lat < minLat or lat > maxLat:
            self._view.create_alert(f"Latitudine fuori range ({minLat} - {maxLat})")
            return

        if lng < minLng or lng > maxLng:
            self._view.create_alert(f"Longitudine fuori range ({minLng} - {maxLng})")
            return

        # valori validi, procedi con la logica successiva
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Coordinate valide: ({lat}, {lng})"))

        self._model.buildGraph(lat, lng, shape)

        # stampo le info
        self._view.txt_result1.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result1.controls.append(
            ft.Text(f"Il grafo ha {self._model.getNumNodes()} nodi e {self._model.getNumEdges()} archi."))

        self._view.txt_result1.controls.append(ft.Text("Archi di peso maggiore:"))
        for a1, a2, peso in self._model.getTopArchi():
            self._view.txt_result1.controls.append(ft.Text(f"{a1.Name} -> {a2.Name} ({peso})"))

        self._view.txt_result1.controls.append(ft.Text("Nodi con grado maggiore:"))
        for nodo, grado in self._model.getTopNodi():
            self._view.txt_result1.controls.append(ft.Text(f"{nodo.Name}: grado {grado}"))

        self._view.update_page()



    def handle_path(self, e):
        pass

    def fill_ddshape(self):
        pass
