class KvStore:

    def __init__(self):
        self.committed_data = {}

    def setString(self, key, value):
        print("Kv to add: " + key + " : " + value)
        self.committed_data[key] = value

    def getString(self, key):
        return self.committed_data[key]
