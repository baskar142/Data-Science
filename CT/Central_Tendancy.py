import pandas as pd
import numpy as np

class CT:
    
    def QuanQual(self, df):
        quan = []
        qual = []
        for columnName in df.columns:
            if df[columnName].dtype == 'O':
                qual.append(columnName)
            else:
                quan.append(columnName)
        return quan, qual

    def compute_descriptive_statistics(self, df, quan):
        descriptive = pd.DataFrame(index=["Mean", "Median", "Mode", "Q1:25%", "Q2:50%", "Q3:75%", "99%", "Q4:100%", "IQR", "1.5rule", "Lesser", "Greater", "Min", "Max"], columns=quan)
        
        for columnName in quan:
            descriptive[columnName]["Mean"] = df[columnName].mean()
            descriptive[columnName]["Median"] = df[columnName].median()
            descriptive[columnName]["Mode"] = df[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"] = df.describe()[columnName]["25%"]
            descriptive[columnName]["Q2:50%"] = df.describe()[columnName]["50%"]
            descriptive[columnName]["Q3:75%"] = df.describe()[columnName]["75%"]
            descriptive[columnName]["99%"] = np.percentile(df[columnName], 99)
            descriptive[columnName]["Q4:100%"] = df.describe()[columnName]["max"]
            descriptive[columnName]["IQR"] = descriptive[columnName]["Q3:75%"] - descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5rule"] = 1.5 * descriptive[columnName]["IQR"]
            descriptive[columnName]["Lesser"] = descriptive[columnName]["Q1:25%"] - descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Greater"] = descriptive[columnName]["Q3:75%"] + descriptive[columnName]["1.5rule"]
            descriptive[columnName]["Min"] = df[columnName].min()
            descriptive[columnName]["Max"] = df[columnName].max()
        
        return descriptive

    def freqTable(self, columnName, df):
        freqTable = pd.DataFrame(columns=["Unique_values","Frequency", "Relative_Frequency", "Cumulative"])
        freqTable["Unique_values"] = df[columnName].value_counts().index
        freqTable["Frequency"] = df[columnName].value_counts().values
        freqTable["Relative_Frequency"] = freqTable["Frequency"] / 100
        freqTable["Cumulative"] = freqTable["Relative_Frequency"].cumsum()
        return freqTable

    def find_outlier(self, descriptive, quan):
        lesser = []
        greater = []
        
        # Find columns with outliers
        for columnName in quan:
            if descriptive[columnName]["Min"] < descriptive[columnName]["Lesser"]:
                lesser.append(columnName)
            if descriptive[columnName]["Max"] > descriptive[columnName]["Greater"]:
                greater.append(columnName)
        return lesser, greater

    def replace_outlier(self, descriptive, quan, df):
        lesser, greater = self.find_outlier(descriptive, quan)
        
        for columnName in lesser:
            df.loc[df[columnName] < descriptive[columnName]["Lesser"], columnName] = descriptive[columnName]["Lesser"]
        for columnName in greater:
            df.loc[df[columnName] > descriptive[columnName]["Greater"], columnName] = descriptive[columnName]["Greater"]
        
        return df
