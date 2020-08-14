from Network import *
from Event import Event
from DAG import Construct_DAG
import Config
import hashlib
import secrets
import random


class Node(object):

    def __init__(self, Id, Download, Upload, incentive, region_id, region_name, prev_block, credit):
        self.Node_Id = Id
        self.Download_bandwidth = Download
        self.Upload_bandwidth = Upload
        self.Incentive = incentive
        self.Region_Id = region_id
        self.Region_Name = region_name
        self.Credit = credit
        self.Peer_list = []
        # self.Message_received = []
        self.Block_Chain = [prev_block]
        self.Incoming_Block = None
        self.Received_New_Block = False

        self.Sent_Gossip_Messages = []
        self.Block_Source_Node = None

    def __str__(self):
        return str(self.Node_Id)

    def propose_block(self, event):
        prev_block = self.Block_Chain[len(self.Block_Chain) - 1]
        prev_block_hash = hashlib.sha256(prev_block.__str__().encode()).hexdigest()
        new_block_content = secrets.randbits(256)

        new_block_msg = Block_Propose_Msg(prev_block_hash, new_block_content)

        new_event = Event(event.Ref_Time,
                          event.Event_Time,
                          Event_Type.BLOCK_GOSSIP_EVENT,
                          new_block_msg,
                          Config.BLOCK_GOSSIP_TIME_OUT,
                          self,
                          self,
                          event.Round_Number,
                          event.Step_Number)

        EventQ.add(new_event)

    def send_block_gossip(self, event):
        if not self.Received_New_Block:
            path = event.Msg_To_Deliver.Source_List
            for node in path:
                if node.Credit == 0:
                    return

            self.Incoming_Block = event.Msg_To_Deliver.block
            self.Received_New_Block = True

            self.Block_Source_Node = event.Source_Node
            new_source_gossip_msg = Source_Gossip_Msg(self, event.Source_Node)

            new_event = Event(event.Ref_Time + Config.BLOCK_GOSSIP_TIME_OUT,
                              event.Ref_Time + Config.BLOCK_GOSSIP_TIME_OUT,
                              Event_Type.SOURCE_NODE_GOSSIP_EVENT,
                              new_source_gossip_msg,
                              Config.SOURCE_GOSSIP_TIME_OUT,
                              self,
                              self,
                              event.Round_Number,
                              event.Step_Number)
            EventQ.add(new_event)

            message = event.Msg_To_Deliver

            random_node_cnt = 0
            while random_node_cnt < Config.NODE_AVERAGE_LINKS * self.Incentive:
                random_node = random.choice(All_Nodes)
                if random_node != self and (random_node not in self.Peer_list):
                    if random_node not in message.Source_List:
                        self.Peer_list.append(random_node)
                        random_node_cnt = random_node_cnt + 1

            message.Add_Source_Node(self)
            for peer in self.Peer_list:
                if event.Event_Time + Block_Delays[self.Node_Id][peer.Node_Id] - event.Ref_Time < event.Time_Out:
                    self.send_msg(event, peer, Block_Delays[self.Node_Id][peer.Node_Id], message)
                else:
                    pass

            self.Peer_list.clear()

    def send_source_node_gossip(self, event):
        if event.Msg_To_Deliver in self.Sent_Gossip_Messages:
            return

        self.Sent_Gossip_Messages.append(event.Msg_To_Deliver)

        random_node_cnt = 0
        while random_node_cnt < Config.GOSSIP_FAN_OUT:
            random_node = random.choice(All_Nodes)
            if random_node != self and (random_node not in self.Peer_list):
                self.Peer_list.append(random_node)
                random_node_cnt = random_node_cnt + 1

        for peer in self.Peer_list:
            self.send_msg(event, peer, 0, event.Msg_To_Deliver)

        self.Peer_list.clear()

        if len(self.Sent_Gossip_Messages) == 1:
            new_event = Event(event.Ref_Time + Config.SOURCE_GOSSIP_TIME_OUT,
                              event.Ref_Time + Config.SOURCE_GOSSIP_TIME_OUT,
                              Event_Type.FINAL_RESULT_EVENT,
                              No_Message(),
                              Config.TIME_OUT_NOT_APPLICABLE,
                              self,
                              self,
                              event.Round_Number,
                              event.Step_Number)
            EventQ.add(new_event)

    def compute_final_result(self):
        credits = Construct_DAG(self.Sent_Gossip_Messages)
        sorted_credits = sorted(credits.items(), key=lambda x: x[1], reverse=True)
        c = 0
        print("DAG created for Node " + str(self) + "Nodes in Final Result:")
        for k, v in sorted_credits:
            if c < Config.DAG_MAX_NODE:
                print(str(k) + " with total credit = " + str(v))
            else:
                break
            c += 1

    def send_msg(self, event, dstNode, deltaTime, msg):
        new_event = Event(event.Ref_Time,
                          event.Event_Time + deltaTime,
                          event.Event_Type,
                          msg,
                          event.Time_Out,
                          dstNode,
                          self,
                          event.Round_Number,
                          event.Step_Number)

        EventQ.add(new_event)
