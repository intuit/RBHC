import pandas
import sklearn
import numpy
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.feature_selection import chi2
import json
import ast
import os
import glob
import operator
import argparse
import sys


def createModelList(modelNameFilePath, dataFile):
    ''' Appends model name to existing list of model name
    dataFile = name of data input file
    modelNameFilePath = path where models.txt is stored
    '''
    try:
        treeList = []
        write = True
        if (os.path.exists(modelNameFilePath)):
            fh = open(modelNameFilePath, "r")
            treeList = ast.literal_eval(fh.read())
            fh.close()
            if (str(dataFile)) not in treeList:
                treeList.append(dataFile)
            else:
                write = False
        else:
            treeList.append(dataFile)
        if (write):
            fh = open(modelNameFilePath, "w")
            fh.write(json.dumps(treeList, ensure_ascii='False'))
            fh.close()
    except Exception as e:
        print(e)
        return False
    return True


def writeCluster(fileName, clusterList, globalCount):
    ''' Writes cluster structure to json file
    fileName = name of data input file
    clusterList = hierarchical cluster created
    globalCount = dictionary with key as level and value as number of nodes at that level
    '''
    try:
        maximumKey = 0
        maximumValue = 0
        for key, value in globalCount.items():
            if (key > maximumKey):
                maximumKey = key
            if (value > maximumValue):
                maximumValue = value
        clusterList["height"] = maximumKey
        clusterList["width"] = maximumValue
        clusterListJson = json.dumps(clusterList, ensure_ascii='False', indent=4)
        fh = open(fileName + ".json", "w")
        fh.write("[" + clusterListJson + "]")
        fh.close()
    except Exception as e:
        print(e)
        return False
    return True


#recursive hierarchical clustering function
def hierarchicalClustering(parentCluster, level, positions, parent, clusterList,
                           silhouetteThreshold, statsPath, user, attributes, globalCount):
    ''' Recursive Binary Hierarchical Clustering Function
    parentCluster = cluster to be subclustered
    level = next level to be clustered
    positions = list of entities in parentCluster by index
    parent = name of parent cluster
    clusterList = hierarchical cluster structure to which subsequent clusters are appended to
    silhouetteThreshold = silhouette score threshold range in [-1 to 1]
    statsPath = path to statistics directory
    user = list of all user ids
    attributes = feature names
    globalCount = dictionary with key as level and value as number of nodes at that level
    '''
    print("At node " + parent)
    silhouetteScore = -1
    #tree node count dictionary at each level for labelling
    if (len(parentCluster) < 2):
        return False

    clusterCount = 2
    #clustering
    clusterer = KMeans(n_clusters=clusterCount, random_state=0)
    kmeans = clusterer.fit(parentCluster)
    clusterLabels = clusterer.fit_predict(parentCluster)
    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
    if (1 < len(set(clusterLabels)) < len(parentCluster)):
        silhouetteScore = silhouette_score(parentCluster, clusterLabels)

    #silhouette score threshold check
    if (silhouetteScore < silhouetteThreshold):
        return False

    indeX = chi2(parentCluster, clusterLabels)[0].tolist()
    #finding max chi score and its feature index
    chi_max = 0
    iterator = 0
    index_ = -1
    featureSignificance = {}
    while (iterator < len(indeX)):
        featureSignificance[attributes[iterator]] = indeX[iterator]
        if (indeX[iterator] > chi_max):
            chi_max = indeX[iterator]
            index_ = iterator
        iterator = iterator + 1
    featureSignificanceSorted = sorted(featureSignificance.items(),
                                       key=lambda x: x[1],
                                       reverse=True)
    try:
        globalCount[level]
    except:
        globalCount[level] = 0

    final_ = []
    childCluster = []
    {
        iterator: final_.append(numpy.where(kmeans.labels_ == iterator)[0])
        for iterator in range(kmeans.n_clusters)
    }
    clusterIterator = 0

    #for each cluster formed
    while clusterIterator < kmeans.n_clusters:
        iterator = 0
        childCluster = []
        new_positions = []
        ids = []
        while iterator < len(final_[clusterIterator]):
            childCluster.append(parentCluster[final_[clusterIterator][iterator]])
            new_positions.append(positions[final_[clusterIterator][iterator]])
            ids.append(user[positions[final_[clusterIterator][iterator]]])
            iterator = iterator + 1

        #cluster data interpretation
        clusterSummary = {}
        clusterName = 'L' + str(level) + 'G' + str(globalCount[level])
        dataIds = pandas.DataFrame(ids, columns=["IDS"])
        dataStats = pandas.DataFrame(childCluster, columns=attributes)
        stats = dataStats[attributes].head(n=len(childCluster)).describe()
        clusterSummary['ClusterId'] = clusterName
        clusterSummary['Size'] = len(childCluster)
        clusterSummary['Primary feature cluster created by'] = attributes[index_]
        clusterSummary['Features chi score'] = featureSignificanceSorted
        clusterSummary['Stats on cluster by each feature'] = stats.to_dict()
        clusterSummary['Ids'] = ids
        clusterSummaryJson = json.dumps(clusterSummary, ensure_ascii='False', indent=4)
        fh = open(statsPath + clusterName + 'clusterDescription' + ".json", "w")
        fh.write("[" + clusterSummaryJson + "]")
        fh.close()
        clusterIterator = clusterIterator + 1
        processingList = {}
        processingList["name"] = clusterName
        processingList["desc"] = clusterName + ",Cluster Size :" + str(
            len(childCluster)) + ',Split by :' + str(attributes[index_]) + ",Mean : " + str(
                round(dataStats[attributes[index_]].mean(), 4))
        processingList["parent"] = parent
        processingList['size'] = len(childCluster)

        if (float(len(childCluster) / len(parentCluster)) < 0.1):
            processingList['line_color'] = 'red'
            processingList['alert_color'] = 'red'

        else:
            processingList['line_color'] = '#000'
            processingList['alert_color'] = '#000'

        processingList["children"] = []
        globalCount[level] = globalCount[level] + 1
        hierarchicalClustering(childCluster, level + 1, new_positions, clusterName,
                               processingList["children"], silhouetteThreshold, statsPath, user,
                               attributes, globalCount)
        clusterList.append(processingList)
    return True


