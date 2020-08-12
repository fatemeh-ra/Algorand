from Network import *
from Node import *
from Event import *
import Config
import sys


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
        print("Event Type is not recognised")


def handler(signum, frame):
    print("Simulation terminated manually")
    sys.exit()


if __name__ == "__main__":
    init_network('graph1_100.txt')

    proposer_node_id = np.random.random(Num_of_Nodes)
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

    while len(EventQ):
        ev = EventQ.pop(0)
        execute_event(ev)

    print("Simulation Completed!")
