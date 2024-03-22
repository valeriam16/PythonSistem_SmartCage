import os

from Interfaces.CagesInterface import CagesInterface
from Interfaces.UsersInterface import UsersInterface
from Logic.Cages import Cages
from Logic.Users import Users
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
                pass
                # print("No hay usuarios asignados a jaulas actualmente.")

            self.instancia = self.dataFileUserCages
            self.guardarInJson=False
        else:
            # CREA NUEVA ASIGNACIÓN, NO SE LE MANDA UNA INSTANCIA
            self.instanciaUserCages = UsersCages()

            if os.path.exists("../JSON/UsersCages.json") and os.path.getsize("../JSON/UsersCages.json") > 0:
                self.instanciaUserCages.cargar()
            else:
                pass
                # print("No hay usuarios asignados a jaulas actualmente.")

            self.instancia = self.instanciaUserCages
            self.guardarInJson=True

        # Inicializar un conjunto para almacenar los ID utilizados
        self.used_ids = set(cage.ID for cage in self.instanciaUserCages.lista)

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

        # print("------------- Asignando una jaula a un usuario -------------")
        # Obtener el siguiente ID disponible
        ID = self.get_next_available_id()

        # Obtener el objeto de USUARIO y usar su ID
        usersInstance = UsersInterface(Users())
        selected_user = usersInstance.seleccionarComoAgregar()
        UserID = selected_user.ID if selected_user else None

        # Obtener el objeto de JAULA y usar su ID
        cageInstance = CagesInterface(Cages())
        selected_cage = cageInstance.seleccionarComoAgregar()
        CageID = selected_cage.ID if selected_cage else None

        UserCage = UsersCages(ID, UserID, CageID)
        res = userAssigment.create(UserCage)

        if res == 1:
            print("Se ha creado la asignación de una jaula a un usuario correctamente.")
            # Agregar el nuevo ID al conjunto de ID utilizados
            self.used_ids.add(ID)
            # Este if sirve para cuando se está creando algo desde una interfaz externa
            if self.guardarInJson == False:
                self.instancia.create(UserCage)
            self.guardarEnJSON()
        else:
            print("Hubo un error al crear la asignación de una jaula a un usuario.")
        return UserCage

    def get_next_available_id(self):
        # Encontrar el siguiente ID disponible después del último ID utilizado
        new_id = max(self.used_ids, default=0) + 1
        return new_id

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

    def updateUserAssigment_PASADO(self, userAssigment=None):
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
                ID = input("Nuevo ID de la asignación (deje vacío para mantener el actual): ")

                # Preguntar al usuario si desea mantener el CageID actual o actualizarlo
                respuesta = input("¿Desea mantener el CageID actual? (Sí/No): ").lower()
                if respuesta == "sí" or respuesta == "si":
                    # Mantener el CageID actual
                    CageID = asignacionAActualizar.CageID
                else:
                    # Actualizar el CageID
                    interfazCages = CagesInterface()
                    CageID = interfazCages.seleccionarActualizacion(asignacionAActualizar.CageID)

                # Preguntar al usuario si desea mantener el UserID actual o actualizarlo
                respuesta2 = input("¿Desea mantener el UserID actual? (Sí/No): ").lower()
                if respuesta2 == "sí" or respuesta2 == "si":
                    # Mantener el UserID actual
                    UserID = asignacionAActualizar.UserID
                else:
                    # Actualizar el UserID
                    interfazUsers = UsersInterface()
                    UserID = interfazUsers.seleccionarActualizacion(asignacionAActualizar.UserID)

                # Verificar si se ingresaron nuevos datos para la asignación
                if ID or CageID or UserID:
                    # Si se proporcionan nuevos datos, crear un objeto UserCages con ellos
                    UserCage = UsersCages(
                        ID or asignacionAActualizar.ID,
                        CageID,
                        UserID
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

                # Solicitar los nuevos datos para la asignación
                # ID = input("Nuevo ID de la asignación (deje vacío para mantener el actual): ")

                # Preguntar al usuario si desea mantener el UserID actual o actualizarlo
                respuesta = input("¿Desea mantener el UserID actual? (Sí/No): ").lower()
                if respuesta == "sí" or respuesta == "si":
                    # Mantener el UserID actual
                    UserID = asignacionAActualizar.UserID
                else:
                    # Actualizar el UserID
                    interfazUsers = UsersInterface()
                    UserID = interfazUsers.seleccionarActualizacion(asignacionAActualizar.UserID)

                # Preguntar al usuario si desea mantener el CageID actual o actualizarlo
                respuesta = input("¿Desea mantener el CageID actual? (Sí/No): ").lower()
                if respuesta == "sí" or respuesta == "si":
                    # Mantener el CageID actual
                    CageID = asignacionAActualizar.CageID
                else:
                    # Actualizar el CageID
                    interfazCages = CagesInterface()
                    CageID = interfazCages.seleccionarActualizacion(asignacionAActualizar.CageID)

                # Verificar si se ingresaron nuevos datos para la asignación
                if CageID or UserID:
                    # Si se proporcionan nuevos datos, crear un objeto UsersCages con ellos
                    UserCage = UsersCages(
                        asignacionAActualizar.ID,
                        UserID,
                        CageID
                    )

                    # Actualizar la asignación con los nuevos datos
                    res = userAssigment.update(id, UserCage)
                    if res == 1:
                        print("Se ha actualizado la asignación correctamente.")
                        if not self.guardarInJson:
                            self.instancia.update(id, UserCage)
                        self.guardarEnJSON()
                        # SE ACTUALIZA EN LA COLECCIÓN CORRESPONDIENTE
                        #query = {"Numero": salaAActualizar.numero}
                        #self.mongodb_connection.update_document(query, obj.diccionario())
                        #print("Se ha actualizado en MongoDB")
                        return UserCage
                    else:
                        print("Hubo un error al actualizar la asignación.")
                else:
                    print("No se proporcionaron nuevos datos. La asignación permanece sin cambios.")
            else:
                print("ID de la asignación no válido.")

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
        while True:
            print("\n----------- Jaulas - Usuarios -----------")
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
    instancia = UserCagesInterface()
    instancia.interfaz()
