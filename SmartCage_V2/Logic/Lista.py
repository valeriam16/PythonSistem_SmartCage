class Lista:
    def __init__(self):
        self.lista = []

    def create(self, obj):
        self.lista.append(obj)
        return 1

    def read(self):
        return self.lista

    def update(self, id, obj):
        for i, item in enumerate(self.lista):
            if item.ID == id:
                self.lista[i] = obj
                return 1
        return 0

    def search(self, id):
        for item in self.lista:
            if item.ID == id:
                return item
        return None

    def delete(self, id):
        obj_to_delete = self.search(id)
        if obj_to_delete:
            self.lista.remove(obj_to_delete)
            return 1
        else:
            return 0

    def __iter__(self):
        return iter(self.lista)
