import math
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns  


class Tf_Idf:
    def __init__(self,document):
        self.document = document
        self.DTM = []
        self.DF = []
        self.result = []
        self.words_index = {}
        
        self.make_DTM()
        self.calculate_DF()
        self.TfIdf()
        self.to_dataframe()
        self.visualization()
        
    def make_DTM(self):
        # Make words index tuple
        for pointer in self.document:
            word_list = pointer.split(' ')
            for check in word_list:
                if check.upper() not in self.words_index:
                    self.words_index[check.upper()] = len(self.words_index)
        
        #Count the number of words in each document
        for pointer in self.document:
            col = []
            for element in self.words_index:
                col.append(pointer.upper().count(element))
            self.DTM.append(col)
        
    def calculate_DF(self):
        for pointer in self.words_index:
            num = 0
            for i in self.DTM:
                if i[self.words_index[pointer]]>=1:
                    num+=1
            self.DF.append(num)
            
    def TfIdf(self):
        for index in self.DTM:
            col = []
            for value in range(len(index)):
                Tf_Idf_Value = index[value]*(math.log((len(self.document)+1)/(1+self.DF[value]))+1)
                col.append(Tf_Idf_Value)
            self.result.append(col)
            
    def to_dataframe(self):
        self.df = pd.DataFrame(self.result, columns  = self.words_index.keys())
        #self.df = pd.DataFrame(self.result)
        self.df = (self.df - self.df.mean())/self.df.std()
    
    def visualization(self):
        plt.figure(figsize=(len(self.words_index)*2,len(self.document)*2))
        #plt.figure()
        sns.heatmap(data = self.df, annot=True, fmt = '.2f', cmap='Blues')
        plt.show()
