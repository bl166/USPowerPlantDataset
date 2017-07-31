# The Creation of US Power Plants NAIP/LANDSAT8 Dataset
This repo is a demonstration of dataset creation. The US Power Plants NAIP/LANDSAT8 Dataset is focused on US mainland power plants, providing both high-resolution (1m) and medium-resolution (15m) imagery for detection/segmentation tasks.
Data sources:
* [NAIP](https://www.fsa.usda.gov/programs-and-services/aerial-photography/imagery-programs/naip-imagery/) for high-resolution imagery
* [Landsat8](https://landsat.usgs.gov/landsat-8) for medium-resolution imagery
* [EPA EGRID documents](https://www.epa.gov/energy/emissions-generation-resource-integrated-database-egrid) for latitude and longtitude locations

## 1 &nbsp; Data Explaination

Items in _Italics_ are related with construction, not to worry for classification concerns; in __bold__ are respectively images, labels, register, and sample code for image segmentation/pixelwise classification; and there are some ```useful scripts``` for making and testing this dataset. Starred* Items are outputs to expect as the results of dataset construction.

1. _/uspp_naip_: high-resolution power plant images (~1115x1115 pix, 5M/ea), used for gathering annotations;

2. __/uspp_landsat__: medium-resolution power plant images (~75x75 pix, 70K/ea), to be used for classification

3. __/annotations__*: confidence and binary masks denoting the outline of power plants. Meaning of pixel values in sub-folders: <br/>
a) /confidence: number of annotators bounding it within a power plant<br/>
b) /binary: whether or not more than half of all annotators agree that it is part of a power plant

4. _/exceptions_*: instances with no valid annotations (most likely no visible power plants; or in a very small chance, all of three annotations were rejected);

5. __uspp_metadata.geogson__*: geographic location, unique egrid id, plant name, state and county name, primary fuel, fossil fuel category, capacity factor, nameplate capacity, and CO<sub>2</sub> emission data;<br/>
Visualization available here: https://github.com/bl166/USPowerPlantDataset/blob/master/uspp_metadata.geojson;

6. _accepted\_ann\_json.txt_: accepted annotations collected from Amazon Mechanical Turk;<br/>
Annotation tool available here: https://github.com/tn74/MTurkAnnotationTool;

7. _egrid2014_data_v2_PLNT14.xlsx_: A subset of the Egrid document which contains US power plant locations and other information;

8. ```cropPowerPlants.py```: exports satellite imagery from Google Earth Engine;

9. ```fixLs.m```: pre-processes landsat imagery, including intensity strech and gamma correction;

10. ```make.py```: constructs the dataset;

11. __```classify_sample.py```__: tests a simple segmentation task (pixel-wise classification) on this dataset.

## 2 &nbsp; Dataset Construction
### 2.0 Overview
This dataset was constructed in three phases:
1. Download satellite imagery;
2. Gather annotations of power plants;
3. Merge accepted annotations and create binary labels.

### 2.1 Satellite Imagery Download
#### Dependencies
+ ```Python 2.X``` (for exporting data)
+ Python API for Google Earth Engine
+ Packages: ```ee, numpy, xlrd```

#### Code & documentation
https://github.com/bl166/USPowerPlantDataset/blob/master/cropPowerPlants.py

#### Steps
1. [Sign up](https://earthengine.google.com/signup/) for Google Earth Engine. To export data you must sign up as a developer.
2. Install the [Python API](https://developers.google.com/earth-engine/python_install).
Follow instructions in the link.
3. In  [cropPowerPlants.py](https://github.com/bl166/USPowerPlantDataset/blob/master/cropPowerPlants.py), on _line\#100 and 101_ define your indices, from which collection to export, and in what order you want the exporting to take place.
```Python
if __name__ == '__main__':
	id_start,id_end = (300,500) # include id_start, exclude id_end
	download_ppt_pic(id_start,id_end,order='descend',collection='naip')
```
4. Run the script, and in Google Earth Engine [code editor](https://code.earthengine.google.com/), right columns -> task -> you can monitor the tasks here.
```bash
# activate whatever environment you may have installed for running the earthengine
source activate YOUR_ENVS
python cropPowerPlants.py
```
After the exporting finishes, these cropped images should be in your Google Drive (Keep an eye on your storage. Download and clear it up regularly. Tasks will fail if there's no enough space in your drive).
5. Download images into __```/uspp_naip```__ and __```/uspp_landsat```__ EXACTLY.

#### Summary
* Input (in the dataset root dir - same directory as the script): __egrid2014_data_v2_PLNT14.xlsx__
* Output (to the dataset root dir): __/uspp\_naip__ and/or __/uspp\_landsat__


### 2.2 Gather Annotstions
See MTurkAnnotationTool: https://github.com/tn74/MTurkAnnotationTool.

### 2.3 Binary Labels Creation
#### Dependencies
+ ```Python 3.X```
+ Packages: ```os, sys, json, numpy, PIL, xlrd```

#### Code & documentation
https://github.com/bl166/USPowerPlantDataset/blob/master/make.py

#### Steps
1. Items that you should already have before running the script:<br/>
  * __```/uspp_naip```__: NAIP data with unprocessed images' names being ```ID.tif```;<br/>
  * __```egrid_2014_subset.xslx```__: the original metadata from which we read locations and cropped those power plants out; <br/>
  * __```accepted_ann_json.txt```__: annotations from the MTurkers.<br/>
    * Note#1: _Items mentioned above should be directly under the root directory and named exactly as quoted. Otherwise the construction will fail._<br/>
  * (Optional, but strongly recommended!) __```/uspp_landsat```__: Landsat8 data with unprocessed images' names being ```ID.tif```.<br/>
    * Note#2: _If you do not have this folder, annotations will still be generated._<br/>
2. Another thing that might be useful to do in advance of making the dataset: preprocessing the Landsat8 data.
```bash
matlab -nodisplay -r fixLs
```
3. Run this script. While the program is running, you can expect some message showing the current status.
```bash
python make.py
```
4. Outputs: After the program finishes, you should find the following items shown up/changed in the root directory:<br/>
  * a new folder called __```/annotations```__, in which <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;i) __```/confidence```__ has all annotated polygons converted into binary polygons masks and added up; <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ii) __```/binary```__ has confidence masks binarized by max voting. <br/>
    * Note#3: _The binary values are 0 and 255, therefore you should normalize it to 0 and 1 at the actual practice._<br/>
  * Images in ```uspp_naip``` (and ```uspp_landsat``` if applicable) that can be corresponded to the "accepted_ann_json.txt"
are __renamed__ (if annotations are found valid) or __moved__ to ```/exceptions``` (if annotations contain only empty content).
    * Note#4 (new name convention): *DataType\_egridUniqueID\_State\_Type.tif*<br/>
  * Finally, a new file named ```uspp_metadata.geojson``` is generated. It contains all annotated power plants' metadata.

5. In case that the process is interrupted, you can re-run it at the spot. All images that are already processed will be intouched, and new power plants will be added to the end of the metadata.

#### Summary
* Input: __/uspp\_naip__, __accepted\_ann\_json.txt__, __/uspp\_landsat__ (optional), __/uspp\_metadata.geojson__ (optional)
* Output: __/annotations__, __/exceptions__, __uspp\_metadata.geogson__

## 3 &nbsp; Test the Dataset
#### Dependencies
+ ```Python 3.X```
+ Packages: ```sklearn, matplotlib, scipy, PIL, json, re, os, sys```

This code is designed for pixel-based image segmentation. It looks at the window centered at each pixel and decides whether or not this pixel belongs to the object of interest.

#### Code & documentation
https://github.com/bl166/USPowerPlantDataset/blob/master/classify_sample.py
```{r,engine='bash',code_cls}
python classify_sample.py
```

### 3.1 Cross-validation Results
<img src="https://image.ibb.co/ksRRPk/Figure_1.png" width="500">

### 3.2 Test on Specific Cases
<img src="https://image.ibb.co/ho2cVQ/Figure_1_1.png" width="700">

## Developers
* Ben Brigman
* Gouttham Chandrasekar
* Shamikh Hossain
* Boning Li
* Trishul Nagenalli

Project: [_Detecting Electricity Access from Aerial Imagery_](http://bigdata.duke.edu/projects/electricity-access-developing-countries-aerial-imagery), Duke Data+ 2017
