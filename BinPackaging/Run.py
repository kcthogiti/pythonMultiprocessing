# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 14:30:11 2018

@author: KRISHNACHAITANYA
"""

import BinPackagingLogic
import sys, time


inputflname = sys.argv[1]
outputflName = sys.argv[2]

if __name__ == '__main__':
    
    start = time.time()
    import numpy as np
    import pandas as pd
    pd.options.mode.chained_assignment = None  # default='warn'

    data = pd.read_excel(inputflname, sheetname="Order Data")
    data["unitVolume"] = data.ITEM_LENGTH*data.ITEM_WIDTH*data.ITEM_HEIGHT
    data["Max"] = data[["ITEM_HEIGHT", "ITEM_WIDTH", "ITEM_LENGTH"]].apply(np.max, axis =1)
    data["Min"] = data[["ITEM_HEIGHT", "ITEM_WIDTH", "ITEM_LENGTH"]].apply(np.min, axis =1)
    data["Median"] = data[["ITEM_HEIGHT", "ITEM_WIDTH", "ITEM_LENGTH"]].apply(np.median, axis =1)
    data["Area"] = data["Max"]*data["Median"]

    #Duplicate the data based on the quantity of item for each order. 
    list_rows = []
    for ix, row in data.iterrows():
        num = int(row["QUANTITY"])
        row1 = row.copy()
        row1["QUANTITY"] = 1
        dict_ = {}
        dict_.update(row1)
        for i in range(num):
            list_rows.append(dict_)

    data_norm_original = pd.DataFrame(list_rows)
    data_norm_original.sort_values(by = ["ORDER_NO", "unitVolume"], ascending=[True, False], inplace=True)
    data_norm_original["AssignedCRT"] = np.NaN
    data_norm_original["AssignedBox"] = ""
    del data


    #Load the Box Data available
    availableBoxes = pd.read_excel(inputflname, sheetname= "Boxes")
    PercentageFull = 0.8
    availableBoxes["Active"] = 0
    availableBoxes["Rank"] = 0
    availableBoxes["Volume"] = availableBoxes.BoxLength*availableBoxes.BoxWidth*availableBoxes.BoxHeight
    availableBoxes["AvailableCapacity"] = availableBoxes["Volume"]*PercentageFull
    availableBoxes.sort_values(by = ["Active", "Volume"], ascending=True, inplace=True)
    availableBoxes["Max"] = availableBoxes[["BoxLength", "BoxWidth", "BoxHeight"]].apply(np.max, axis =1)
    availableBoxes["Min"] = availableBoxes[["BoxLength", "BoxWidth", "BoxHeight"]].apply(np.min, axis =1)
    availableBoxes["Median"] = availableBoxes[["BoxLength", "BoxWidth", "BoxHeight"]].apply(np.median, axis =1)
    availableBoxes["Area"] = availableBoxes["Max"]*availableBoxes["Median"]

    analysisrun = BinPackagingLogic.BinAssignment()
    analysisrun.generateResults(data_norm_original, availableBoxes, outputflName)
    
    end = time.time()
    print("Total Time:", end-start)