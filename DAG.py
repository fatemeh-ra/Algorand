from Network import *

Visited = []
Credit = {}


def Construct_DAG(Sent_Gossip_Messages):
    DAG_edge = [[] for i in range(Num_of_Nodes)]
    for m in Sent_Gossip_Messages:
        DAG_edge[m.Sender_Node.Node_Id].append(m.Receiver_Node.Node_Id)
        if m.Sender_Node == m.Receiver_Node:
            DAG_root = m.Sender_Node.Node_Id

    Visited = [0 for i in range(Num_of_Nodes)]
    Compute_DAG_Credits(DAG_edge, DAG_root)
    return Credit


def Compute_DAG_Credits(DAG_edge, currant):
    total_credit = All_Nodes[currant].credit
    for i in DAG_edge[currant]:
        if not Visited[i]:
            Compute_DAG_Credits(DAG_edge, i)
        total_credit += Credit[i]
    Credit[currant] = total_credit

