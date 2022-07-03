import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


class Tf_Idf:
    def __init__(self, address):
        self.document = self.get_document(address)
        self.DTM = []
        self.DF = []
        self.result = []
        self.words_index = {}

        self.make_DTM()
        self.calculate_DF()
        self.TfIdf()
        self.to_dataframe()
        # self.visualization()

    def get_document(self, address):
        doc = []
        file = os.listdir(address)
        for i in file:
            if '.txt' in i:
                with open(address + "\\" + i, 'r', encoding='utf-8') as file:
                    contents = file.readlines()
                contents = ''.join(contents)
                contents = contents.replace("\n", "")
                contents = contents.replace(".", "")
                doc.append(contents)
        return doc

    def make_DTM(self):
        # Make words index tuple
        for pointer in self.document:
            word_list = pointer.split(' ')
            for check in word_list:
                if check.upper() not in self.words_index:
                    self.words_index[check.upper()] = len(self.words_index)

        # Count the number of words in each document
        for pointer in self.document:
            col = []
            for element in self.words_index:
                col.append(pointer.upper().count(element))
            self.DTM.append(col)

    def calculate_DF(self):
        for pointer in self.words_index:
            num = 0
            for i in self.DTM:
                if i[self.words_index[pointer]] >= 1:
                    num += 1
            self.DF.append(num)

    def TfIdf(self):
        for index in self.DTM:
            col = []
            for value in range(len(index)):
                Tf_Idf_Value = index[value] * (math.log((len(self.document) + 1) / (1 + self.DF[value])) + 1)
                col.append(Tf_Idf_Value)
            self.result.append(col)

    def to_dataframe(self):
        self.df = pd.DataFrame(self.result, columns=self.words_index.keys())
        # self.df = pd.DataFrame(self.result)
        self.df = (self.df - self.df.mean()) / self.df.std()

    def visualization(self):
        plt.figure(figsize=(len(self.words_index) * 2, len(self.document) * 2))
        # plt.figure()
        sns.heatmap(data=self.df, annot=True, fmt='.2f', cmap='Blues')


if __name__ == '__main__':
    address = input("텍스트가 저장되어 있는 폴더의 주소를 입력하세요:")
    print("파일 개수: ", len(os.listdir(address)))
    print("프로그램 실행 중....")
    tfidf = Tf_Idf(address)
    print("계산 완료!")
    print("발견한 txt파일 수: ", len(tfidf.document))
    print("행렬 크기: {}X{}".format(len(tfidf.DTM), len(tfidf.DTM[0])))
    save = input("결과를 저장하겠습니까? Y/N")
    if save.upper() == "Y":
        add = input("저장할 주소를 입력하세요:")
        tfidf.df.to_csv(add + "\\tfidf.csv", mode='a',encoding="utf-8")
        print("저장이 완료되었습니다.")
    os.system("pause")