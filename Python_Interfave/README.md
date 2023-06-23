# HoloHeart TRANSFER - Command Line Tool
The CARTO script reads the mesh and LAT data of one or multiple patient data set and transfers the 3D geometry to a text file. The path to the CARTO data sets can be entered in runtime, so they don't need to be in the same directory as the script. It then stores the relevant information in .txt files for later use in Blender. The script will convertd every mesurement set. The desired results can be chosen later in Blender.



## Overview
*main.py*
- is the main script for the convertion of the CARTO 3D data

*check_folders.py*
- finds the given directory with the patient folders and repeats the request if necessary (faulty input)

*read_data.py*
- hovers through the subdirectories and finds the relevant files for each patient

*convert_data.py*
- opens the mesh/car files, reads their data, converts it for appropriate use in blender and saves them in the given directory



## Installation
To ensure that python is working open a terminal and check if pyhton is already installed:
```
py --version
```

If you need to install, download it from the [python webpage](https://www.python.org/downloads/) and follow the instructions on the page.



## Execution

#### In Windows
The input data will be entered during runtime. Needed for the data transfer:
- one or more Patient data folders, usually named like  "Patient 2014_03_10"
- path were to find these folders
- path to store the converted data (optional)

The output data will be stored in a converted_data folder in the directory were the Patient folders are by default. Another directory can be chosen during runtime.

To run the script in windows, click on the windows symbol and type
```
python
```
Then open e.g. *IDLE python (...)* and type
```
import os
```
Followed by
```
os.chdir(r'path to main.py')
```
where at 'path to main.py' you have to insert the path where to find the python script 'main.py' , e.g. 'D:\Eigene Dokumente\Klinik\Carto\Python'
Finally type
```
import main
```
and follow the instructions on the screen


#### In Ubuntu
Just run the `main` to execute the script and follow the instructions.
```python
python3 main.py
```
