import json
from os import path

def _save(dbFilePath, workers):
    def map_worker(w): return w.to_dict()
    file = open(dbFilePath, "w")        
    file.write(json.dumps(list(map(map_worker, workers.values()))))
    file.close()

class Storage:
    _workers = {}
    _dbFilePath = ""

    def load(dbFilePath):
        Storage._dbFilePath = dbFilePath

        if not path.isfile(Storage._dbFilePath): return
        file = open(Storage._dbFilePath, "r")
        json_content = file.read()
        file.close()

        items = json.loads(json_content)
        for itm in items:
            w = Worker(itm["name"], itm["age"], "")
            w._id = int(itm["id"])
            Storage._workers[w._id] = w

    def add(worker):
        max_id = 0
        if len(Storage._workers) > 0:
            max_id = max(Storage._workers.keys())

        worker._id = max_id + 1        
        Storage._workers[worker.id] = worker
        Storage.save()

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
        Storage.save()

    def save():
        _save(Storage._dbFilePath, Storage._workers)


class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self._id = 0

    @property
    def id(self):
        return self._id

    def __str__(self):
        return "name={0},age={1}".format(self.name, self.age)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age
        }

class Worker(Person):
    def __init__(self, name, age, position):
        super(Worker, self).__init__(name, age)
        self.position = position

    def __str__(self):
        return "name={0},age={1},position={2}".format(self.name, self.age, self.position)