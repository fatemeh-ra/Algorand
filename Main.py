from Node import *
from Event import *
import Config
import sys
from math import floor
import json
import numpy as np


def execute_event(event):
    event_type = event.Event_Type
    target_node = event.Target_Node

    if event_type == Event_Type.BLOCK_PROPOSE_EVENT:
        target_node.propose_block(event)

    elif event_type == Event_Type.BLOCK_GOSSIP_EVENT:
        target_node.send_block_gossip(event)

    elif event_type == Event_Type.SOURCE_NODE_GOSSIP_EVENT:
        target_node.send_source_node_gossip(event)

    elif event_type == Event_Type.FINAL_RESULT_EVENT:
        target_node.compute_final_result()

    else:
        print("Event Type is not recognized")


def handler(signum, frame):
    print("Simulation terminated manually")
    sys.exit()


def init_network(path):
    global Num_of_Nodes
    file = open(path, 'r')
    general_info = json.loads(file.readline())
    Num_of_Nodes = general_info['Num_of_Nodes']
    prev_block = general_info['Prev_Block']

    for i in range(Num_of_Nodes):
        info = json.loads(file.readline())
        incentive = np.random.random()
        n = Node(i, info['Download'], info['Upload'], incentive, info['Region_id'] - 1
                 , info['Region_name'], prev_block, info['Credit'])
        All_Nodes.append(n)

    # for i in range(Num_of_Nodes):
    #     for j in range(Num_of_Nodes):
    #         delay = [int(x) for x in file.readline().split()]
    #         Delays.append(delay)


if __name__ == "__main__":
    init_network('graph1_50000.txt')
    print("Hello! Simulation Started!\n" + "Using "+str(Num_of_Nodes)+" in this Simulation")

    proposer_node_id = floor(np.random.random()*Num_of_Nodes)
    node = All_Nodes[proposer_node_id]
    event = Event(0,
                  0,
                  Event_Type.BLOCK_PROPOSE_EVENT,
                  No_Message(),
                  Config.TIME_OUT_NOT_APPLICABLE,
                  node,
                  node,
                  1,
                  0)
    EventQ.add(event)
    node.Incentive = 1
    print("root : ", proposer_node_id)

    file = open("log.txt", "w")
    while len(EventQ):
        ev = EventQ.pop(0)
        file.write(str(ev) + '\n')
        execute_event(ev)

    print("Simulation Completed!")
