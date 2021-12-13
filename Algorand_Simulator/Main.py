from Node import *
from Event import *
import Config
import sys
import os
from math import floor
import json
import numpy as np

cnt = 0

def execute_event(event):
    event_type = event.Event_Type
    target_node = event.Target_Node

    if event_type == Event_Type.BLOCK_PROPOSE_EVENT:
        target_node.propose_block(event)

    elif event_type == Event_Type.BLOCK_GOSSIP_EVENT:
        target_node.send_block_gossip(event)

    elif event_type == Event_Type.AGENT_MESSAGE_EVENT:
        global cnt
        cnt += 1
        target_node.agent_receive_message(event)

    elif event_type == Event_Type.AGENT_AGGREGATION_EVENT:
        target_node.agent_aggregation(event)
        # pass

    elif event_type == Event_Type.SOURCE_NODE_GOSSIP_EVENT:
        # target_node.send_source_node_gossip(event)
        pass

    elif event_type == Event_Type.FINAL_RESULT_EVENT:
        target_node.compute_final_result()

    else:
        print("Event Type is not recognized")


def handler(signum, frame):
    print("Simulation terminated manually")
    sys.exit()


def init_network():
    global Num_of_Nodes
    file = open(Config.Network_Path, 'r')
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

    for node in All_Nodes:
        potential_list = {}
        random_node_cnt = 0
        while random_node_cnt < Config.NODE_POTENTIAL_PEER_COUNT:
            random_node = random.choice(All_Nodes)
            if random_node not in potential_list:
                potential_list[random_node] = Config.LATENCY[node.Region_Id][random_node.Region_Id]
                random_node_cnt = random_node_cnt + 1

        cnt = 0
        for i in sorted(potential_list.items(), key=lambda x: x[1]):
            node.Peer_list.append(i[0])
            i[0].Peer_list.append(node)
            cnt += 1
            if cnt == Config.NODE_AVERAGE_LINKS/2:
                break

    # agent_list = []
    # random_node_cnt = 0
    # while random_node_cnt < Config.NUM_OF_AGENT_NODES:
    #     random_node = random.choice(All_Nodes)
    #     if random_node not in agent_list:
    #         agent_list.append(random_node)
    #         random_node.Is_Agent = True
    #         random_node_cnt = random_node_cnt + 1
    #
    # str_agent = [str(i) for i in agent_list]
    # print("Agent list :", str_agent)


def init_paths():
    n = 1
    while(os.path.exists("Logs/Log_"+str(n))):
        n += 1
    Config.Main_Path = "Logs/Log_"+str(n)
    os.mkdir(Config.Main_Path)
    Event_Log_Path = Config.Main_Path + "/Event_Log.txt"
    Agent_Log_Path = Config.Main_Path + "/Agent_Log.txt"
    Source_Msg_Path = Config.Main_Path + "/Source_Msg_Log.txt"
    Node_Log_Path = Config.Main_Path + "/Node_Log.txt"
    Config.Network_Path = "Networks/" + Config.GRAPH + "_" + str(Config.NUM_OF_NODES) + ".txt"

    Config.Event_Log = open(Event_Log_Path, 'w')
    Config.Agent_Log = open(Agent_Log_Path, 'w')
    Config.Source_Msg_Log = open(Source_Msg_Path, 'w')
    Config.Node_Log = open(Node_Log_Path, 'w')


if __name__ == "__main__":
    init_paths()
    init_network()
    print("Hello! Simulation Started!\n" + "Using "+str(Num_of_Nodes)+" nodes in this Simulation")

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
    node.Is_Agent = True
    print("Proposer Node ID : ", proposer_node_id)

    while len(EventQ):
        ev = EventQ.pop(0)
        Config.Event_Log.write(str(ev) + '\n')
        execute_event(ev)

    # print(len(Agents), "Agents")
    # print(cnt)

    print("Simulation Completed!")
