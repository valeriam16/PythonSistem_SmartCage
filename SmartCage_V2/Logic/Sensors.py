import json
from Logic.Lista import Lista


class Sensors(Lista):
    def __init__(self, SensorID=None, Type=None, Name=None, Unit=None, Description=None):
        super().__init__()
        if SensorID is not None and Type is not None and Name is not None and Unit is not None and Description is not None:
            self.SensorID = SensorID
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
                'SensorID': self.SensorID,
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
                sensor_data['SensorID'],
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
        return f"{'SensorID'.rjust(25)} \t\t\t {'Type'.rjust(25)} \t\t\t {'Name'.rjust(13)}\t\t {'Unit'.rjust(2)} \t\t\t {'Description'.rjust(25)}"

    def __str__(self):
        return f"{self.SensorID.rjust(30)} \t\t\t  {self.Type.rjust(30)} \t\t\t  {self.Name.rjust(5)}\t\t\t {self.Unit.rjust(5)} \t\t\t {self.Description.rjust(30)} \t\t\t"
