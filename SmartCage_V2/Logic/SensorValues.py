import json
from Logic.Lista import Lista


class SensorValues(Lista):
    def __init__(self, ID=None, SensorAssignedToCageID=None, Value=None):
        super().__init__()
        if ID is not None and SensorAssignedToCageID is not None and Value is not None:
            self.ID = ID
            self.SensorAssignedToCageID = SensorAssignedToCageID
            self.Value = Value
            self.lista = []

    def diccionario(self):
        if self.lista:
            datos = [
                values.diccionario()
                for values in self.lista
            ]
            return datos
        else:
            return {
                'ID': int(self.ID),
                'SensorAssignedToCageID': int(self.SensorAssignedToCageID),
                'Value': float(self.Value)
            }

    def guardar(self, diccionario):
        with open('../JSON/SensorValues.json', 'w', encoding='utf-8') as sensor_values_json:
            json.dump(diccionario, sensor_values_json, indent=2, ensure_ascii=False)

    def recuperarDatos(self):
        with open('../JSON/SensorValues.json', 'r', encoding='utf-8') as sensor_values_json:
            datos = json.load(sensor_values_json)
            return datos

    def convertirAObjeto(self, datos):
        self.lista = []
        for sensor_value_data in datos:
            sensor_value = SensorValues(
                sensor_value_data['ID'],
                sensor_value_data['SensorAssignedToCageID'],
                sensor_value_data['Value']
            )
            self.create(sensor_value)
        return self

    def cargar(self):
        self.convertirAObjeto(self.recuperarDatos())

    def encabezados(self):
        return f"{'ID'.rjust(1)} {'SensorAssignedToCageID'.rjust(25)} {'Value'.rjust(10)}"

    def __str__(self):
        return f"{str(self.ID).rjust(1)} {str(self.SensorAssignedToCageID).rjust(15)} {str(self.Value).rjust(20)}"
