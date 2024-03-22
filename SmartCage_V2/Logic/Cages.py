import json
from Logic.Lista import Lista


class Cages(Lista):
    def __init__(self, ID=None):
        super().__init__()
        if ID is not None:
            self.ID = ID
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
                'ID': int(self.ID)
            }

    def guardar(self, diccionario):
        with open('../JSON/Cages.json', 'w', encoding='utf-8') as cages_json:
            json.dump(diccionario, cages_json, indent=2, ensure_ascii=False)

    def recuperarDatos(self):
        with open('../JSON/Cages.json', 'r', encoding='utf-8') as cages_json:
            datos = json.load(cages_json)
            return datos

    def convertirAObjeto(self, datos):
        self.lista = []
        for cage_data in datos:
            cage = Cages(
                cage_data['ID']
            )
            self.create(cage)
        return self

    def cargar(self):
        self.convertirAObjeto(self.recuperarDatos())

    def encabezados(self):
        return f"{'ID'.rjust(1)}"

    def __str__(self):
        return f'{str(self.ID).rjust(1)}'
