import json
from Logic.Lista import Lista


class UsersCages(Lista):
    def __init__(self, ID=None, UserID=None, CageID=None):
        super().__init__()
        if ID is not None and UserID is not None and CageID is not None:
            self.ID = ID
            self.UserID = UserID
            self.CageID = CageID
            self.lista = []

    def diccionario(self):
        if self.lista:
            datos = [
                userCages.diccionario()
                for userCages in self.lista
            ]
            return datos
        else:
            return {
                'ID': int(self.ID),
                'UserID': int(self.UserID),
                'CageID': int(self.CageID)
            }

    def guardar(self, diccionario):
        with open('../JSON/UsersCages.json', 'w', encoding='utf-8') as user_cages_json:
            json.dump(diccionario, user_cages_json, indent=2, ensure_ascii=False)

    def recuperarDatos(self):
        with open('../JSON/UsersCages.json', 'r', encoding='utf-8') as user_cages_json:
            datos = json.load(user_cages_json)
            return datos

    def convertirAObjeto(self, datos):
        self.lista = []
        for user_cages_data in datos:
            user_cage = UsersCages(
                user_cages_data['ID'],
                user_cages_data['UserID'],
                user_cages_data['CageID']
            )
            self.create(user_cage)
        return self

    def cargar(self):
        self.convertirAObjeto(self.recuperarDatos())

    def encabezados(self):
        return f"{'UserCageID'.rjust(1)} {'UserID'.rjust(10)} {'CageID'.rjust(10)}"

    def __str__(self):
        return f"{str(self.ID).rjust(5)} {str(self.UserID).rjust(12)} {str(self.CageID).rjust(10)}"

