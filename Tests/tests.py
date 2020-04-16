import unittest
import os
import sys
sys.path.append("../RBHC/")
from Clustering import *
clusterList={}
parentCluster=[[1,2,3,4,5,6,7,8,9],[9,9,9,9,9,9,9,9,9],[9,9,9,9,9,9,9,9,9],[9,9,9,9,9,9,9,9,9],[9,9,9,9,9,9,9,9,9]]
level=1
positions=[0,1,2,3,4]
parent='L0G0'
silhouetteThreshold=0.65
statsPath='Statisticstests/Hierarchical/unittest/'
user=['test','checking2','checking3','checking4','checking5']
attributes=['A','B','C','D','E','F','G','H','I']
globalCount={}
visualisationDirectory="Visualisationtests/"
modelNameFilePath="Visualisationtests/models.txt"
sampleJson={'name': 'L0G0', 'parent': 'null', 'desc': 'Cluster Size :6394', 'size': 6394, 'line_color': '#000', 'alert_color': '#000', 'children': [{'name': 'L1G0', 'desc': 'L1G0,Cluster Size :6335,Split by :Feature15,Mean : 2.3503', 'parent': 'L0G0', 'size': 6335, 'line_color': '#000', 'alert_color': '#000', 'children': [{'name': 'L2G0', 'desc': 'L2G0,Cluster Size :6163,Split by :Feature12,Mean : 2.0805', 'parent': 'L1G0', 'size': 6163, 'line_color': '#000', 'alert_color': '#000', 'children': [{'name': 'L3G0', 'desc': 'L3G0,Cluster Size :6156,Split by :Feature1,Mean : 0.4977', 'parent': 'L2G0', 'size': 6156, 'line_color': '#000', 'alert_color': '#000', 'children': [{'name': 'L4G0', 'desc': 'L4G0,Cluster Size :5977,Split by :Feature12,Mean : 0.9587', 'parent': 'L3G0', 'size': 5977, 'line_color': '#000', 'alert_color': '#000', 'children': [{'name': 'L5G0', 'desc': 'L5G0,Cluster Size :19,Split by :Feature1,Mean : 61.1053', 'parent': 'L4G0', 'size': 19, 'line_color': 'red', 'alert_color': 'red', 'children': [{'name': 'L6G0', 'desc': 'L6G0,Cluster Size :11,Split by :Feature1,Mean : 42.2727', 'parent': 'L5G0', 'size': 11, 'line_color': '#000', 'alert_color': '#000', 'children': []}, {'name': 'L6G1', 'desc': 'L6G1,Cluster Size :8,Split by :Feature1,Mean : 87.0', 'parent': 'L5G0', 'size': 8, 'line_color': '#000', 'alert_color': '#000', 'children': []}]}, {'name': 'L5G1', 'desc': 'L5G1,Cluster Size :5958,Split by :Feature1,Mean : 0.2969', 'parent': 'L4G0', 'size': 5958, 'line_color': '#000', 'alert_color': '#000', 'children': [{'name': 'L6G2', 'desc': 'L6G2,Cluster Size :5648,Split by :Feature12,Mean : 0.4232', 'parent': 'L5G1', 'size': 5648, 'line_color': '#000', 'alert_color': '#000', 'children': [{'name': 'L7G0', 'desc': 'L7G0,Cluster Size :204,Split by :Feature1,Mean : 2.3676', 'parent': 'L6G2', 'size': 204, 'line_color': 'red', 'alert_color': 'red', 'children': []}, {'name': 'L7G1', 'desc': 'L7G1,Cluster Size :5444,Split by :Feature1,Mean : 0.1964', 'parent': 'L6G2', 'size': 5444, 'line_color': '#000', 'alert_color': '#000', 'children': []}]}, {'name': 'L6G3', 'desc': 'L6G3,Cluster Size :310,Split by :Feature12,Mean : 10.7645', 'parent': 'L5G1', 'size': 310, 'line_color': 'red', 'alert_color': 'red', 'children': []}]}]}, {'name': 'L4G1', 'desc': 'L4G1,Cluster Size :179,Split by :Feature12,Mean : 39.6201', 'parent': 'L3G0', 'size': 179, 'line_color': 'red', 'alert_color': 'red', 'children': []}]}, {'name': 'L3G1', 'desc': 'L3G1,Cluster Size :7,Split by :Feature1,Mean : 221.8571', 'parent': 'L2G0', 'size': 7, 'line_color': 'red', 'alert_color': 'red', 'children': []}]}, {'name': 'L2G1', 'desc': 'L2G1,Cluster Size :172,Split by :Feature12,Mean : 124.6919', 'parent': 'L1G0', 'size': 172, 'line_color': 'red', 'alert_color': 'red', 'children': []}]}, {'name': 'L1G1', 'desc': 'L1G1,Cluster Size :59,Split by :Feature15,Mean : 420.2034', 'parent': 'L0G0', 'size': 59, 'line_color': 'red', 'alert_color': 'red', 'children': []}], 'clusterCreated': True}

class TestClustering(unittest.TestCase):
    def test_initializeClusterList(self):
        if(not os.path.exists(statsPath)):
            os.makedirs(statsPath)
        if(not os.path.exists(visualisationDirectory)):
            os.makedirs(visualisationDirectory)
        self.assertEqual(initializeClusterList(parentCluster,clusterList),True)
        self.assertEqual(hierarchicalClustering(parentCluster,level,positions,parent,clusterList["children"],silhouetteThreshold,statsPath,user,attributes,globalCount),True)
        self.assertEqual(writeCluster(visualisationDirectory+'unittest',clusterList,globalCount),True)
        self.assertEqual(createModelList(modelNameFilePath,'unittest'),True)
        self.assertEqual(clustering('../Data/sampleData.csv',0.65),sampleJson)
if __name__=='__main__':
    unittest.main()
