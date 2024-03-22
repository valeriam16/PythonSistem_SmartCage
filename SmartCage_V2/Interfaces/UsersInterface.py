import os
from Logic.Users import Users
#from Logic.ConexionMongoDB import ConexionMongoDB


class UsersInterface:
    def __init__(self, user=None):
        #CONEXIÓN A MONGODB
        #self.mongodb_connection = ConexionMongoDB(collection_name='funciones')

        #TRABAJA CON EL JSON, SI SE LA MANDA UNA INSTANCIA
        if user is not None:
            self.instanciaUser = user # Si se proporciona una instancia de Users, úsala
            self.dataFileUser = Users() # Lista[] que servira para guardar los datos de los usuarios existentes en el JSON

            if os.path.exists("../JSON/Users.json") and os.path.getsize("../JSON/Users.json") > 0:
                self.dataFileUser.cargar() # Aquí guardamos los datos del JSON en la lista[]
            else:
                pass
                #print("No hay usuarios actualmente.")

            self.instancia = self.dataFileUser
            self.guardarInJson=False
        else:
            # CREA NUEVA FUNCIÓN, NO SE LE MANDA UNA INSTANCIA
            self.instanciaUser = Users()

            if os.path.exists("../JSON/Users.json") and os.path.getsize("../JSON/Users.json") > 0:
                self.instanciaUser.cargar()
            else:
                pass
                #print("No hay usuarios actualmente.")

            self.instancia = self.instanciaUser
            self.guardarInJson=True

    def seleccionarComoAgregar_PASADO(self, users=None):
        self.readUsers(self.dataFileUser)
        id_user = int(input("ID del usuario que desea asignar (-1 para crear uno nuevo): "))

        if id_user == -1:
            # Crea un nuevo usuario
            self.createUser(users)
        else:
            # Obtener el usuario seleccionado
            usuario_asignado = self.dataFileUser.search(id_user)
            if usuario_asignado:
                self.instanciaUser.create(usuario_asignado)
            else:
                print("ID del usuario inválido.")

        return self.instanciaUser

    def seleccionarComoAgregar(self, users=None):
        self.readUsers(self.dataFileUser)
        id_user = int(input("ID del usuario que desea asignar (-1 para crear uno nuevo): "))

        if id_user == -1:
            # Crea un nuevo usuario
            new_user = self.createUser(users)
            return new_user  # Devuelve el objeto de usuario creado
        else:
            # Obtener el usuario seleccionado
            usuario_asignado = self.dataFileUser.search(id_user)
            if usuario_asignado:
                self.instanciaUser.create(usuario_asignado)
                return usuario_asignado  # Devuelve el objeto de usuario encontrado
            else:
                print("ID del usuario inválido.")
                return None  # Devuelve None si no se encuentra el usuario

    def seleccionarActualizacion(self, current_user_id):
        self.readUsers()  # Asume que tienes un método para mostrar los usuarios disponibles
        nuevo_userID = int(input("Selecciona un UserID nuevo: "))
        if nuevo_userID == current_user_id:
            return current_user_id
        else:
            return nuevo_userID

    def createUser(self, users=None):
        if users is None:
            users = self.instanciaUser

        userID = int(input("ID del usuario: "))
        name = input("Nombre: ")
        user = input("User: ")
        email = input("Email: ")
        password = input("Password: ")
        user = Users(userID, name, user, email, password)
        res = users.create(user)

        if res == 1:
            print("Se ha creado el usuario correctamente.")
            # Este if sirve para cuando se está creando algo desde una interfaz externa
            if self.guardarInJson == False:
                self.instancia.create(user)
            self.guardarEnJSON()
            # SE GUARDA EN LA COLECCIÓN CORRESPONDIENTE
            #self.mongodb_connection.insert_document(obj.diccionario())
            #print("Se ha guardado en MongoDB")
        else:
            print("Hubo un error al crear el usuario.")
        return user

    def readUsers(self, users=None):
        if users is None:
            users = self.instanciaUser

        if os.path.getsize("../JSON/Users.json") == 0:
            print("No hay usuarios actualmente.")
        else:
            print("\nUsuarios existentes: ")
            print(users.encabezados())
            for obj in users.lista:
                print(f"{obj}")

    def updateUser(self, users=None):
        if users is None:
            users = self.instanciaUser

        if os.path.getsize("../JSON/Users.json") == 0:
            print("No hay usuarios actualmente.")
        else:
            self.readUsers(users)  # Ahora mostrará los usuarios proporcionados en lugar de los internos

            id = int(input("ID del usuario que desea actualizar: "))
            usuarioAActualizar = users.search(id)

            if usuarioAActualizar:
                print(f"\nDatos actuales del usuario a actualizar:")
                print(users.encabezados())
                print(f"{usuarioAActualizar}")

                # Solicitar los nuevos datos para el usuario
                userID = input("Nuevo ID del usuario (deje vacío para mantener el actual): ")
                name = input("Nuevo nombre (deje vacío para mantener el actual): ")
                user = input("Nuevo user (deje vacío para mantener el actual): ")
                email = input("Nuevo email (deje vacío para mantener el actual): ")
                password = input("Nueva contraseña (deje vacío para mantener la actual): ")

                # Verificar si se ingresaron nuevos datos para el sensor
                if userID or name or user or email or password:
                    # Si se proporcionan nuevos datos, crear un objeto Users con ellos
                    user = Users(
                        userID or usuarioAActualizar.ID,
                        name or usuarioAActualizar.Name,
                        user or usuarioAActualizar.User,
                        email or usuarioAActualizar.Email,
                        password or usuarioAActualizar.Password
                    )

                    # Intentar actualizar el usuario con los nuevos datos
                    res = users.update(id, user)
                    if res == 1:
                        print("Se ha actualizado el usuario correctamente.")
                        #if not self.guardarInJson:
                            #self.instancia.update(id, obj)
                        self.guardarEnJSON()
                        # SE ACTUALIZA EN LA COLECCIÓN CORRESPONDIENTE
                        #query = {"Nombre": funcionAActualizar.nombre}
                        #self.mongodb_connection.update_document(query, obj.diccionario())
                        #print("Se ha actualizado en MongoDB")
                        return users
                    else:
                        print("Hubo un error al actualizar el usuario.")
                else:
                    print("No se proporcionaron nuevos datos. El usuario permanece sin cambios.")
            else:
                print("ID del usuario inválido.")

    def deleteUser(self, users=None):
        if users is None:
            users = self.instanciaUser

        if os.path.getsize("../JSON/Users.json") == 0:
            print("No hay usuarios actualmente.")
        else:
            self.readUsers(users)

            id = int(input("ID del usuario que desea eliminar: "))
            usuarioAEliminar = users.search(id)

            if usuarioAEliminar:
                res = users.delete(id)
                if res == 1:
                    print("Se ha eliminado el usuario correctamente.")
                    self.guardarEnJSON()
                    # SE GUARDA EN LA COLECCIÓN CORRESPONDIENTE
                    #query = {"Nombre": funcionAEliminar.nombre}
                    #self.mongodb_connection.delete_document(query)
                    #print("Se ha eliminado de MongoDB")
                else:
                    print("Hubo un error al eliminar el usuario.")
            else:
                print("ID del usuario inválido.")

    def guardarEnJSON(self):
        if self.guardarInJson:
            diccionario_obj = self.instanciaUser.diccionario()
            self.instanciaUser.guardar(diccionario_obj)
        else:
            diccionario_obj = self.instancia.diccionario()
            self.instancia.guardar(diccionario_obj)

    def interfaz(self):
        while True:
            print("\n----------- Usuarios -----------")
            print("\nSeleccione qué desea realizar:")
            print("1. Crear")
            print("2. Mostrar")
            print("3. Actualizar")
            print("4. Eliminar")
            print("5. Salir")
            operation = input("Operación a realizar: ")

            if operation == "1":  # CREAR
                self.createUser()
            elif operation == "2":  # MOSTRAR
                self.readUsers()
            elif operation == "3":  # ACTUALIZAR
                self.updateUser()
            elif operation == "4":  # ELIMINAR
                self.deleteUser()
            elif operation == "5":
                print("Saliendo del programa. ¡Hasta pronto!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
                continue


if __name__ == "__main__":
    instancia = UsersInterface()
    instancia.interfaz()
