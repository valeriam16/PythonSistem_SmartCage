import json
from Lista import Lista


class SensorValues(Lista):
    def __init__(self, ValueID=None, SensorID=None, Value=None):
        super().__init__()
        if ValueID is not None and SensorID is not None and Value is not None:
            self.ValueID = ValueID
            self.SensorID = SensorID
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
                'ValueID': self.ValueID,
                'SensorID': self.SensorID,
                'Value': self.Value
            }

    def guardar(self, diccionario):
        with open('SensorValues.json', 'w', encoding='utf-8') as sensor_values_json:
            json.dump(diccionario, sensor_values_json, indent=2, ensure_ascii=False)

    def recuperarDatos(self):
        with open('SensorValues.json', 'r', encoding='utf-8') as sensor_values_json:
            datos = json.load(sensor_values_json)
            return datos

    def convertirAObjeto(self, datos):
        self.lista = []
        for sensor_value_data in datos:
            sensor_value = SensorValues(
                sensor_value_data['ValueID'],
                sensor_value_data['SensorID'],
                sensor_value_data['Value']
            )
            self.create(sensor_value)
        return self

    def cargar(self):
        self.convertirAObjeto(self.recuperarDatos())

    def encabezados(self):
        return f"{'ValueID'.rjust(25)} {'SensorID'.rjust(10)} {'Value'.rjust(5)}"

    def __str__(self):
        return f"{str(self.ValueID).rjust(25)} {str(self.SensorID).rjust(10)} {str(self.Value).rjust(5)}"