def initializeClusterList(transformedValues, clusterList):
    '''Initialises clusterList
    transformedValues = Input feature vector
    clusterList = hierarchical cluster structure to which subsequent clusters are appended to
    '''
    try:
        clusterList["name"] = 'L0G0'
        clusterList["parent"] = "null"
        clusterList["desc"] = "Cluster Size :" + str(len(transformedValues))
        clusterList["size"] = len(transformedValues)
        clusterList["line_color"] = '#000'
        clusterList["alert_color"] = '#000'
        clusterList["children"] = []
        clusterList["clusterCreated"] = False
    except Exception as e:
        print(e)
        return False
    return True


def clustering(dataFilePath, silhouetteThreshold=0.65):
    ''' Clusering function
    dataFilePath = Path of input csv file
    silhouetteThreshold = silhouette score threshold
    '''
    user = []
    transformedValues = []
    attributes = []
    clusterList = {}
    positions = []
    globalCount = {}
    if (not os.path.exists(dataFilePath)):
        print(dataFilePath + " Not found")
        sys.exit(-1)
    dataFile = os.path.splitext(os.path.basename(dataFilePath))[0]
    statsPath = "Statistics/Hierarchical/" + str(dataFile) + "/"
    visualisationDirectory = "Visualisation/"
    modelNameFilePath = visualisationDirectory + 'models.txt'
    vector = pandas.read_csv(dataFilePath)
    print(vector.head(n=len(vector)).describe())
    attributes = list(vector.columns[1:])
    transformedValues = vector.iloc[:, 1:].values.tolist()
    user = vector.iloc[:, 0].values.tolist()
    positions = list(range(0, len(transformedValues)))
    # Stats Path to be created
    if not os.path.exists(statsPath):
        os.makedirs(statsPath)
    else:
        files = glob.glob(statsPath + '/*')
        for f in files:
            os.remove(f)

    if (initializeClusterList(transformedValues, clusterList)):
        if (hierarchicalClustering(transformedValues, 1, positions, 'L0G0', clusterList["children"],
                                   silhouetteThreshold, statsPath, user, attributes, globalCount)):
            clusterList['clusterCreated'] = True
            if (os.path.isdir(visualisationDirectory)):
                if (writeCluster(visualisationDirectory + dataFile, clusterList, globalCount)):
                    createModelList(modelNameFilePath, dataFile)

    return (clusterList)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--datafilepath', help='Enter name of data file in data folder')
    parser.add_argument('--silhouettethreshold', help='Enter silhouetteThreshold')
    args = parser.parse_args()
    if (not args.datafilepath):
        print("Please Provide Data File")
        sys.exit(-1)
    dataFilePath = args.datafilepath
    if (not (args.silhouettethreshold)):
        silhouetteThreshold = 0.65
    else:
        silhouetteThreshold = args.silhouettethreshold
    clustering(dataFilePath, silhouetteThreshold)


if __name__ == "__main__":
    main()
