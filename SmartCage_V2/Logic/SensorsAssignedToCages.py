import json
from Lista import Lista


class SensorsAssignedToCages(Lista):
    def __init__(self, SensorAssignedID=None, SensorID=None, NumberSensor=None, UserID=None, CageID=None):
        super().__init__()
        if SensorAssignedID is not None and SensorID is not None and NumberSensor is not None and UserID is not None and CageID is not None:
            self.SensorAssignedID = SensorAssignedID # 1, 2
            self.SensorID = SensorID # 1 (US), 2 (TM), 1 (US)
            self.NumberSensor = NumberSensor # 1, 1, 2
            self.UserID = UserID # 1, 1
            self.CageID = CageID # 1, 1
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
                'SensorAssignedID': self.SensorAssignedID,
                'SensorID': self.SensorID,
                'NumberSensor': self.NumberSensor,
                'UserID': self.UserID,
                'CageID': self.CageID
            }

    def guardar(self, diccionario):
        with open('sensor_assigned.json', 'w', encoding='utf-8') as sensor_assigned_json:
            json.dump(diccionario, sensor_assigned_json, indent=2, ensure_ascii=False)

    def recuperarDatos(self):
        with open('sensor_assigned.json', 'r', encoding='utf-8') as sensor_assigned_json:
            datos = json.load(sensor_assigned_json)
            return datos

    def convertirAObjeto(self, datos):
        self.lista = []
        for sensor_assigned_data in datos:
            sensor_assigned = SensorsAssignedToCages(
                sensor_assigned_data['SensorAssignedID'],
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
        return f"{'SensorAssignedID'.rjust(25)} {'SensorID'.rjust(10)} {'NumberSensor'.rjust(10)} {'UserID'.rjust(10)} {'CageID'.rjust(5)}"

    def __str__(self):
        return f"{str(self.SensorAssignedID).rjust(25)} {str(self.SensorID).rjust(10)} {str(self.NumberSensor).rjust(10)} {str(self.UserID).rjust(10)} {str(self.CageID).rjust(5)}"
