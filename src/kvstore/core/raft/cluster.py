class Cluster:
    allNodes = []

    def __init__(self, nodes):
        self.allNodes = nodes

    # If there is a leader node, this functions returns all follower nodes for this node
    def get_remote_followers(self, leader_id):
        # if leader_id != self.return_node_leader():
        #   raise Exception('This leader is not in this cluster!')
        if leader_id in self.allNodes:
            return self.allNodes.remove(leader_id)
        return self.allNodes

    def start_all(self):
        for node in self.allNodes:
            node.start(self)

    def stop_all(self):
        for node in self.allNodes:
            node.stop()

    def stop_leader(self):
        leader = self.return_node_leader()
        leader.stop()
        return leader

    def return_node_leader(self):
        for node in self.allNodes:
            if node.is_leader():
                return node
        raise Exception('No leader in this cluster!')

    # Checks if the cluster is in a valid state
    def check(self):
        leader_count = 0
        follower_count = 0
        candidate_count = 0

        for node in self.allNodes:
            if node.is_follower():
                follower_count += 1
            elif node.is_leader():
                leader_count += 1
            elif node.is_candidate():
                candidate_count += 1
            else:
                raise Exception('Node is in an invalid state!')
        if leader_count > 1:
            raise Exception("there are multiple leaders in the cluster")
        elif leader_count == 0:
            raise Exception("there is no leader in the cluster")
        elif follower_count < len(self.allNodes) / 2:
            raise Exception("there are not enough followers -> split brain")

        return True, None
