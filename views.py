from models import Storage, Worker

class BaseView(object):
    def __init__(self, model=None):
        self._model = model

    def render(self):
        raise NotImplementedError()

    def action(selft):
        raise NotImplementedError()

class MainView(BaseView):
    def render(self):
        print("===Menu===")
        print("1. Workers")
        
        print("\nq. Exit")

    def action(self, option):
        if option == "q":
            return BaseView()

        if option == "1":
            return ListView(Storage.all())

        return None

class ListView(BaseView):
    def render(self):
        print("===List===")
        
        if len(self._model) == 0:
            print("(empty)")
        else:
            for w in self._model:
                print("{0}. {1}".format(w.id, w.name))
        
        print("\na. Add")
        print("b. Back")        

    def action(self, option):
        try:
            id = int(option)
            model = Storage.get(id)
            if not model:
                return None

            return DetailsView(model)
        except ValueError:            
            if option == "b":
                return MainView()
            if option == "a":
                return AddView()
        
        return None

class AddView(BaseView):
    def __init__(self):
        self._tempWorker = None

    def render(self):
        print("===Add===")
        
        if not self._tempWorker:
            name = input("\nName: ")
            age = input("Age: ")
            self._tempWorker = Worker(name, age, "")

        print("\nAdd {0}? (y/n)".format(self._tempWorker.name))

    def action(self, option):  
        if option == "y":
            Storage.add(self._tempWorker)
       
        if option == "y" or option == "n":
            self._tempWorker = None
            return ListView(Storage.all())

        return None
        
class DetailsView(BaseView):
    def __init__(self, model):
        super(DetailsView, self).__init__(model)
        self._deleting = False

    def render(self):
        print("===Details of {0.name}===".format(self._model))
        print("Name: {0.name}\nAge: {0.age}".format(self._model))

        if self._deleting:
            print("\nAre you sure? (y/n)")
        else:
            print("\nd. Delete")
            print("b. Back")

    def action(self, option):
        if option == "b":
            return ListView(Storage.all())
        if option == "d":
            self._deleting = True

        if self._deleting and option == "y":
            Storage.delete(self._model.id)
            return ListView(Storage.all())
        if self._deleting and option == "n":
            self._deleting = False
        
        return None