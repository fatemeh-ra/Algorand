# !/bin/python3

from sortedcontainers import SortedList
from enum import Enum

Num_of_Nodes = 0
All_Nodes = []
Block_Delays = []
EventQ = SortedList([])


class Event_Type(int, Enum):
    BLOCK_PROPOSE_EVENT = 1
    BLOCK_GOSSIP_EVENT = 2
    SOURCE_NODE_GOSSIP_EVENT = 3
    FINAL_RESULT_EVENT = 4


class Block(object):
    def __init__(self, randomString, prevBlockHash=None):
        self.transactions = randomString
        self.prevBlockHash = prevBlockHash

    def __str__(self):
        return "transactions = " + str(self.transactions) + "\t" + "prevBlockHash = " + str(self.prevBlockHash)


class Block_Propose_Msg(object):
    def __init__(self, prevBlockHash, thisBlockContent):
        self.block = Block(thisBlockContent, prevBlockHash)
        # self.Source_Node = self
        self.Source_List = []

    def __str__(self):
        return "block propose message\n" + "block = " + str(self.block) + "\n"

    def Add_Source_Node(self, node):
        self.Source_List.append(node)


class Source_Gossip_Msg(object):
    def __init__(self, Receiver, Sender):
        self.Receiver_Node = Receiver
        self.Sender_Node = Sender

    def __str__(self):
        return "Gossip message\n" + "block from " + str(self.Sender_Node) + " to " + str(self.Receiver_Node) + "\n"


class No_Message(object):
    def __init__(self):
        pass

    def __str__(self):
        return "No Message\n"
