class Node:

    def __init__(self, Id, Download, Upload, incentive, region_id, region_name):
        self.nodeId = Id
        self.Download_bandwidth = Download
        self.Upload_bandwidth = Upload
        self.Incentive = incentive
        self.Region_Id = region_id
        self.Region_Name = region_name
        self.Peer_list = []
        self.Message_received = []

