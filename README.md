
# README

[![DOI](https://zenodo.org/badge/240088009.svg)](https://zenodo.org/badge/latestdoi/240088009)

This directory contains tooling to map NeuroRacer data. It is a prequisite that you have access to a directory containing such data. 

NeuroRacer's data packages usually contain a `.yaml` with metadata and a subfolder system like `zed/left/image_raw_color/compressed`, containing the cameras pictures. 

The 2 functions if this tooling contains is mapping and augmenting the mapped data.

These functions have been split and can be executed separately to optimise runtimes.

The datamapper is designed to be deployed on a remote system and for a path containing one or more packages of NeuroRacer data. It will then look for the `.yaml` and the image data in all folders down the path.

The augmenter is then used to augment the mapped images, also remotely.


###  Map the data

1. Check if the config.py file contains the correct target path for the NeuroRace Data as `SOURCE_DIR`.

2. If 1. is true, use`python3 datamapper.py` to map the data. It will produce a `mapped.csv` at the location you started datamapper from.

   

### Augment the data

1. Have you mapped the data?
2. If 1. is true, move the the `mapped.csv` file to the directory containing `augmenter.py` . 
3. Check if `config.py` contains the path you want your augemented data to end at as `TARGET_DIR`.
4. In `config.py` , adjust how to many pictures you want to fill the bins up to with `FILL_UP_TO`



###  Visualise how much data was augmented

After augmenting the data, there will be a `numbers.csv` in the folder you started `augmenter.py` from. It can be visualised using `visualise.py`



### Known issues

`visualise.py` might looking for collumns that are falsely labeled or missing. Adjustments can be made fairly easily by changing column names in either`numbers.csv`  or `visulise.py` .

Apart from that, the code has no known issues. Make sure not to end paths with `/` since `os.path.join` does not like that. 
