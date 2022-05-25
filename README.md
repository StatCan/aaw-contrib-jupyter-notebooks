## Purpose

This repository is used to hold example Jupyter notebooks and tutorials to help users get started with Data Science and Machine Learning. Example notebooks consists of creating Kubeflow Pipelines, developing Plotly Dash apps, tensorflow, scikitlearn, pytorch and many more! We recommend having first a look at the Quickstart.ipynb.

## How do the artifacts from this repo get mounted to user notebook pods?
Example notebooks are mounted on all user notebooks in the `/aaw-contrib-jupyter-notebooks` folder. This is done via the start-custom.sh script in [`aaw-kubeflow-containers`](https://github.com/StatCan/aaw-kubeflow-containers/blob/master/resources/common/start-custom.sh#L7).

## Example Notebooks:
- Authors: Christian Ritter, Blair Drummond, Andrew Scribner

### Kubeflow-Pipeline Basics:
Kubeflow Pipelines allows users to build and deploy scalable machine learning workflows on Docker containers.
Contains two basic example notebooks: building a simple pipeline using dockerized components and using lightweight Kubeflow pipeline components.
More information about [`KFP`](https://v1-3-branch.kubeflow.org/docs/components/pipelines/overview/pipelines-overview/) and [`KFP SDK API`](https://kubeflow-pipelines.readthedocs.io/en/latest/source/kfp.html) 

### Kubeflow-metadata (Move to archive folder, broken)

### MapReduce-Pipeline
This is another Kubeflow Pipeline example which uses the map-reduce pattern; executing a first step (map) and then aggregating all results from the map in another step (reduce). These examples also include pipelines that write data to MinIO. 

### Plotting
There are 3 examples of plotting libraries used: Jupyter Dash, Matplotlib and Plotly. <br />
Using the Jupyter Dash library, it is easy to develop Plotly Dash apps interactively within Jupyter environments.  <br />
Link to Jupyter Dash Repo: https://github.com/plotly/jupyter-dash <br />

Matplotlib leaverages the Jupyter interactive widgets framework, `ipympl` enables the interactive features of Matplotlib in the Jupyter notebook and in Jupyterlab. Overview from Matplotlib [`readme`](https://github.com/matplotlib/ipympl#ipympl) <br />
Visit https://matplotlib.org/ for more examples, references and tutorials. 

Plotly is a declarative charting library with over 30 chart types, including scientific charts, 3D graphs, statistical charts, SVG maps, financial charts, and more. Overview from Plotly [`readme`](https://github.com/plotly/plotly.py/blob/master/README.md#overview). <br />
The Jupyter notebook tutorial contains examples creating a 3D scatter plot, 3D scatter plot with a regression surface, line plot with adjacent histogram and a bubble map.

### Python
The CANSIM Jupyter notebook explores the CANSIM API created by Statistics Canada. Exploring functions like `getCodeSets`, `getAllCubeList` and `getCubeMetaData` from Statistics Canada's Web Data Service (WDS), downloading it as CSV data files. <br />
For more information about the WDS, visit: https://www.statcan.gc.ca/eng/developers/wds/user-guide

### Pytorch
This Jupyter notebook demonstrates a Pytorch tutorial on how to use the torchtext library to build a dataset for text classification analysis. </br>
For more information and tutorials visit [`Pytorch Homepage`](https://pytorch.org/tutorials/beginner/text_sentiment_ngrams_tutorial.html) </br>
TorchText library Docs: https://pytorch.org/text/stable/index.html

### QuerySQL
This notebooks runs SQL queries on the S3 storage system, Minio. Minio's API is compatible with S3 storage [`SELECT API`](https://docs.min.io/docs/minio-select-api-quickstart-guide.html). It is not effective for creating joins or other relational database tricks, but it's phenomenal at extracting exactly the data that you need, so that your queries are blazingly fast. Examples include querying data with SQL in .csv.gz, .parquet and .csv format.

### R
Contains a demo of creating scatter plots in R using the `ggplot2` library. Documentation on [`ggplot2`](http://r-statistics.co/Top50-Ggplot2-Visualizations-MasterList-R-Code.html#Scatterplot) <br />
Also contains a Jupyter notebook demo using an interactive worldmap visualization with R, demonstrating how well R and Jupyter work together. 

### ScikitLearn
Using the Iris Dataset with Scikit-Learn and running decision tree classifiers on feature subsets. <br />
Link to Sckitlearn docs https://scikit-learn.org/stable/  

### Self-serve-storage
Consists of demos on how to connect to the bucket storage system using the minio client, s3fs library in Python and R.

### StatsCan Data
A demo of using the Web Data Service developed by Statistics Canada, providing access to data and metadat Stats Can releases in R and Python. <br />
More information about Web Data Service [`(WDS)`](https://www.statcan.gc.ca/en/developers/wds)

### Tensorflow
A tutorial from the [`TF homepage`](https://www.tensorflow.org/tutorials/keras/classification) using image classification via Keras.
