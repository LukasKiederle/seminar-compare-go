class State:

    def __init__(self, state_id):
        self.state_id = state_id

    def __str__(self):
        switcher = {
            0: "FOLLOWER",
            1: "CANDIDATE",
            2: "LEADER",
        }
        return switcher.get(self.state_id, "Invalid State")
