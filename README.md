# q2-humann2

QIIME2 plugin for running HUMAnN2. 

## Installation

You can install the Q2-HUMAnN2 plugin through miniconda:

```bash
conda create -n q2-humann2 python=3.5
source activate q2-humann2
pip install https://github.com/qiime2/qiime2/archive/master.zip https://github.com/qiime2/q2cli/archive/master.zip https://github.com/qiime2/q2-types/archive/master.zip https://github.com/qiime2/q2-feature-table/archive/master.zip https://github.com/wasade/q2-humann2/archive/master.zip
```

## Example

The Q2-HUMAnN2 plugin consumes a demultiplexed artifact from QIIME and produces gene family, pathway coverage and pathway abundance BIOM tables. 

```bash
qiime2 humann2 run --i-demultiplexed-seqs seqs.qza --output-dir results --p-threads=1
```

The produced artifacts can then be fed into downstream QIIME diversity analyses:

```bash
# commands adapted from q2-dada2 plugin readme and assumes the file 
# sample-metadata.tsv is in your current working directory and is relevant for
# your data
qiime diversity beta --i-table results/pathcoverage.qza --p-metric braycurtis --o-distance-matrix bray-curtis-dm
qiime diversity pcoa --i-distance-matrix bray-curtis-dm.qza --o-pcoa bray-curtis-pc
qiime emperor plot --i-pcoa bray-curtis-pc.qza --m-sample-metadata-file sample-metadata.tsv --o-visualization bray-curtis-emperor
qiime tools view bray-curtis-emperor.qzv
```
