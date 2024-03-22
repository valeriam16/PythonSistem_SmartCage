import os
from Logic.Cages import Cages
#from Logic.ConexionMongoDB import ConexionMongoDB


class CagesInterface:
    def __init__(self, cage=None):
        #CONEXIÓN A MONGODB
        #self.mongodb_connection = ConexionMongoDB(collection_name='funciones')

        #TRABAJA CON EL JSON, SI SE LA MANDA UNA INSTANCIA
        if cage is not None:
            self.instanciaCage = cage # Si se proporciona una instancia de Cages, úsala
            self.dataFileCage = Cages() # Lista[] que servira para guardar los datos de los usuarios existentes en el JSON

            if os.path.exists("../JSON/Cages.json") and os.path.getsize("../JSON/Cages.json") > 0:
                self.dataFileCage.cargar() # Aquí guardamos los datos del JSON en la lista[]
            else:
                pass
                #print("No hay jaulas actualmente.")

            self.instancia = self.dataFileCage
            self.guardarInJson=False
        else:
            # CREA NUEVA FUNCIÓN, NO SE LE MANDA UNA INSTANCIA
            self.instanciaCage = Cages()

            if os.path.exists("../JSON/Cages.json") and os.path.getsize("../JSON/Cages.json") > 0:
                self.instanciaCage.cargar()
            else:
                pass
                #print("No hay jaulas actualmente.")

            self.instancia = self.instanciaCage
            self.guardarInJson=True

        # Inicializar un conjunto para almacenar los ID utilizados
        self.used_ids = set(cage.ID for cage in self.instanciaCage.lista)

    def seleccionarComoAgregar(self, cages=None):
        self.readCages(self.dataFileCage)
        id_cage = int(input("ID de la jaula que desea asignar (-1 para crear uno nuevo): "))

        if id_cage == -1:
            # Crea una nueva jaula
            new_cage = self.createCage(cages)
            return new_cage  # Devuelve el objeto de jaula creado
        else:
            # Obtener la jaula seleccionado
            jaula_asignada = self.dataFileCage.search(id_cage)
            if jaula_asignada:
                self.instanciaCage.create(jaula_asignada)
                return jaula_asignada  # Devuelve el objeto de jaula encontrado
            else:
                print("ID de la jaula inválido.")
                #self.seleccionarComoAgregar()
                return None  # Devuelve None si no se encuentra la jaula

    def seleccionarActualizacion(self, current_cage_id):
        self.readCages()
        nuevo_cageID = int(input("Selecciona un CageID nuevo: "))
        if nuevo_cageID == current_cage_id:
            return current_cage_id
        else:
            return nuevo_cageID

    def createCage(self, cages=None):
        if cages is None:
            cages = self.instanciaCage

        # Obtener el siguiente ID disponible
        ID = self.get_next_available_id()

        # ID = int(input("ID de la jaula: "))
        cage = Cages(ID)
        res = cages.create(cage)

        if res == 1:
            print("Se ha creado la jaula correctamente.")
            # Agregar el nuevo ID al conjunto de ID utilizados
            self.used_ids.add(ID)
            # Este if sirve para cuando se está creando algo desde una interfaz externa
            if self.guardarInJson == False:
                self.instancia.create(cage)
            self.guardarEnJSON()
            # SE GUARDA EN LA COLECCIÓN CORRESPONDIENTE
            #self.mongodb_connection.insert_document(obj.diccionario())
            #print("Se ha guardado en MongoDB")
        else:
            print("Hubo un error al crear la jaula.")
        return cage

    def get_next_available_id(self):
        # Encontrar el siguiente ID disponible después del último ID utilizado
        new_id = max(self.used_ids, default=0) + 1
        return new_id

    def readCages(self, cages=None):
        if cages is None:
            cages = self.instanciaCage

        if os.path.getsize("../JSON/Cages.json") == 0:
            print("No hay jaulas actualmente.")
        else:
            print("\nJaulas existentes: ")
            print(cages.encabezados())
            for obj in cages.lista:
                print(f"{obj}")

    def deleteCage(self, cages=None):
        if cages is None:
            cages = self.instanciaCage

        if os.path.getsize("../JSON/Cages.json") == 0:
            print("No hay jaulas actualmente.")
        else:
            self.readCages(cages)

            id = int(input("ID de la jaula que desea eliminar: "))
            jaulaAEliminar = cages.search(id)

            if jaulaAEliminar:
                res = cages.delete(id)
                if res == 1:
                    print("Se ha eliminado la jaula correctamente.")
                    self.guardarEnJSON()
                    # SE GUARDA EN LA COLECCIÓN CORRESPONDIENTE
                    #query = {"Nombre": funcionAEliminar.nombre}
                    #self.mongodb_connection.delete_document(query)
                    #print("Se ha eliminado de MongoDB")
                else:
                    print("Hubo un error al eliminar la jaula.")
            else:
                print("ID de la jaula inválido.")

    def guardarEnJSON(self):
        if self.guardarInJson:
            diccionario_obj = self.instanciaCage.diccionario()
            self.instanciaCage.guardar(diccionario_obj)
        else:
            diccionario_obj = self.instancia.diccionario()
            self.instancia.guardar(diccionario_obj)

    def interfaz(self):
        print("\n-------------JAULAS-----------")
        while True:
            print("\nSeleccione qué desea realizar:")
            print("1. Crear")
            print("2. Mostrar")
            print("3. Actualizar")
            print("4. Eliminar")
            print("5. Salir")
            operation = input("Operación a realizar: ")

            if operation == "1":  # CREAR
                self.createCage()
            elif operation == "2":  # MOSTRAR
                self.readCages()
            # elif operation == "3":  # ACTUALIZAR
                # self.updateUser()
            elif operation == "4":  # ELIMINAR
                self.deleteCage()
            elif operation == "5":
                print("Saliendo del programa. ¡Hasta pronto!")
                break
            else:
                print("Opción no válida. Intente de nuevo.")
                continue


if __name__ == "__main__":
    instancia = CagesInterface()
    instancia.interfaz()
