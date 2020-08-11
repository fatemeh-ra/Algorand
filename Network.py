import json
import numpy as np
from Node import *
from sortedcontainers import SortedList
from enum import Enum

Num_of_Nodes = 0
All_Nodes = []
Block_Delays = []
EventQ = SortedList()


class EventType(int, Enum):
    BLOCK_PROPOSE_EVENT = 1
    BLOCK_GOSSIP_EVENT = 2
    SOURCE_NODE_GOSSIP_EVENT = 3
    FINAL_RESULT_EVENT = 4


def init_Network(path):
    file = open(path, 'r')
    General_Info = json.loads(file.readline())
    Num_of_Nodes = General_Info['Num_of_Nodes']

    for i in range(Num_of_Nodes):
        Info = json.loads(file.readline())
        incentive = np.random.random()
        N = Node(i, Info['Download'], Info['Upload'], incentive, Info['Region_id'], Info['Region_name'])
        All_Nodes.append(N)

    for i in range(Num_of_Nodes):
        for j in range(Num_of_Nodes):
            delay = [int(x) for x in file.readline().split()]
            Block_Delays.append(delay)
