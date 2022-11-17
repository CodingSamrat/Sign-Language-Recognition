import os
import cv2
import pandas as pd
import numpy as np
from tqdm import tqdm



def CreateColumns(_imgSize):
    """
    Creating Columns of Dataframe.
    This Function returns a list of Columns
    which are the title of Features
    """
    columns = []
    featuresClmLength = _imgSize * _imgSize
        
    for i in range(featuresClmLength):
        columns.append(f"px-{i}")
        
    print(f"\n'{featuresClmLength}' Columns are Created Succeaafully!\n")
    return columns



def Image2CSV(_path, _columns, _imgSize):
    """
    It takes four parameters Path, List of Columns, img Size and empty DataFrame for fetures.
    And create two CSV Files, features.csv & labels.csv.
    Path should be root of all Classes of images. Like,
    Data/[A[*.jpg,], B[*.jpg,], C[*.jpg,], ...]
    For This Data tree (path = "Data/")
    """
    
    labelIndex = 0
    features_df = pd.DataFrame(columns=_columns)
    labels = []

    for dir in os.listdir(_path):
        for img in os.listdir(f"{_path}/{dir}"):
            img = cv2.imread(f"{_path}/{dir}/{img}")                        # Reading Image
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                     # Converting Image from RGB to Gray Scale (1 Channel)
            img = cv2.resize(img, (_imgSize, _imgSize))                     # Resizing Image to (64 X 64)
            img = np.asarray(img)
            img = img.flatten()                                             # Converting 2D array to 1D [[64], [64] ... [64]] = [4096]
            
            temp_df = pd.DataFrame(img.reshape(1,-1),columns=_columns)      # Appending Features
            features_df = pd.concat([features_df, temp_df]) 
            
            labels.append(labelIndex)                                       # Appending Labels

        labelIndex += 1
        

    # Storing Features into CSV File
    features_df.to_csv("features.csv", index=False)                        # Saving Features DataFrame into CSV File

    labels_df = pd.DataFrame(labels, columns=["label"])                     # Converting Labels(np array) into a Pandas DataFrame
    labels_df.to_csv("labels.csv", index=False)                             # Saving Labels DataFrame into CSV File


    print(f"'{features_df.shape[0]}' Features are added Successfully!")
    print(f"\nThe shape fo Features is '{features_df.shape}'")



if __name__ == "__main__":
    
    path = "data/"
    imgSize = 64
    columns = CreateColumns(imgSize)

    Image2CSV(path, columns, imgSize)

