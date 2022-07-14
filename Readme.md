# Study Cleaner
Use this script to clean DICOM studies using NIRC naming convention 
```
poetry publish --build --username $PYPI_USERNAME --password $PYPI_PASSWORD
```
## Setup
##### 1. Environment
go to python current working directory
```
conda env create --file enviroment.yml
```

[More info on conda](https://kiwidamien.github.io/save-the-environment-with-conda-and-how-to-let-others-run-your-programs.html)


##### 2. Setup Script Alias
Set up an alias on computer. In terminal type:
```
sudo nano ~/.zshrc
```

add a line with the path to the script
```
alias studyclean='<PATH_TO_SCRIPT>'
```

save changes

```
source ~/.zshrc
```

## Usage
##### Prep

Extract all DICOM files into a one source directory. Make sure that everything in this directory comes from the same study. Place them in the source directory with the following directories already created

```
Study
│
└───source
│
└───cleaned
│
└───archive
```

Cleaned will contain all the dicom files for each individual study
archive will contain the .zip files for each study


##### 1. Clean
Clean should be the first command you use. All files from the source folder will be scanned and cleaned to match the same convention. Pad for both subject and site will determine the exact number of slots for both respective identifiers.
```
studyclean clean -i <path_to_source> -o <path_to_cleaned> --subject_pad=2 --site_pad=3
```
Output of each study will look like:
**Study-010-02-Timepoint**

##### 2. Extract
Extract will go through each study folder and output a small JSON file containing the subject id and modalities... amongst other things. This should be done **after** clean has taken plaec

```
studyclean extract -i <path_to_cleaned>
```



##### 3. archive
Will create a zip folder for every directory and the contents of each subdirectory. 
```
studyclean archive -i <path_to_cleaned> -o <path_to_archive>
```



