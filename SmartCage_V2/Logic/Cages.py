import json
from Lista import Lista


class Cages(Lista):
    def __init__(self, CageID=None):
        super().__init__()
        if CageID is not None:
            self.CageID = CageID
            self.lista = []

    def diccionario(self):
        if self.lista:
            datos = [
                cage.diccionario()
                for cage in self.lista
            ]
            return datos
        else:
            return {
                'CageID': self.CageID
            }

    def guardar(self, diccionario):
        with open('Cages.json', 'w', encoding='utf-8') as cages_json:
            json.dump(diccionario, cages_json, indent=2, ensure_ascii=False)

    def recuperarDatos(self):
        with open('Cages.json', 'r', encoding='utf-8') as cages_json:
            datos = json.load(cages_json)
            return datos

    def convertirAObjeto(self, datos):
        self.lista = []
        for cage_data in datos:
            cage = Cages(
                cage_data['CageID']
            )
            self.create(cage)
        return self

    def cargar(self):
        self.convertirAObjeto(self.recuperarDatos())

    def encabezados(self):
        return f"{'CageID'.rjust(1)}"

    def __str__(self):
        return f'{str(self.CageID).rjust(20)}'
