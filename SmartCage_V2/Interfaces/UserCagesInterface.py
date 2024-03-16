import os
from Logic.UsersCages import UsersCages
#from Logic.ConexionMongoDB import ConexionMongoDB


class UserCagesInterface:
    def __init__(self, userCages=None):
        #CONEXIÓN A MONGODB
        #self.mongodb_connection = ConexionMongoDB(collection_name='funciones')

        #TRABAJA CON EL JSON, SI SE LA MANDA UNA INSTANCIA
        if userCages is not None:
            self.instanciaUserCages = userCages # Si se proporciona una instancia de UserCages, úsala
            self.dataFileUserCages = UsersCages() # Lista[] que servira para guardar los datos de los UserCages existentes en el JSON

            if os.path.exists("../JSON/UsersCages.json") and os.path.getsize("../JSON/UsersCages.json") > 0:
                self.dataFileUserCages.cargar() # Aquí guardamos los datos del JSON en la lista[]
            else:
                print("No hay usuarios asignados a jaulas actualmente.")

            self.instancia = self.dataFileUserCages
            self.guardarInJson=False
        else:
            # CREA NUEVA ASIGNACIÓN, NO SE LE MANDA UNA INSTANCIA
            self.instanciaUserCages = UsersCages()

            if os.path.exists("../JSON/UsersCages.json") and os.path.getsize("../JSON/UsersCages.json") > 0:
                self.instanciaUserCages.cargar()
            else:
                print("No hay usuarios asignados a jaulas actualmente.")
            self.instancia = self.instanciaUserCages

            self.guardarInJson=True

    def seleccionarComoAgregar(self, userAssigment=None):
        self.readUserAssignment(self.dataFileUserCages)
        id_sensor = int(input("ID de la asignación que desea seleccionar (-1 para crear uno nuevo): "))

        if id_sensor == -1:
            # Crea una nueva asignación
            self.createUserAssignment(userAssigment)
        else:
            # Obtener la asignación seleccionado
            asignacion_asignada = self.dataFileUserCages.search(id_sensor)
            if asignacion_asignada:
                self.instanciaUserCages.create(asignacion_asignada)
            else:
                print("ID del sensor inválido.")

        return self.instanciaUserCages

    def createUserAssignment(self, userAssigment=None):
        if userAssigment is None:
            userAssigment = self.instanciaUserCages

        UsersCagesID = input("ID de asignación: ")
        CageID = input("ID de la jaula a la que se está asignando el sensor: ")
        UserID = input("ID del usuario al que pertenece esa jaula: ")
        UserCage = UsersCages(UsersCagesID, CageID, UserID)
        res = userAssigment.create(UserCage)

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
        return UserCage

    def readUserAssignment(self, userAssigment=None):
        if userAssigment is None:
            userAssigment = self.instanciaUserCages

        if os.path.getsize("../JSON/UsersCages.json") == 0:
            print("No hay asignaciones actualmente.")
        else:
            print("\nAsignaciones existentes: ")
            print(userAssigment.encabezados())
            for obj in userAssigment.lista:
                print(f"{obj}")
            #for i, obj in enumerate(sensors.read()):
                #print(f"{i}. {obj}")

    def updateUserAssigment(self, userAssigment=None):
        if userAssigment is None:
            userAssigment = self.instanciaUserCages

        if os.path.getsize("../JSON/UsersCages.json") == 0:
            print("No hay asignaciones actualmente.")
        else:
            self.readUserAssignment(userAssigment)  # Ahora mostrará las asignaciones proporcionados en lugar de los internos

            id = int(input("ID de la asignación que desea actualizar: "))
            asignacionAActualizar = userAssigment.search(id)

            if asignacionAActualizar:
                print(f"\nDatos actuales de la asignación a actualizar:")
                print(userAssigment.encabezados())
                print(f"{asignacionAActualizar}")

                # Solicitar los nuevos datos para el sensor
                UsersCagesID = input("Nuevo ID de la asignación (deje vacío para mantener el actual): ")
                CageID = input("Nuevo ID de la jaula (deje vacío para mantener el actual): ")
                UserID = input("Nuevo ID del usuario al que le pertenece la jaula (deje vacío para mantener el actual): ")

                # Verificar si se ingresaron nuevos datos para la asignación
                if UsersCagesID or CageID or UserID:
                    # Si se proporcionan nuevos datos, crear un objeto UserCages con ellos
                    UserCage = UsersCages(
                        UsersCagesID or asignacionAActualizar.UsersCagesID,
                        CageID or asignacionAActualizar.CageID,
                        UserID or asignacionAActualizar.UserID
                    )

                    # Intentar actualizar la asignación con los nuevos datos
                    res = userAssigment.update(id, UserCage)
                    if res == 1:
                        print("Se ha actualizado la asignación de la caja a un usuario correctamente.")
                        # if not self.guardarInJson:
                            # self.instancia.update(id, obj)
                        self.guardarEnJSON()
                        # SE ACTUALIZA EN LA COLECCIÓN CORRESPONDIENTE
                        # query = {"Nombre": funcionAActualizar.nombre}
                        # self.mongodb_connection.update_document(query, obj.diccionario())
                        # print("Se ha actualizado en MongoDB")
                        return userAssigment
                    else:
                        print("Hubo un error al actualizar la asignación.")
                else:
                    print("No se proporcionaron nuevos datos. La asignación permanece sin cambios.")
            else:
                print("ID de la asignación inválido.")

    def deleteUserAssigment(self, userAssigment=None):
        if userAssigment is None:
            userAssigment = self.instanciaUserCages

        if os.path.getsize("../JSON/UsersCages.json") == 0:
            print("No hay asignaciones actualmente.")
        else:
            self.readUserAssignment(userAssigment)

            id = int(input("ID de la asignación que desea eliminar: "))
            asignacionAEliminar = userAssigment.search(id)

            if asignacionAEliminar:
                res = userAssigment.delete(id)
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
            diccionario_obj = self.instanciaUserCages.diccionario()
            self.instanciaUserCages.guardar(diccionario_obj)
        else:
            diccionario_obj = self.instancia.diccionario()
            self.instancia.guardar(diccionario_obj)

    def interfaz(self):
        print("\n-------------ASIGNACIONES DE JAULAS A USUARIOS-----------")
        while True:
            print("\nSeleccione qué desea realizar:")
            print("1. Crear")
            print("2. Mostrar")
            print("3. Actualizar")
            print("4. Eliminar")
            print("5. Salir")
            operation = input("Operación a realizar: ")

            if operation == "1":  # CREAR
                self.createUserAssignment()
            elif operation == "2":  # MOSTRAR
                self.readUserAssignment()
            elif operation == "3":  # ACTUALIZAR
                self.updateUserAssigment()
            elif operation == "4":  # ELIMINAR
                self.deleteUserAssigment()
            elif operation == "5":
                print("Saliendo del programa. ¡Hasta pronto!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
                continue


if __name__ == "__main__":
    interfazAsignacionInstancia = UserCagesInterface() # Forma 1
    # interfazFuncionesInstancia = InterfazFunciones_V2(Funciones()) #Forma 2 (Se va a comportar como una lista)
    interfazAsignacionInstancia.interfaz()
