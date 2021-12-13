# !/bin/python3

from sortedcontainers import SortedList
from enum import Enum
import copy
import Config

Num_of_Nodes = 0
All_Nodes = []
Delays = []
EventQ = SortedList([])
Agents = []


class Event_Type(int, Enum):
    BLOCK_PROPOSE_EVENT = 1
    BLOCK_GOSSIP_EVENT = 2
    AGENT_MESSAGE_EVENT = 3
    AGENT_AGGREGATION_EVENT = 4
    SOURCE_NODE_GOSSIP_EVENT = 5
    FINAL_RESULT_EVENT = 6


class Block(object):
    def __init__(self, randomString, prevBlockHash=None):
        self.transactions = randomString
        self.prevBlockHash = prevBlockHash

    def __str__(self):
        return "transactions = " + str(self.transactions) + "\t" + "prevBlockHash = " + str(self.prevBlockHash)


class Block_Propose_Msg(object):
    def __init__(self, block, source_list, selected_agent, prob=0.0):
        self.Block = block
        self.Source_List = source_list
        self.Selected_Agent = selected_agent
        self.Agent_Probability = prob

    @classmethod
    def new_message(cls, prevBlockHash, thisBlockContent, agent):
        block = Block(thisBlockContent, prevBlockHash)
        return cls(block, [], agent, 0)

    @classmethod
    def relay_message(cls, Msg, time):
        tmp = 1
        if len(Msg.Source_List) > 1 : tmp = 0
        if time > 40000 : tmp = 0
        return cls(Msg.Block, copy.copy(Msg.Source_List), Msg.Selected_Agent,
                   (Msg.Agent_Probability + (Config.AGENT_PROBABILITY_INCREASE))*tmp)
                   # (1 - ((time / 40000) ** 3)))*tmp)   #  - (len(Msg.Source_List)**1.5/100)

    def __str__(self):
        STR = [str(i) for i in self.Source_List]
        return "Source list = " + str(STR) + ", Agent = " + str(self.Selected_Agent) + " "

    def add_source_node(self, node):
        self.Source_List.append(node)

    def change_agent(self, agent):
        self.Selected_Agent = agent

    def reset_probability(self):
        self.Agent_Probability = 1


class Source_Gossip_Msg(object):
    def __init__(self, Receiver, Sender):
        self.Receiver_Node = Receiver
        self.Sender_Node = Sender

    def __str__(self):
        return "Gossip message " + "block from " + str(self.Sender_Node) + " to " + str(self.Receiver_Node) + "\n"


class No_Message(object):
    def __init__(self):
        pass

    def __str__(self):
        return "No Message\n"
