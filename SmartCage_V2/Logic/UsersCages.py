import json
from Lista import Lista


class UsersCages(Lista):
    def __init__(self, UsersCagesID=None, UserID=None, CageID=None):
        super().__init__()
        if UsersCagesID is not None and UserID is not None and CageID is not None:
            self.UsersCagesID = UsersCagesID
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
                'UserCagesID': self.UsersCagesID,
                'UserID': self.UserID,
                'CageID': self.CageID
            }

    def guardar(self, diccionario):
        with open('user_cages.json', 'w', encoding='utf-8') as user_cages_json:
            json.dump(diccionario, user_cages_json, indent=2, ensure_ascii=False)

    def recuperarDatos(self):
        with open('user_cages.json', 'r', encoding='utf-8') as user_cages_json:
            datos = json.load(user_cages_json)
            return datos

    def convertirAObjeto(self, datos):
        self.lista = []
        for user_cages_data in datos:
            user_cage = UsersCages(
                user_cages_data['UserCagesID'],
                user_cages_data['UserID'],
                user_cages_data['CagesID']
            )
            self.create(user_cage)
        return self

    def cargar(self):
        self.convertirAObjeto(self.recuperarDatos())

    def encabezados(self):
        return f"{'UserCageID'.rjust(25)} {'UserID'.rjust(10)} {'CageID'.rjust(5)}"

    def __str__(self):
        return f"{str(self.UsersCagesID).rjust(25)} {str(self.UserID).rjust(10)} {str(self.CageID).rjust(5)}"
