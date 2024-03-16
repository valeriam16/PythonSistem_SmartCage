import json
from Logic.Lista import Lista


class Users(Lista):
    def __init__(self, ID=None, Name=None, User=None, Email=None, Password=None):
        super().__init__()
        if ID is not None and Name is not None and User is not None and Email is not None and Password is not None:
            self.ID = ID
            self.Name = Name
            self.User = User
            self.Email = Email
            self.Password = Password
            self.lista = []

    def diccionario(self):
        if self.lista:
            datos = [
                user.diccionario()
                for user in self.lista
            ]
            return datos
        else:
            return {
                'ID': self.ID,
                'Name': self.Name,
                'User': self.User,
                'Email': self.Email,
                'Password': self.Password
            }

    def guardar(self, diccionario):
        with open('../JSON/Users.json', 'w', encoding='utf-8') as usuarios_json:
            json.dump(diccionario, usuarios_json, indent=2, ensure_ascii=False)

    def recuperarDatos(self):
        with open('../JSON/Users.json', 'r', encoding='utf-8') as usuarios_json:
            datos = json.load(usuarios_json)
            return datos

    def convertirAObjeto(self, datos):
        self.lista = []
        for user_data in datos:
            user = Users(
                user_data['ID'],
                user_data['Name'],
                user_data['User'],
                user_data['Email'],
                user_data['Password']
            )
            self.create(user)
        return self

    def cargar(self):
        self.convertirAObjeto(self.recuperarDatos())

    def encabezados(self):
        return f"{'ID'.rjust(1)} {'Name'.rjust(15)} {'User'.rjust(30)} {'Email'.rjust(23)} {'Password'.rjust(30)}"

    def __str__(self):
        return f"{str(self.ID).rjust(1)} \t\t\t {self.Name.rjust(20)} {self.User.rjust(21)} {self.Email.rjust(30)} {self.Password.rjust(21)}"
