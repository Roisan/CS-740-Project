from time import sleep
# from typing import Any, List


class Node:
    def __init__(self, id1):
        self.id = id1
        self.role = 'follower'
        self.cur_term = 0
        self.vote = None
        self.log = []
        self.election_timeout = 0

    def req_vote(self, c_id, term):
        # update term
        # print(f"Voted for {self.vote}")
        if term > self.cur_term:
            self.cur_term = term
            self.role = 'follower'
        # check if node voted for given candidate
        if term == self.cur_term and (self.vote is None or self.vote == c_id):
            # print(f"Node{self.id} voted for {c_id}")
            self.vote = c_id
            return True
        return False

    def app_entries(self, term, prev_log_index, entries):
        if term >= self.cur_term:
            self.cur_term = term
            # reset vote
            self.vote = None
            self.role = 'follower'
            # check if logs are recently updated
            if prev_log_index >= len(self.log):  # or self.log[prev_log_index.term!=entries[0].term]:
                return False
            self.log = self.log[:prev_log_index + 1] + entries
            # print(f"Entries appended for {self.id}")
            return True
        return False

    def change_leader(self):
        self.role = 'leader'

    def dup_log(self, log=0):
        if self.role == 'leader':
            # simulate log creation
            print(f"Leader {self.id} added Entry {log} .. Replicating to followers")
            sleep(1)
            self.log.append(f"Entry {log}")
            for node in nodes:
                if node.id != self.id:
                    match_index = min(len(self.log) - 1, len(node.log) - 1)
                    entries = self.log[match_index + 1:]
                    if len(entries) > 0:
                        # append entries and validate success
                        success = node.app_entries(self.cur_term, match_index, entries)
                        if not success:
                            self.role = "follower"

    def get_match_index(self):
        return len(self.log) - 1


nodes = [Node(i) for i in range(5)]


class Raft:
    def __init__(self, cur_nodes):
        self.nodes = cur_nodes

    def start_election(self):
        print(f"Election starting for term {self.nodes[0].cur_term+1}")
        candidates = [-1, -1]
        for node in self.nodes:
            if node.role == "leader":
                node.role = "follower"

        print(f"Enter two candidates to contest (0-4):")
        candidates[0] = nodes[int(input())]
        candidates[1] = nodes[int(input())]
        candidates[0].vote = candidates[0].id
        candidates[1].vote = candidates[1].id

        for node in self.nodes:
            if node != candidates[0] and node != candidates[1]:
                print(f"Enter the vote id for voter{node.id}:")
                node.vote = int(input())
        for candidate in candidates:
            # candidate = random.choice(self.nodes)
            print(f"For candidate{candidate.id}")
            candidate.cur_term += 1
            candidate.role = "candidate"
            candidate.vote = candidate.id

            votes = [candidate.id]
            for node in self.nodes:
                if node.id != candidates[0].id and node.id != candidates[1].id:
                    vote_granted = node.req_vote(candidate.id, candidate.cur_term)
                    if vote_granted:
                        votes.append(node.id)

            print(f"No of votes={len(votes)}")
            if len(votes) > len(self.nodes) // 2:
                candidate.change_leader()
                print(f"Node {candidate.id} is elected leader")
                for node in self.nodes:
                    node.election_timeout = 5
                return True
            else:
                candidate.role = "follower"
        return False

    def handle_messages(self, log):
        election_done = False
        for node in self.nodes:
            node.election_timeout -= 1
            if node.election_timeout > 0:
                election_done = True
            if node.election_timeout <= 0:
                while not election_done:
                    election_done = self.start_election()
            if node.role == "leader":
                node.dup_log(log)
            elif node.role == "candidate":
                if node.election_timeout <= 0:
                    node.role = "follower"
                    node.vote = None

    def main_loop(self):
        log = -1
        for i in range(6):
            log += 1
            self.handle_messages(log)
            '''
            commit_index=self.nodes[0].get_commit_index()
            for i in range(len(self.nodes)):
                while len(self.nodes[i].log)>commit_index and self.nodes[i].log[commit_index].term==self.nodes[i]
                .cur_term:
                    commit_index+=1
            for i in range(commit_index):
                for node in self.nodes:
                    print(f"Node{node.id}: {node.log[i].value}")
                    '''
            for node in self.nodes:
                print(f"Node:{node.id}, Term:{node.cur_term}, Role:{node.role}, Log:{node.log}")


raft = Raft(nodes)
raft.main_loop()
