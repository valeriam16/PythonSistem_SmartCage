import os
from Logic.Sensors import Sensors
#from Logic.ConexionMongoDB import ConexionMongoDB


class SensorsInterface:
    def __init__(self, sensors=None):
        #CONEXIÓN A MONGODB
        #self.mongodb_connection = ConexionMongoDB(collection_name='funciones')

        #TRABAJA CON EL JSON, SI SE LA MANDA UNA INSTANCIA
        if sensors is not None:
            self.instanciaSensors = sensors # Si se proporciona una instancia de Sensors, úsala
            self.dataFileSensors = Sensors() # Lista[] que servira para guardar los datos de las funciones existentes en el JSON

            if os.path.exists("../JSON/Sensors.json") and os.path.getsize("../JSON/Sensors.json") > 0:
                self.dataFileSensors.cargar() # Aquí guardamos los datos del JSON en la lista[]
            else:
                print("No hay sensores actualmente.")

            self.instancia = self.dataFileSensors
            self.guardarInJson=False
        else:
            # CREA NUEVA FUNCIÓN, NO SE LE MANDA UNA INSTANCIA
            self.instanciaSensors = Sensors()

            if os.path.exists("../JSON/Sensors.json") and os.path.getsize("../JSON/Sensors.json") > 0:
                self.instanciaSensors.cargar()
            else:
                print("No hay sensores actualmente.")
            self.instancia = self.instanciaSensors

            self.guardarInJson=True

    def seleccionarComoAgregar(self, sensors=None):
        self.readSensors(self.dataFileSensors)
        id_sensor = int(input("ID del sensor que desea seleccionar (-1 para crear uno nuevo): "))

        if id_sensor == -1:
            # Crea un nuevo sensor
            self.createSensor(sensors)
        else:
            # Obtener el sensor seleccionado
            sensor_asignado = self.dataFileSensors.search(id_sensor)
            if sensor_asignado:
                self.instanciaSensors.create(sensor_asignado)
            else:
                print("ID del sensor inválido.")

        return self.instanciaSensors

    def createSensor(self, sensors=None):
        if sensors is None:
            sensors = self.instanciaSensors

        ID = input("ID del sensor: ")
        type = input("Tipo de sensor: ")
        name = input("Nombre del sensor: ")
        unit = input("Unidad en que tomará las medidas el sensor: ")
        description = input("Descripción de lo que se monitoreará con el sensor: ")
        sensor = Sensors(ID, type, name, unit, description)
        res = sensors.create(sensor)

        if res == 1:
            print("Se ha creado el sensor correctamente.")
            #if self.guardarInJson == False:
                #self.instancia.create(sensor)
            self.guardarEnJSON()
            # SE GUARDA EN LA COLECCIÓN CORRESPONDIENTE
            #self.mongodb_connection.insert_document(obj.diccionario())
            #print("Se ha guardado en MongoDB")
        else:
            print("Hubo un error al crear el sensor.")
        return sensor

    def readSensors(self, sensors=None):
        if sensors is None:
            sensors = self.instanciaSensors

        if os.path.getsize("../JSON/Sensors.json") == 0:
            print("No hay sensores actualmente.")
        else:
            print("\nSensores existentes: ")
            print(sensors.encabezados())
            for obj in sensors.lista:
                print(f"{obj}")
            #for i, obj in enumerate(sensors.read()):
                #print(f"{i}. {obj}")

    def updateSensor(self, sensors=None):
        if sensors is None:
            sensors = self.instanciaSensors

        if os.path.getsize("../JSON/Sensors.json") == 0:
            print("No hay sensores actualmente.")
        else:
            self.readSensors(sensors)  # Ahora mostrará los sensores proporcionados en lugar de los internos

            id = int(input("ID del sensor que desea actualizar: "))
            sensorAActualizar = sensors.search(id)

            if sensorAActualizar:
                print(f"\nDatos actuales del sensor a actualizar:")
                print(sensors.encabezados())
                print(f"{sensorAActualizar}")

                # Solicitar los nuevos datos para el sensor
                ID = input("Nuevo ID del sensor (deje vacío para mantener el actual): ")
                type = input("Nuevo tipo de sensor (deje vacío para mantener el actual): ")
                name = input("Nuevo nombre del sensor (deje vacío para mantener el actual): ")
                unit = input("Nueva unidad del sensor (deje vacío para mantener la actual): ")
                description = input("Nueva descripción del sensor (deje vacío para mantener la actual): ")

                # Verificar si se ingresaron nuevos datos para el sensor
                if ID or type or name or unit or description:
                    # Si se proporcionan nuevos datos, crear un objeto Funciones con ellos
                    sensor = Sensors(
                        ID or sensorAActualizar.ID,
                        type or sensorAActualizar.Type,
                        name or sensorAActualizar.Name,
                        unit or sensorAActualizar.Unit,
                        description or sensorAActualizar.Description
                    )

                    # Intentar actualizar el sensor con los nuevos datos
                    res = sensors.update(id, sensor)
                    if res == 1:
                        print("Se ha actualizado el sensor correctamente.")
                        # if not self.guardarInJson:
                            # self.instancia.update(id, obj)
                        self.guardarEnJSON()
                        # SE ACTUALIZA EN LA COLECCIÓN CORRESPONDIENTE
                        # query = {"Nombre": funcionAActualizar.nombre}
                        # self.mongodb_connection.update_document(query, obj.diccionario())
                        # print("Se ha actualizado en MongoDB")
                        return sensors
                    else:
                        print("Hubo un error al actualizar el sensor.")
                else:
                    print("No se proporcionaron nuevos datos. El sensor permanece sin cambios.")
            else:
                print("ID del sensor inválido.")

    def deleteSensor(self, sensors=None):
        if sensors is None:
            sensors = self.instanciaSensors

        if os.path.getsize("../JSON/Sensors.json") == 0:
            print("No hay sensores actualmente.")
        else:
            self.readSensors(sensors)

            id = int(input("ID del sensor que desea eliminar: "))
            sensorAEliminar = sensors.search(id)

            if sensorAEliminar:
                res = sensors.delete(id)
                if res == 1:
                    print("Se ha eliminado el sensor correctamente.")
                    self.guardarEnJSON()
                    # SE GUARDA EN LA COLECCIÓN CORRESPONDIENTE
                    #query = {"Nombre": funcionAEliminar.nombre}
                    #self.mongodb_connection.delete_document(query)
                    #print("Se ha eliminado de MongoDB")
                else:
                    print("Hubo un error al eliminar el sensor.")
            else:
                print("ID del sensor inválido.")

    def guardarEnJSON(self):
        if self.guardarInJson:
            diccionario_obj = self.instanciaSensors.diccionario()
            self.instanciaSensors.guardar(diccionario_obj)
        else:
            diccionario_obj = self.instancia.diccionario()
            self.instancia.guardar(diccionario_obj)

    def interfaz(self):
        print("\n-------------SENSORES-----------")
        while True:
            print("\nSeleccione qué desea realizar:")
            print("1. Crear")
            print("2. Mostrar")
            print("3. Actualizar")
            print("4. Eliminar")
            print("5. Salir")
            operation = input("Operación a realizar: ")

            if operation == "1":  # CREAR
                self.createSensor()
            elif operation == "2":  # MOSTRAR
                self.readSensors()
            elif operation == "3":  # ACTUALIZAR
                self.updateSensor()
            elif operation == "4":  # ELIMINAR
                self.deleteSensor()
            elif operation == "5":
                print("Saliendo del programa. ¡Hasta pronto!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
                continue


if __name__ == "__main__":
    interfazSensoresInstancia = SensorsInterface() # Forma 1
    # interfazFuncionesInstancia = InterfazFunciones_V2(Funciones()) #Forma 2 (Se va a comportar como una lista)
    interfazSensoresInstancia.interfaz()
