
Num_of_Nodes = 50000

Block_size = 100000000

Region_List = ["Amsterdam", "Brussels", "Chicago", "London", "Madrid", "Melbourne", "Moscow", "NewYork", "Paris",
               "Seoul", "Shanghai", "Sydney", "Tokyo", "Toronto", "Washington", "NEW_Dehli"]

LATENCY = [[3, 5, 98, 7, 26, 268, 49, 76, 10, 272, 262, 283, 240, 95, 84, 157],
           [5, 6, 98, 10, 22, 281, 44, 85, 10, 277, 386, 268, 232, 97, 85, 139],
           [98, 98, 9, 86, 97, 251, 137, 23, 94, 179, 272, 250, 169, 16, 28, 229],
           [10, 10, 86, 16, 24, 259, 46, 71, 9, 270, 246, 272, 217, 90, 78, 140],
           [26, 22, 96, 24, 8, 289, 67, 95, 18, 269, 380, 281, 230, 116, 93, 155],
           [268, 280, 252, 259, 289, 10, 314, 212, 273, 287, 324, 117, 144, 212, 206, 299],
           [52, 44, 137, 45, 67, 313, 10, 118, 50, 276, 140, 278, 194, 132, 134, 196],
           [77, 85, 23, 72, 95, 212, 118, 10, 74, 187, 280, 239, 176, 15, 9, 220],
           [10, 10, 94, 9, 18, 273, 50, 74, 13, 274, 233, 263, 235, 94, 79, 209],
           [273, 277, 178, 270, 269, 287, 271, 187, 274, 3, 193, 299, 33, 186, 198, 390],
           [223, 398, 257, 207, 289, 370, 209, 284, 233, 200, 4, 214, 47, 223, 221, 238],
           [283, 268, 251, 271, 281, 11, 278, 201, 263, 299, 380, 11, 114, 200, 242, 299],
           [240, 232, 169, 217, 230, 144, 194, 176, 235, 33, 75, 114, 30, 178, 170, 258],
           [100, 98, 17, 89, 114, 212, 137, 227, 17, 94, 188, 226, 199, 178, 8, 258],
           [84, 85, 28, 77, 94, 206, 134, 9, 87, 196, 219, 243, 171, 21, 7, 212],
           [150, 139, 226, 141, 155, 300, 196, 24, 220, 210, 390, 238, 299, 259, 223, 217]]

DOWNLOAD_BANDWIDTH = [68000000, 68000000, 37000000, 60000000, 35000000, 41000000, 34000000, 14000000, 45000000,
                      55000000, 25000000, 7000000, 36000000, 82000000, 34000000, 32000000, 20 * 1000000]

UPLOAD_BANDWIDTH = [20000000, 20000000, 10000000, 12000000, 10000000, 12000000, 18000000, 7000000, 15000000, 21000000,
                    31000000, 4000000, 14000000, 25000000, 10000000, 12000000, 20 * 1000000]

REGION_DISTRIBUTION = [0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625,
                       0.0625, 0.0625, 0.0625, 0.0625, 0.0625, 0.0625]

REGION_VARIANCE = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]