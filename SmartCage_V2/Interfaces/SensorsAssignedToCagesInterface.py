import os
from Logic.SensorsAssignedToCages import SensorsAssignedToCages
#from Logic.ConexionMongoDB import ConexionMongoDB


class SensorsAsignedToCagesInterface:
    def __init__(self, sensorsAssigned=None):
        #CONEXIÓN A MONGODB
        #self.mongodb_connection = ConexionMongoDB(collection_name='funciones')

        #TRABAJA CON EL JSON, SI SE LA MANDA UNA INSTANCIA
        if sensorsAssigned is not None:
            self.instanciaSensorsAssigned = sensorsAssigned # Si se proporciona una instancia de SensorsAssigned, úsala
            self.dataFileSensorsAssigned = SensorsAssignedToCages() # Lista[] que servira para guardar los datos de las funciones existentes en el JSON

            if os.path.exists("../JSON/SensorsAssignedToCages.json") and os.path.getsize("../JSON/SensorsAssignedToCages.json") > 0:
                self.dataFileSensorsAssigned.cargar() # Aquí guardamos los datos del JSON en la lista[]
            else:
                print("No hay sensores asignados actualmente.")

            self.instancia = self.dataFileSensorsAssigned
            self.guardarInJson=False
        else:
            # CREA NUEVA ASIGNACIÓN, NO SE LE MANDA UNA INSTANCIA
            self.instanciaSensorsAssigned = SensorsAssignedToCages()

            if os.path.exists("../JSON/SensorsAssignedToCages.json") and os.path.getsize("../JSON/SensorsAssignedToCages.json") > 0:
                self.instanciaSensorsAssigned.cargar()
            else:
                print("No hay sensores asignados actualmente.")
            self.instancia = self.instanciaSensorsAssigned

            self.guardarInJson=True

    def seleccionarComoAgregar(self, assigment=None):
        self.readAssigment(self.dataFileSensorsAssigned)
        id_sensor = int(input("ID de la asignación que desea seleccionar (-1 para crear uno nuevo): "))

        if id_sensor == -1:
            # Crea una nueva asignación
            self.createAssignment(assigment)
        else:
            # Obtener la asignación seleccionado
            asignacion_asignada = self.dataFileSensorsAssigned.search(id_sensor)
            if asignacion_asignada:
                self.instanciaSensorsAssigned.create(asignacion_asignada)
            else:
                print("ID del sensor inválido.")

        return self.instanciaSensorsAssigned

    def createAssignment(self, assigment=None):
        if assigment is None:
            assigment = self.instanciaSensorsAssigned

        SensorAssignedID = input("ID de asignación: ")
        SensorID = input("ID del sensor que se está asignandp: ")
        NumberSensor = input("Número del sensor: ")
        CageID = input("Jaula a la que se está asignando el sensor: ")
        UserID = (input("Usuario al que pertenece esa jaula: "))
        SensorAssigned = SensorsAssignedToCages(SensorAssignedID, SensorID, NumberSensor, CageID, UserID)
        res = assigment.create(SensorAssigned)

        if res == 1:
            print("Se ha creado la asignación correctamente.")
            #if self.guardarInJson == False:
                #self.instancia.create(sensor)
            self.guardarEnJSON()
            # SE GUARDA EN LA COLECCIÓN CORRESPONDIENTE
            #self.mongodb_connection.insert_document(obj.diccionario())
            #print("Se ha guardado en MongoDB")
        else:
            print("Hubo un error al crear la asignación.")
        return SensorAssigned

    def readAssigment(self, assigment=None):
        if assigment is None:
            assigment = self.instanciaSensorsAssigned

        if os.path.getsize("../JSON/SensorsAssignedToCages.json") == 0:
            print("No hay asignaciones actualmente.")
        else:
            print("\nAsignaciones existentes: ")
            print(assigment.encabezados())
            for obj in assigment.lista:
                print(f"{obj}")
            #for i, obj in enumerate(sensors.read()):
                #print(f"{i}. {obj}")

    def updateAssigment(self, assigment=None):
        if assigment is None:
            assigment = self.instanciaSensorsAssigned

        if os.path.getsize("../JSON/SensorsAssignedToCages.json") == 0:
            print("No hay asignaciones actualmente.")
        else:
            self.readAssigment(assigment)  # Ahora mostrará las asignaciones proporcionados en lugar de los internos

            id = int(input("ID de la asignación que desea actualizar: "))
            asignacionAActualizar = assigment.search(id)

            if asignacionAActualizar:
                print(f"\nDatos actuales de la asignación a actualizar:")
                print(assigment.encabezados())
                print(f"{asignacionAActualizar}")

                # Solicitar los nuevos datos para el sensor
                SensorAssignedID = input("Nuevo ID de la asignación (deje vacío para mantener el actual): ")
                SensorID = input("Nuevo ID del sensor (deje vacío para mantener el actual): ")
                NumberSensor = input("Nuevo número de sensor (deje vacío para mantener el actual): ")
                CageID = input("Nuevo ID de la jaula a la que se asigno el sensor (deje vacío para mantener el actual): ")
                UserID = input("Nuevo ID del usuario al que le pertenece esa jaula (deje vacío para mantener el actual): ")

                # Verificar si se ingresaron nuevos datos para la asignación
                if SensorAssignedID or SensorID or NumberSensor or CageID or UserID:
                    # Si se proporcionan nuevos datos, crear un objeto SensorsAssignedToCages con ellos
                    SensorAssigned = SensorsAssignedToCages(
                        SensorAssignedID or asignacionAActualizar.SensorAssigned,
                        SensorID or asignacionAActualizar.SensorID,
                        NumberSensor or asignacionAActualizar.NumberSensor,
                        CageID or asignacionAActualizar.CageID,
                        UserID or asignacionAActualizar.UserID
                    )

                    # Intentar actualizar la asignación con los nuevos datos
                    res = assigment.update(id, SensorAssigned)
                    if res == 1:
                        print("Se ha actualizado la asignación de un sensor correctamente.")
                        # if not self.guardarInJson:
                            # self.instancia.update(id, obj)
                        self.guardarEnJSON()
                        # SE ACTUALIZA EN LA COLECCIÓN CORRESPONDIENTE
                        # query = {"Nombre": funcionAActualizar.nombre}
                        # self.mongodb_connection.update_document(query, obj.diccionario())
                        # print("Se ha actualizado en MongoDB")
                        return assigment
                    else:
                        print("Hubo un error al actualizar la asignación.")
                else:
                    print("No se proporcionaron nuevos datos. La asignación permanece sin cambios.")
            else:
                print("ID de la asignación inválido.")

    def deleteAssigment(self, assigment=None):
        if assigment is None:
            assigment = self.instanciaSensorsAssigned

        if os.path.getsize("../JSON/SensorsAssignedToCages.json") == 0:
            print("No hay asignaciones actualmente.")
        else:
            self.readAssigment(assigment)

            id = int(input("ID de la asignación que desea eliminar: "))
            asignacionAEliminar = assigment.search(id)

            if asignacionAEliminar:
                res = assigment.delete(id)
                if res == 1:
                    print("Se ha eliminado la asignación correctamente.")
                    self.guardarEnJSON()
                    # SE GUARDA EN LA COLECCIÓN CORRESPONDIENTE
                    #query = {"Nombre": funcionAEliminar.nombre}
                    #self.mongodb_connection.delete_document(query)
                    #print("Se ha eliminado de MongoDB")
                else:
                    print("Hubo un error al eliminar la asignación.")
            else:
                print("ID de la asignación inválido.")

    def guardarEnJSON(self):
        if self.guardarInJson:
            diccionario_obj = self.instanciaSensorsAssigned.diccionario()
            self.instanciaSensorsAssigned.guardar(diccionario_obj)
        else:
            diccionario_obj = self.instancia.diccionario()
            self.instancia.guardar(diccionario_obj)

    def interfaz(self):
        print("\n-------------ASIGNACIONES DE SENSORES-----------")
        while True:
            print("\nSeleccione qué desea realizar:")
            print("1. Crear")
            print("2. Mostrar")
            print("3. Actualizar")
            print("4. Eliminar")
            print("5. Salir")
            operation = input("Operación a realizar: ")

            if operation == "1":  # CREAR
                self.createAssignment()
            elif operation == "2":  # MOSTRAR
                self.readAssigment()
            elif operation == "3":  # ACTUALIZAR
                self.updateAssigment()
            elif operation == "4":  # ELIMINAR
                self.deleteAssigment()
            elif operation == "5":
                print("Saliendo del programa. ¡Hasta pronto!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
                continue


if __name__ == "__main__":
    interfazAsignacionInstancia = SensorsAsignedToCagesInterface() # Forma 1
    # interfazFuncionesInstancia = InterfazFunciones_V2(Funciones()) #Forma 2 (Se va a comportar como una lista)
    interfazAsignacionInstancia.interfaz()
