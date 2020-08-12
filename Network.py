import json
import numpy as np
from Node import *
from sortedcontainers import SortedList
from enum import Enum

Num_of_Nodes = 0
All_Nodes = []
Block_Delays = []
EventQ = SortedList()


class Event_Type(int, Enum):
    BLOCK_PROPOSE_EVENT = 1
    BLOCK_GOSSIP_EVENT = 2
    SOURCE_NODE_GOSSIP_EVENT = 3
    FINAL_RESULT_EVENT = 4


def init_network(path):
    file = open(path, 'r')
    general_info = json.loads(file.readline())
    num_of_nodes = general_info['Num_of_Nodes']

    for i in range(num_of_nodes):
        info = json.loads(file.readline())
        incentive = np.random.random()
        n = Node(i, info['Download'], info['Upload'], incentive, info['Region_id'], info['Region_name'])
        All_Nodes.append(n)

    for i in range(num_of_nodes):
        for j in range(num_of_nodes):
            delay = [int(x) for x in file.readline().split()]
            Block_Delays.append(delay)


class No_Message(object):
    def __init__(self):
        pass
    @property
    def __str__(self):
        return '\n'.join(('{} = {}'.format(item, self.__dict__[item]) for item in self.__dict__))


