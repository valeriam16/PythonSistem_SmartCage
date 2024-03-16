import os
from Logic.SensorValues import SensorValues
#from Logic.ConexionMongoDB import ConexionMongoDB


class SensorValuesInterface:
    def __init__(self, sensorValues=None):
        #CONEXIÓN A MONGODB
        #self.mongodb_connection = ConexionMongoDB(collection_name='funciones')

        #TRABAJA CON EL JSON, SI SE LA MANDA UNA INSTANCIA
        if sensorValues is not None:
            self.instanciaSensorValues = sensorValues # Si se proporciona una instancia de UserCages, úsala
            self.dataFileSensorValues = SensorValues() # Lista[] que servira para guardar los datos de los UserCages existentes en el JSON

            if os.path.exists("../JSON/SensorValues.json") and os.path.getsize("../JSON/SensorValues.json") > 0:
                self.dataFileSensorValues.cargar() # Aquí guardamos los datos del JSON en la lista[]
            else:
                print("No hay valores tomados de los sensores actualmente.")

            self.instancia = self.dataFileSensorValues
            self.guardarInJson=False
        else:
            # CREA NUEVA ASIGNACIÓN, NO SE LE MANDA UNA INSTANCIA
            self.instanciaSensorValues = SensorValues()

            if os.path.exists("../JSON/SensorValues.json") and os.path.getsize("../JSON/SensorValues.json") > 0:
                self.instanciaSensorValues.cargar()
            else:
                print("No hay valores tomados de los sensores actualmente.")
            self.instancia = self.instanciaSensorValues

            self.guardarInJson=True

    def seleccionarComoAgregar(self, sensorValues=None):
        self.readSensorValue(self.dataFileSensorValues)
        id_sensor = int(input("ID del valor que desea seleccionar (-1 para crear uno nuevo): "))

        if id_sensor == -1:
            # Crea un nuevo valor
            self.createSensorValue(sensorValues)
        else:
            # Obtener el valor seleccionado
            valor_asignado = self.dataFileSensorValues.search(id_sensor)
            if valor_asignado:
                self.instanciaSensorValues.create(valor_asignado)
            else:
                print("ID del valor inválido.")

        return self.instanciaSensorValues

    def createSensorValue(self, sensorValues=None):
        if sensorValues is None:
            sensorValues = self.instanciaSensorValues

        ValueID = input("ID del valor tomado: ")
        SensorID = input("ID del sensor que está tomando el valor: ")
        Value = input("Valor tomado por el sensor: ")
        SensorValue = SensorValues(ValueID, SensorID, Value)
        res = sensorValues.create(SensorValue)

        if res == 1:
            print("Se ha guardado el valor correctamente.")
            #if self.guardarInJson == False:
                #self.instancia.create(sensor)
            self.guardarEnJSON()
            # SE GUARDA EN LA COLECCIÓN CORRESPONDIENTE
            #self.mongodb_connection.insert_document(obj.diccionario())
            #print("Se ha guardado en MongoDB")
        else:
            print("Hubo un error al guardar el valor.")
        return SensorValue

    def readSensorValue(self, sensorValues=None):
        if sensorValues is None:
            sensorValues = self.instanciaSensorValues

        if os.path.getsize("../JSON/SensorValues.json") == 0:
            print("No hay valores tomados de los sensores actualmente.")
        else:
            print("\nValores existentes: ")
            print(sensorValues.encabezados())
            for obj in sensorValues.lista:
                print(f"{obj}")
            #for i, obj in enumerate(sensors.read()):
                #print(f"{i}. {obj}")

    def updateSensorValue(self, sensorValues=None):
        if sensorValues is None:
            sensorValues = self.instanciaSensorValues

        if os.path.getsize("../JSON/SensorValues.json") == 0:
            print("No hay valores tomados de los sensores actualmente.")
        else:
            self.readSensorValue(sensorValues)  # Ahora mostrará las asignaciones proporcionados en lugar de los internos

            id = int(input("ID del valor que desea actualizar: "))
            valorAActualizar = sensorValues.search(id)

            if valorAActualizar:
                print(f"\nDatos actuales del valor a actualizar:")
                print(sensorValues.encabezados())
                print(f"{valorAActualizar}")

                # Solicitar los nuevos datos para el valor
                ValueID = input("Nuevo ID del valor (deje vacío para mantener el actual): ")
                SensorID = input("Nuevo ID del sensor que tomó el valor (deje vacío para mantener el actual): ")
                Value = input("Nuevo valor que tomó el sensor (deje vacío para mantener el actual): ")

                # Verificar si se ingresaron nuevos datos para el valor
                if ValueID or SensorID or Value:
                    # Si se proporcionan nuevos datos, crear un objeto UserCages con ellos
                    SensorValue = SensorValues(
                        ValueID or valorAActualizar.ValueID,
                        SensorID or valorAActualizar.SensorID,
                        Value or valorAActualizar.Value
                    )

                    # Intentar actualizar la asignación con los nuevos datos
                    res = sensorValues.update(id, SensorValue)
                    if res == 1:
                        print("Se ha actualizado el valor correctamente.")
                        # if not self.guardarInJson:
                            # self.instancia.update(id, obj)
                        self.guardarEnJSON()
                        # SE ACTUALIZA EN LA COLECCIÓN CORRESPONDIENTE
                        # query = {"Nombre": funcionAActualizar.nombre}
                        # self.mongodb_connection.update_document(query, obj.diccionario())
                        # print("Se ha actualizado en MongoDB")
                        return sensorValues
                    else:
                        print("Hubo un error al actualizar el valor.")
                else:
                    print("No se proporcionaron nuevos datos. El valor permanece sin cambios.")
            else:
                print("ID del valor inválido.")

    def deleteSensorValue(self, sensorValues=None):
        if sensorValues is None:
            sensorValues = self.instanciaSensorValues

        if os.path.getsize("../JSON/UsersCages.json") == 0:
            print("No hay valores tomados de los sensores actualmente.")
        else:
            self.readSensorValue(sensorValues)

            id = int(input("ID del valor que desea eliminar: "))
            valorAEliminar = sensorValues.search(id)

            if valorAEliminar:
                res = sensorValues.delete(id)
                if res == 1:
                    print("Se ha eliminado el valor correctamente.")
                    self.guardarEnJSON()
                    # SE GUARDA EN LA COLECCIÓN CORRESPONDIENTE
                    #query = {"Nombre": funcionAEliminar.nombre}
                    #self.mongodb_connection.delete_document(query)
                    #print("Se ha eliminado de MongoDB")
                else:
                    print("Hubo un error al eliminar el valor.")
            else:
                print("ID del valor inválido.")

    def guardarEnJSON(self):
        if self.guardarInJson:
            diccionario_obj = self.instanciaSensorValues.diccionario()
            self.instanciaSensorValues.guardar(diccionario_obj)
        else:
            diccionario_obj = self.instancia.diccionario()
            self.instancia.guardar(diccionario_obj)

    def interfaz(self):
        print("\n-------------VALORES TOMADOS POR LOS SENSORES-----------")
        while True:
            print("\nSeleccione qué desea realizar:")
            print("1. Crear")
            print("2. Mostrar")
            print("3. Actualizar")
            print("4. Eliminar")
            print("5. Salir")
            operation = input("Operación a realizar: ")

            if operation == "1":  # CREAR
                self.createSensorValue()
            elif operation == "2":  # MOSTRAR
                self.readSensorValue()
            elif operation == "3":  # ACTUALIZAR
                self.updateSensorValue()
            elif operation == "4":  # ELIMINAR
                self.deleteSensorValue()
            elif operation == "5":
                print("Saliendo del programa. ¡Hasta pronto!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
                continue


if __name__ == "__main__":
    interfazValoresInstancia = SensorValuesInterface() # Forma 1
    # interfazFuncionesInstancia = InterfazFunciones_V2(Funciones()) #Forma 2 (Se va a comportar como una lista)
    interfazValoresInstancia.interfaz()
