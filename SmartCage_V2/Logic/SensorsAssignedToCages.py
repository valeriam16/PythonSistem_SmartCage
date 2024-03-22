import json
from Logic.Lista import Lista


class SensorsAssignedToCages(Lista):
    def __init__(self, ID=None, SensorID=None, NumberSensor=None, UserID=None, CageID=None):
        super().__init__()
        if ID is not None and SensorID is not None and NumberSensor is not None and UserID is not None and CageID is not None:
            self.ID = ID
            self.SensorID = SensorID
            self.NumberSensor = NumberSensor
            self.UserID = UserID
            self.CageID = CageID
            self.lista = []

    def diccionario(self):
        if self.lista:
            datos = [
                sensorAssigned.diccionario()
                for sensorAssigned in self.lista
            ]
            return datos
        else:
            return {
                'ID': int(self.ID),
                'SensorID': int(self.SensorID),
                'NumberSensor': int(self.NumberSensor),
                'UserID': int(self.UserID),
                'CageID': int(self.CageID)
            }

    def guardar(self, diccionario):
        with open('../JSON/SensorsAssignedToCages.json', 'w', encoding='utf-8') as sensor_assigned_json:
            json.dump(diccionario, sensor_assigned_json, indent=2, ensure_ascii=False)

    def recuperarDatos(self):
        with open('../JSON/SensorsAssignedToCages.json', 'r', encoding='utf-8') as sensor_assigned_json:
            datos = json.load(sensor_assigned_json)
            return datos

    def convertirAObjeto(self, datos):
        self.lista = []
        for sensor_assigned_data in datos:
            sensor_assigned = SensorsAssignedToCages(
                sensor_assigned_data['ID'],
                sensor_assigned_data['SensorID'],
                sensor_assigned_data['NumberSensor'],
                sensor_assigned_data['UserID'],
                sensor_assigned_data['CageID']
            )
            self.create(sensor_assigned)
        return self

    def cargar(self):
        self.convertirAObjeto(self.recuperarDatos())

    def encabezados(self):
        return f"{'ID'.rjust(1)} {'SensorID'.rjust(12)} {'NumberSensor'.rjust(16)} {'UserID'.rjust(10)} {'CageID'.rjust(10)}"

    def __str__(self):
        return f"{str(self.ID).rjust(1)} {str(self.SensorID).rjust(9)} {str(self.NumberSensor).rjust(14)} {str(self.UserID).rjust(14)} {str(self.CageID).rjust(10)}"
