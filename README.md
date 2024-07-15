# t-SNE for cytometry data
> t-Distributed Stochasitc Neighbor Embedding for visualizing high-dimentional cytometry data

Simple project to analyse raw ".fcs" files, create t-SNE cluster plots and further analyse different subpopulations found in it.

## Getting started

`git clone https://github.com/Garzdak/tSNE-cyt.git`

Requirements:
* python >= 3.8
* pandas >= 0.22
* seaborn
* sklearn
* flowkit
* xlsxwriter

In the given repository you can find the following files:

1. Perform tSNE.py - perform t-SNE analysis from raw .fcs files
2. Analysis.py - analyse the t-SNE clustering results
3. test/cytometry data - contains 3 samples and file for compensation for "Perform tSNE.py"
4. test/for analysis/Xn.pkl - sample cluster for "Analysis.py"


## Features

* Select parameters for the t-SNE clustering
* Color the clusters by channels or subpopulations
* Compare different parts of t-SNE cluster
* Have a slice of the t-SNE map only for samples of interst
* Plot distributions for t-SNE subpopulations


# User Guide  

Please click [here](https://github.com/Garzdak/tSNE-cyt/tree/main/guide) to read user guide.

## For handling cytometry data the code relies on the following package

[White, S., Quinn, J., Enzor, J., Staats, J., Mosier, S. M., Almarode, J., Denny, T. N., Weinhold, K. J., Ferrari, G., & Chan, C. (2021). FlowKit: A Python toolkit for integrated manual and automated cytometry analysis workflows. Frontiers in Immunology, 12. https://doi.org/10.3389/fimmu.2021.768541](https://www.frontiersin.org/articles/10.3389/fimmu.2021.768541/full)


## Licensing

The code in this project is licensed under MIT license.


