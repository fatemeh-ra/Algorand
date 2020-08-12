from Network import *

Visited = []
Credit = {}


def Construct_DAG(Sent_Gossip_Messages):
    DAG_edge = [[] for i in range(len(All_Nodes))]
    for m in Sent_Gossip_Messages:
        if m.Sender_Node == m.Receiver_Node:
            DAG_root = m.Sender_Node.Node_Id
            continue
        x = m.Sender_Node.Node_Id
        DAG_edge[x].append(m.Receiver_Node.Node_Id)

    global Visited
    Visited = [0 for i in range(len(All_Nodes))]
    Compute_DAG_Credits(DAG_edge, DAG_root)
    return Credit


def Compute_DAG_Credits(DAG_edge, currant):
    global Credit
    total_credit = All_Nodes[currant].Credit
    for i in DAG_edge[currant]:
        if not Visited[i]:
            Visited[i] = 1
            Compute_DAG_Credits(DAG_edge, i)
        total_credit += Credit[i]
    Credit[currant] = total_credit

