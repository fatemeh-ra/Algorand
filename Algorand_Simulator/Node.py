from Network import *
from Event import Event
from Tree import Contribution_Tree
from math import floor
import Config
import hashlib
import secrets
import random
import copy


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
        self.Received_Time = None

        self.Is_Agent = False
        self.Agent_list = []

        self.Sent_Gossip_Messages = []
        self.Block_Source_Node = None
        self.final_reward_set = []

    def __str__(self):
        return str(self.Node_Id)

    def propose_block(self, event):
        prev_block = self.Block_Chain[len(self.Block_Chain) - 1]
        prev_block_hash = hashlib.sha256(prev_block.__str__().encode()).hexdigest()
        new_block_content = secrets.randbits(256)

        new_block_msg = Block_Propose_Msg.new_message(prev_block_hash, new_block_content, self)

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
            # check path for zero credit nodes

            if event.Event_Time < 0 : exit()
            path = event.Msg_To_Deliver.Source_List
            for node in path:
                if node.Credit == 0:
                    return

            Config.Node_Log.write(str(self)+" "+str(event.Event_Time)+" "+str(self.Region_Id)+" "
                                  +str(len(event.Msg_To_Deliver.Source_List))+" "+str(len(self.Peer_list))+'\n')


            self.Received_Time = event.Event_Time
            # add message to list
            self.Incoming_Block = event.Msg_To_Deliver.Block
            self.Received_New_Block = True

            # agent check
            r = random.random()
            time = event.Event_Time
            if 1 <= event.Msg_To_Deliver.Agent_Probability: # * (1 - (time/60000) ** 2):
                self.Is_Agent = True
                Agents.append(self)

            # Block gossip
            agent_flag = False
            D = 0
            for peer in self.Peer_list:
                delay = Config.LATENCY[self.Region_Id][peer.Region_Id] + floor((Config.BLOCK_SIZE/232)*0.113) + \
                        floor(Config.BLOCK_SIZE*8 / (min(self.Upload_bandwidth, peer.Download_bandwidth) / 1000)) + D
                D += floor(Config.BLOCK_SIZE*8 / (min(self.Upload_bandwidth, peer.Download_bandwidth) / 1000))

                if event.Event_Time + delay - event.Ref_Time < event.Time_Out and peer.Received_New_Block == False:
                    agent_flag = True
                    new_message = Block_Propose_Msg.relay_message(event.Msg_To_Deliver,
                                                                  event.Event_Time - event.Ref_Time + delay)
                    new_message.add_source_node(self)
                    if self.Is_Agent:
                        new_message.change_agent(self)
                        new_message.reset_probability()
                    self.send_msg(event, peer, delay, new_message)
                else:
                    pass

            # new events
            if self.Is_Agent and agent_flag == False:
                self.Is_Agent = False

            if self.Is_Agent:
                new_event = Event(event.Ref_Time + Config.BLOCK_GOSSIP_TIME_OUT,
                                  event.Ref_Time + Config.BLOCK_GOSSIP_TIME_OUT,
                                  Event_Type.AGENT_AGGREGATION_EVENT,
                                  None,
                                  Config.SOURCE_GOSSIP_TIME_OUT,
                                  self,
                                  self,
                                  event.Round_Number,
                                  event.Step_Number)
                EventQ.add(new_event)
                self.Block_Source_Node = event.Source_Node
                new_source_gossip_msg = Source_Gossip_Msg(self, event.Source_Node)

                Config.Source_Msg_Log.write(str(new_source_gossip_msg))
                self.Agent_list.append(new_source_gossip_msg)
            else:
                # make event for source node proposal
                self.Block_Source_Node = event.Source_Node
                new_source_gossip_msg = Source_Gossip_Msg(self, event.Source_Node)
                Config.Source_Msg_Log.write(str(new_source_gossip_msg))

                new_event = Event(event.Ref_Time,
                                  event.Event_Time,
                                  Event_Type.AGENT_MESSAGE_EVENT,
                                  new_source_gossip_msg,
                                  Config.SOURCE_GOSSIP_TIME_OUT,
                                  event.Msg_To_Deliver.Selected_Agent,
                                  self,
                                  event.Round_Number,
                                  event.Step_Number)
                EventQ.add(new_event)

            new_event = Event(event.Ref_Time + Config.BLOCK_GOSSIP_TIME_OUT + Config.SOURCE_GOSSIP_TIME_OUT,
                              event.Ref_Time + Config.BLOCK_GOSSIP_TIME_OUT + Config.SOURCE_GOSSIP_TIME_OUT,
                              Event_Type.FINAL_RESULT_EVENT,
                              No_Message(),
                              Config.TIME_OUT_NOT_APPLICABLE,
                              self,
                              self,
                              event.Round_Number,
                              event.Step_Number)
            # EventQ.add(new_event)

        else:
            pass

    def agent_receive_message(self, event):
        self.Agent_list.append(event.Msg_To_Deliver)

    def agent_aggregation(self, event):
        # print(str(self) + " is agent of", len(self.Agent_list), "nodes")
        Config.Agent_Log.write(str(self)+" "+str(self.Received_Time)+" "+str(len(self.Agent_list))+'\n')
        for peer in self.Peer_list:
            new_event = Event(event.Ref_Time,
                              event.Event_Time + Config.LATENCY[self.Region_Id][peer.Region_Id],
                              Event_Type.SOURCE_NODE_GOSSIP_EVENT,
                              self.Agent_list,
                              Config.SOURCE_GOSSIP_TIME_OUT,
                              peer,
                              self,
                              event.Round_Number,
                              event.Step_Number)
            EventQ.add(new_event)

    def send_source_node_gossip(self, event):
        if event.Msg_To_Deliver in self.Sent_Gossip_Messages:
            return

        self.Sent_Gossip_Messages.append(event.Msg_To_Deliver)

        # random_node_cnt = 0
        # while random_node_cnt < Config.GOSSIP_FAN_OUT:
        #     random_node = random.choice(All_Nodes)
        #     if random_node != self and (random_node not in self.Peer_list):
        #         self.Peer_list.append(random_node)
        #         random_node_cnt = random_node_cnt + 1

        for peer in self.Peer_list:
            self.send_msg(event, peer, Config.LATENCY[self.Region_Id][peer.Region_Id], event.Msg_To_Deliver)

        # self.Peer_list.clear()

    def compute_final_result(self):
        tree = Contribution_Tree(self.Sent_Gossip_Messages)
        tree.compute_score(tree.root)
        self.final_reward_set = tree.deepening_choose()

        print("DAG created for Node " + str(self) + " Nodes in Final Result:")
        for k in self.final_reward_set:
            print(str(k) + ", ", end='')

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
