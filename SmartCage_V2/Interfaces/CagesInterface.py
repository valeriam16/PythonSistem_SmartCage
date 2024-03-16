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
                print("No hay jaulas actualmente.")

            self.instancia = self.dataFileCage
            self.guardarInJson=False
        else:
            # CREA NUEVA FUNCIÓN, NO SE LE MANDA UNA INSTANCIA
            self.instanciaCage = Cages()

            if os.path.exists("../JSON/Cages.json") and os.path.getsize("../JSON/Cages.json") > 0:
                self.instanciaCage.cargar()
            else:
                print("No hay jaulas actualmente.")
            self.instancia = self.instanciaCage

            self.guardarInJson=True

    def seleccionarComoAgregar(self, cages=None):
        self.readCages(self.dataFileCage)
        id_jaula = int(input("ID de la jaula que desea asignar (-1 para crear uno nueva): "))

        if id_jaula == -1:
            # Crea una nueva jaula
            self.createCage(cages)
        else:
            # Obtener la jaula seleccionado
            jaula_asignada = self.dataFileCage.search(id_jaula)
            if jaula_asignada:
                self.instanciaCage.create(jaula_asignada)
            else:
                print("ID de la jaula inválido.")

        return self.instanciaCage

    def createCage(self, cages=None):
        if cages is None:
            cages = self.instanciaCage

        cageID = input("ID de la jaula: ")
        cage = Cages(cageID)
        res = cages.create(cage)

        if res == 1:
            print("Se ha creado la jaula correctamente.")
            #if self.guardarInJson == False:
                #self.instancia.create(sensor)
            self.guardarEnJSON()
            # SE GUARDA EN LA COLECCIÓN CORRESPONDIENTE
            #self.mongodb_connection.insert_document(obj.diccionario())
            #print("Se ha guardado en MongoDB")
        else:
            print("Hubo un error al crear la jaula.")
        return cage

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
    interfazJaulasInstancia = CagesInterface() # Forma 1
    # interfazFuncionesInstancia = InterfazFunciones_V2(Funciones()) #Forma 2 (Se va a comportar como una lista)
    interfazJaulasInstancia.interfaz()
