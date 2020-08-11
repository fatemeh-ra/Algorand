
class Node:

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
        self.Sent_Gossip_Messages = []
        self.Incoming_Block = []

    def propose_block(self):
        # TODO
        pass

    def send_block_gossip(self):
        # TODO
        pass

    def send_source_node_gossip(self):
        pass
        # TODO

    def compute_final_result(self):
        # TODO
        pass

