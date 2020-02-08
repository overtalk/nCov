import pymongo


class Config:
    host = ''
    port = ''
    db = ''

    def __init__(self, db, host='127.0.0.1', port=27017):
        self.db = db
        self.port = port
        self.host = host


class MongoDB:
    config = Config
    db = pymongo.MongoReplicaSetClient

    def __init__(self, c):
        self.config = c
        self.db = pymongo.MongoClient(host=c.host, port=c.port)[c.db]

    def insert(self, table, *items):
        self.db[table].insert_many(items)

    def find_one(self, table, **conditions):
        result = self.db[table].find_one(conditions)
        print(result)

    def find(self, table, **conditions):
        results = self.db[table].find(conditions)
        for result in results:
            print(result)

    def update(self, table, conditions, update):
        results = self.db[table].update_one(conditions, update)
        print(results)

    def del_one(self, table, conditions):
        results = self.db[table].delete_one(conditions)
        print(results)
