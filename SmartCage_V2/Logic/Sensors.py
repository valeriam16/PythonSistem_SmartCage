import json
from Logic.Lista import Lista


class Sensors(Lista):
    def __init__(self, ID=None, Type=None, Name=None, Unit=None, Description=None):
        super().__init__()
        if ID is not None and Type is not None and Name is not None and Unit is not None and Description is not None:
            self.ID = ID
            self.Type = Type # Ultrasónico
            self.Name = Name # US
            self.Unit = Unit # cm
            self.Description = Description # Sensor que detectará si la puerta de la jaula está abierta o cerrada
            self.lista = []

    def diccionario(self):
        if self.lista:
            datos = [
                sensor.diccionario()
                for sensor in self.lista
            ]
            return datos
        else:
            return {
                'ID': int(self.ID),
                'Type': self.Type,
                'Name': self.Name,
                'Unit': self.Unit,
                'Description': self.Description
            }

    def guardar(self, diccionario):
        with open('../JSON/Sensors.json', 'w', encoding='utf-8') as sensores_json:
            json.dump(diccionario, sensores_json, indent=2, ensure_ascii=False)

    def recuperarDatos(self):
        with open('../JSON/Sensors.json', 'r', encoding='utf-8') as sensores_json:
            datos = json.load(sensores_json)
            return datos

    def convertirAObjeto(self, datos):
        self.lista = []
        for sensor_data in datos:
            sensor = Sensors(
                sensor_data['ID'],
                sensor_data['Type'],
                sensor_data['Name'],
                sensor_data['Unit'],
                sensor_data['Description']
            )
            self.create(sensor)
        return self

    def cargar(self):
        self.convertirAObjeto(self.recuperarDatos())

    def encabezados(self):
        return f"{'ID'.rjust(1)} \t\t\t {'Type'.rjust(5)} \t\t\t {'Name'.rjust(13)}\t\t {'Unit'.rjust(8)} \t\t\t {'Description'.rjust(5)}"

    def __str__(self):
        return f"{str(self.ID).rjust(1)} \t\t\t  {self.Type.rjust(10)} \t\t\t  {self.Name.rjust(1)}\t\t\t {self.Unit.rjust(1)} \t\t\t {self.Description.rjust(10)} \t\t\t"
