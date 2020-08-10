from graph_config import *
import numpy as np
import json
from math import floor

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


file = open("graph1_100.txt", "w")
for i in range(Num_of_Nodes):
    Node_Download_Bandwidth.append(floor(np.random.normal(DOWNLOAD_BANDWIDTH[Node_Region[i]],
                                               REGION_VARIANCE[Node_Region[i]] * 100000)))
    Node_Upload_bandwidth.append(floor(np.random.normal(UPLOAD_BANDWIDTH[Node_Region[i]],
                                               REGION_VARIANCE[Node_Region[i]] * 100000)))
    Info = {}
    Info['Region_id'] = Node_Region[i] + 1
    Info['Region_name'] = Region_List[Node_Region[i]]
    Info['Dowload'] = Node_Download_Bandwidth[i]
    Info['Upload'] = Node_Upload_bandwidth[i]
    Info_String = json.dumps(Info)
    file.write(Info_String+'\n')


for i in range(Num_of_Nodes):
    for j in range(Num_of_Nodes):
        if i == j:
            file.write('0 ')
            continue
        min_Bandwidth = min(Node_Download_Bandwidth[i], Node_Upload_bandwidth[j])
        L = floor(LATENCY[Node_Region[i]][Node_Region[j]] + Block_size / min_Bandwidth)
        file.write(str(L) + ' ')
    file.write('\n')

