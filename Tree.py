from Network import *
import Config


class Contribution_Tree(object):

    def __init__(self, Sent_Gossip_Messages):
        self.tree_edges = [[] for i in range(len(All_Nodes))]
        self.sender_set = set()
        for m in Sent_Gossip_Messages:
            self.sender_set.add(m.Sender_Node.Node_Id)
            if m.Sender_Node == m.Receiver_Node:
                self.root = m.Sender_Node.Node_Id
                continue
            x = m.Sender_Node.Node_Id
            self.tree_edges[x].append(m.Receiver_Node.Node_Id)
        self.Visited = [0 for i in range(len(All_Nodes))]
        self.Score = {}

    def compute_score(self, currant):
        total_score = 0
        for i in self.tree_edges[currant]:
            if not self.Visited[i]:
                self.Visited[i] = 1
                self.compute_score(i)
            total_score += self.Score[i]
            total_score += All_Nodes[i].Credit
        self.Score[currant] = total_score

    def deepening_choose(self):
        self.Visited = [0 for i in range(len(All_Nodes))]
        currant = self.root
        node_cntr = 0
        result = []

        while node_cntr < Config.TREE_MAX_NODE:
            max_tmp = -1
            tmp = -1
            for i in self.tree_edges[currant]:
                if self.Score[i] > 0 and self.Score[i] > max_tmp and self.Visited[i] == 0:
                    max_tmp = self.Score[i]
                    tmp = i
            if tmp == -1:
                currant = self.root
                continue
            result.append(tmp)
            node_cntr += 1
            currant = tmp
            self.Visited[tmp] = 1

        return result

    def iterative_deepening_choose(self):
        self.Visited = [0 for i in range(len(All_Nodes))]
        currant = self.root
        node_cntr = 0
        stack = []
        result = []

        while node_cntr < Config.TREE_MAX_NODE:
            max_tmp = -1
            tmp = -1
            for i in self.tree_edges[currant]:
                if self.Score[i] > 0 and self.Score[i] > max_tmp and self.Visited[i] == 0:
                    max_tmp = self.Score[i]
                    tmp = i
            if tmp == -1:
                currant = stack.pop()
                continue
            result.append(tmp)
            node_cntr += 1
            currant = tmp
            self.Visited[tmp] = 1

        return result

    def not_leaves_choose(self):
        return self.sender_set
