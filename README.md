# RBHC
<p align="center">
<img src="https://github.com/intuit/RBHC/blob/master/Images/RBHC.png" width="400" height="400">
</p>

[![CircleCI](https://circleci.com/gh/intuit/RBHC/tree/master.svg?style=svg&circle-token=8dc91b504991b931f05d3b116040a4dfee4d0586)](https://circleci.com/gh/intuit/RBHC/tree/master)
[![codecov](https://codecov.tools.a.intuit.com/ghe/aatluri/RBHC/branch/master/graph/badge.svg)](https://codecov.tools.a.intuit.com/ghe/aatluri/RBHC)
[![PyPI version](https://badge.fury.io/py/RBHC.svg)](https://badge.fury.io/py/RBHC)
## Recursive Binary Hierarchical Clustering
This code is for accomplishing recursive binary hierarchical clustering of data <br>
K-Means algorithm is applied on the initial dataset and a binary partition is created after which using chi square score statistic, the feature (event) that was responsible for the partition is found out. The remaining clusters are further divided recursively using the above approach until the cluster size reaches 1 or the silhouette score reaches the threshold value <br>
- [Installation](#installation)
- [Usage](#usage)
- [Statistics](#statistics)
- [Visualisation](#visualisation)
- [Data File Structure](#data-file-structure)
- [Contribution and license](#contribution-and-license)
### Installation
Prerequisites: python3 <br>
```
pip install RBHC
```

### Usage
```
from RBHC import clustering
clustering(dataFilePath,thresholdValue)
```

  - dataFilePath = Path to data file  [Check data file structure](#data-file-structure)
  - thresholdValue = Silhouette value threshold (optional parameter and default in program is 0.65)

Return value from this function is a json with a tree structure that is generated with following important fields
  - name = Name of cluster node (string)
  - parent = Name of it's parent node (string)
  - size = Size of cluster (integer)
  - children = Tree structure of subtree (List)
  - clusterCreated = If clustering has been successful (Boolean)

To see a sample of this return value run clustering over sample dataset provided and print output or check visualisation/sampleData.json <br>

If you want to run this program in an interactive manner in a jupyter notebook run this command in root directory *jupyter notebook* and then it opens up in localhost

### Statistics
Once program runs then clustering statistics are stored in statistics/hierarchical/nameOfDataFile/ and for each sub cluster created stats are stored in a .json file and attributes are following

- ClusterId = Identifier of a sub cluster L=Level G=Number of cluster in that level counted left to right
- Size = Size of cluster
- Primary feature cluster created by = Name of feature which is responsible primarily for this cluster formation
- Features chi score = Shows chi score of all features in that cluster
- Stats on cluster by each feature = Stats of each feature in this cluster
- Ids = All instances that are part of cluster and names are derived from column[0] of data file

### Visualisation
Copy visualisation folder to directory where clustering is being used<br>
In visualisation folder nameOfDataFile.json will be created for clustering visualisation <br>
Run this in visualisation folder *python -m http.server 8888* and then in web browser open http://localhost:8888/
![](Clustering.gif)

### Data File Structure

```
IDS         | feature1    |                     | featureN
------------|-------------|---------------------|-----------------
ID1         |  value1     |                     |  valueN
            |             |                     |  
            |             |                     |
            |             |                     |  
```

All data files should be stored in data folder and check data folder for a sample .csv data file

### Contribution and license
- [Contributing guidelines](.github/CONTRIBUTING.md)
- [License](LICENSE)
