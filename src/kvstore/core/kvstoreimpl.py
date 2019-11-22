# used for storing information in the cluster (still not fully implemented
class KvStore:

    def __init__(self):
        self.committed_data = {}

    def set_string(self, key, value):
        print("Kv to add: " + key + " : " + value)
        self.committed_data[key] = value

    def get_string(self, key):
        return self.committed_data[key]
