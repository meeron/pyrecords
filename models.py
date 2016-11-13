import json
from os import path
from security import Passwd

class Storage:
    _workers = {}
    _dbFilePath = ""
    _passwd = None
    is_new = False

    def load(dbFilePath, password):
        Storage._passwd = Passwd(password)
        Storage._dbFilePath = dbFilePath

        if not path.isfile(Storage._dbFilePath):
            Storage.is_new = True
            return True

        with open(Storage._dbFilePath, "rb") as f:
            json_content = Storage._passwd.decrypt(f.read())

        if json_content is None:
            return False

        items = json.loads(json_content)
        for itm in items:
            w = Worker(itm["name"], itm["age"], "")
            w._id = int(itm["id"])
            Storage._workers[w._id] = w

        return True

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
        def map_worker(w): return w.to_dict()
        
        with open(Storage._dbFilePath, "wb") as f:
            json_msg = json.dumps(list(map(map_worker, Storage._workers.values())))        
            f.write(Storage._passwd.encrypt(json_msg))

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