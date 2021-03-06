from graph_config import *
import numpy as np
import json
from math import floor
import secrets

Region_Ranges = REGION_DISTRIBUTION.copy()
tmp = 0
for i in range(len(Region_Ranges)):
    Region_Ranges[i] += tmp
    tmp = Region_Ranges[i]


Node_Region = []
Node_Download_Bandwidth = []
Node_Upload_bandwidth = []

Nodes = np.random.random(Num_of_Nodes)
for N in Nodes:
    for i in range(len(Region_Ranges)):
        if N < Region_Ranges[i]:
            Node_Region.append(i)
            break


file = open("graph2_50000.txt", "w")
General_Info = {}
General_Info['Num_of_Nodes'] = Num_of_Nodes
General_Info['Num_of_Regions'] = len(Region_List)
General_Info['Prev_Block'] = secrets.randbits(256)
file.write(json.dumps(General_Info)+'\n')

for i in range(Num_of_Nodes):
    # Node_Download_Bandwidth.append(floor(np.random.normal(DOWNLOAD_BANDWIDTH[Node_Region[i]],
    #                                            REGION_VARIANCE[Node_Region[i]] * 100000)))
    # Node_Upload_bandwidth.append(floor(np.random.normal(UPLOAD_BANDWIDTH[Node_Region[i]],
    #                                            REGION_VARIANCE[Node_Region[i]] * 10000)))
    Node_Download_Bandwidth.append(DOWNLOAD_BANDWIDTH[Node_Region[i]])
    Node_Upload_bandwidth.append(UPLOAD_BANDWIDTH[Node_Region[i]])
    Info = {}
    Info['Region_id'] = Node_Region[i] + 1
    Info['Region_name'] = Region_List[Node_Region[i]]
    Info['Download'] = Node_Download_Bandwidth[i]
    Info['Upload'] = Node_Upload_bandwidth[i]
    Info['Credit'] = floor(np.random.random()*100)
    Info_String = json.dumps(Info)
    file.write(Info_String+'\n')

# for i in range(Num_of_Nodes):
#     for j in range(Num_of_Nodes):
#         if i == j:
#             file.write('0 ')
#             continue
#         # min_Bandwidth = min(Node_Download_Bandwidth[i], Node_Upload_bandwidth[j])
#         # L = floor(LATENCY[Node_Region[i]][Node_Region[j]] + Block_size / min_Bandwidth)
#         # L = floor(np.random.normal(LATENCY[Node_Region[i]][Node_Region[j]], 50))
#         L = LATENCY[Node_Region[i]][Node_Region[j]]
#         file.write(str(L) + ' ')
#     file.write('\n')

