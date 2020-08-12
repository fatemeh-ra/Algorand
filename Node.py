from Network import *
from Event import Event
import Config
import hashlib
import secrets


class Node(object):

    def __init__(self, Id, Download, Upload, incentive, region_id, region_name):
        self.Node_Id = Id
        self.Download_bandwidth = Download
        self.Upload_bandwidth = Upload
        self.Incentive = incentive
        self.Region_Id = region_id
        self.Region_Name = region_name
        self.Peer_list = []
        # self.Message_received = []
        self.Block_Chain = []
        self.Incoming_Block = []

        self.Sent_Gossip_Messages = []
        self.Block_Source_Nodes = []

    def propose_block(self, event):
        prev_block = self.Block_Chain[len(self.Block_Chain) - 1]
        prev_block_hash = hashlib.sha256(prev_block.__str__().encode()).hexdigest()
        new_block_content = secrets.randbits(256)

        new_block_msg = Block_Propose_Msg(prev_block_hash, new_block_content)

        new_event = Event(event.evTime,
                          event.evTime,
                          Event_Type.BLOCK_GOSSIP_EVENT,
                          new_block_msg,
                          Config.BLOCK_GOSSIP_TIME_OUT,
                          self,
                          self,
                          event.Round_Number,
                          event.Step_Number)

        EventQ.add(new_event)

    def send_block_gossip(self):
        # TODO
        pass

    def send_source_node_gossip(self):
        pass
        # TODO

    def compute_final_result(self):
        # TODO
        pass
