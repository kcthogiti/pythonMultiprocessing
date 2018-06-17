# -*- coding: utf-8 -*-
"""
Created on Sat Jun 16 14:27:40 2018

@author: KRISHNACHAITANYA
"""

#Load the required packages
import numpy as np
import pandas as pd

class BinAssignment:
    
    #Sorts the box dataframe
    def sortBoxes(self,df, volume, maxarea, maxDim):
        df["rankingFactor1"] = df["AvailableCapacity"]/volume > 1
        df["rankingFactor2"] = df["AvailableCapacity"]/volume
        df["rankingFactor3"] = df["Max"] > maxDim
        df["rankingFactor4"] =  df["Area"] > maxarea
        df.sort_values(by = ["Active", "rankingFactor1", "rankingFactor2","rankingFactor3", "rankingFactor3"], ascending=[False, False, True, False, False], inplace=True )

    #Logic to assign boxes to the order data
    def AssignBoxes(self,data_norm, availableBoxes):
        self.sortBoxes(availableBoxes, np.sum(data_norm["unitVolume"]), np.max(data_norm["Area"]), np.max(data_norm["Max"]) )
        total_volume = np.sum(data_norm["unitVolume"])
        boxes_df = pd.concat([availableBoxes]*data_norm.shape[0], ignore_index=False)   
        boxes_df = boxes_df.reset_index()
        for ix, row in data_norm.iterrows():
            count = 0
            vol = row["unitVolume"]
            area = row["Area"]
            dim1 = row["Min"]
            dim2 = row["Max"]
            #print(boxes_df.head())
            for ix1, row1 in boxes_df.iterrows():
                if(vol < row1["AvailableCapacity"]) & (area <= row1["Area"]) & (dim1 <= row1["Min"]) & (dim2 <= row1["Max"]):
                    availableCapacity = row1["AvailableCapacity"] - vol
                    total_volume = total_volume - vol
                    boxes_df.set_value(ix1, "AvailableCapacity", availableCapacity)
                    boxes_df.set_value(ix1, "Active", 1)
                    count = count + 1   
                    data_norm.set_value(ix, "AssignedCRT", row1["id"])
                    data_norm.set_value(ix, "AssignedBox", "Box" + str(row1["index"]))
                    break     
            self.sortBoxes(boxes_df, total_volume, np.max(data_norm[np.isnan(data_norm["AssignedCRT"])]["Area"]), np.max(data_norm[np.isnan(data_norm["AssignedCRT"])]["Max"]))  
        data_norm["AssignedBox"]= data_norm["AssignedBox"].replace(data_norm["AssignedBox"].unique(),["Box" + str(x) for x in np.arange(0,len(data_norm["AssignedBox"].unique())) ] )
        data_norm = data_norm.merge(availableBoxes, how = "inner", left_on = "AssignedCRT", right_on="id")
        data_norm = data_norm[["DIST_NO","ORDER_NO", "Item_No", "ITEM_LENGTH", "ITEM_HEIGHT", "ITEM_WIDTH", "QUANTITY", "unitVolume", "AssignedCRT", "AssignedBox", "BoxLength", "BoxHeight", "BoxWidth"]]    
        return data_norm



    def generateResults(self,  orderData, availableBoxes, outputflName):
        #Load Order Dat
        #Loop through the Orders and assign the boxes to the order data        
        Result = self.AssignBoxes(orderData, availableBoxes)

        UtilizationSummary = Result.groupby(by = ["DIST_NO", "ORDER_NO","AssignedCRT", "AssignedBox", "BoxLength", "BoxHeight", "BoxWidth"], as_index=False)[["unitVolume"]] \
                                .sum() \
                                .rename(columns = {"unitVolume":"ProductVolume"})
        UtilizationSummary["BoxVolume"] = UtilizationSummary.BoxHeight*UtilizationSummary.BoxLength*UtilizationSummary.BoxWidth
        UtilizationSummary["Utilization"] = UtilizationSummary.ProductVolume/UtilizationSummary.BoxVolume

        UtilizationSummary["id"] = UtilizationSummary["ORDER_NO"].map(str) + UtilizationSummary["AssignedBox"]
        BoxSummary = UtilizationSummary.groupby(by = ["BoxLength", "BoxWidth","BoxHeight"], as_index = False).agg({"id": lambda x: x.nunique(), "Utilization":np.mean})
        BoxSummary =  BoxSummary.rename(columns = {"id":"NumOfBoxes", "Utilization":"AvgUtilization"})
        del UtilizationSummary["id"]

        writer = pd.ExcelWriter(outputflName)
        BoxSummary.to_excel(writer, index = False, sheet_name = "BoxSummary")
        UtilizationSummary.to_excel(writer, index = False, sheet_name = "UtilizationSummary")
        Result.to_excel(writer, index = False,sheet_name="OrderData")
        availableBoxes[["id", "BoxLength", "BoxWidth", "BoxHeight"]].sort_values(by = "id").to_excel(writer, index = False, sheet_name = "Boxes")
        writer.save()
