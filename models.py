import json
from os import path

def _save(workers):
    def map_worker(w): return w.to_dict()
    file = open("data.json", "w")        
    file.write(json.dumps(list(map(map_worker, workers.values()))))
    file.close()

class Storage:
    _workers = {}

    def load():
        if not path.isfile("data.json"): return
        file = open("data.json", "r")
        json_content = file.read()
        file.close()

        items = json.loads(json_content)
        for itm in items:
            Storage._workers[itm["id"]] = Worker(itm["name"], itm["age"], "")


    def add(worker):        
        Storage._workers[worker.id] = worker
        _save(Storage._workers)

    def count():
        return len(Storage._workers)

    def get(id):
        if not id in Storage._workers:
            return None
        return Storage._workers[id]

    def all():
        return Storage._workers.values()

    def delete(id):
        Storage._workers.pop(id)
        _save(Storage._workers)


class Person(object):
    def __init__(self, name, age):
        self._name = name
        self._age = age
        self._id = Storage.count() + 1

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @property
    def id(self):
        return self._id

    def __str__(self):
        return "name={0},age={1}".format(self._name, self._age)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age
        }

class Worker(Person):
    def __init__(self, name, age, position):
        super(Worker, self).__init__(name, age)
        self._position = position

    def __str__(self):
        return "name={0},age={1},position={2}".format(self._name, self._age, self._position)