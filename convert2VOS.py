from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

with open("LabelsNode.txt", 'r+') as Xoa:
    Xoa.truncate(0)
    Xoa.close()
with open("ConectpaperFile.txt", 'r+') as Xoa:
    Xoa.truncate(0)
    Xoa.close()

a = "https://www.connectedpapers.com/main/8d6d8711b76be49569ae18b8e7712af3676090a0/A-homogenized-Reissner%20Mindlin-model-for-orthotropic-periodic-plates%3A-Application-to-brickwork-panels/graph"

driver = webdriver.Edge()
driver.get(a)
wait = WebDriverWait(driver, 10)
time.sleep(5)
print("Đã chạy 1")
print("đã click")

#tạo các list rỗng
CX_List = []
CY_List = []
Weight_List = []

Labels_List = []
X_Labels_List = []
Y_Labels_List = []
temp_list = []

Edges_X1 = []
Edges_Y1 = []
Edges_X2 = []
Edges_Y2 = []
Edges_Strength = []

i = 0
j = 0
#tìm tọa độđộ các nodes
nodes = driver.find_elements(By.XPATH,"//*[name()='circle' and @class='node-circle']") #khi xử lý SVG cần xử lý như bên cạnh, tìm tương đối.
for item in nodes:
    CX = item.get_attribute("cx")
    CY = item.get_attribute("cy")

    i = i +1
    CX_List.append(CX)
    CY_List.append(CY)
    Weight_List.append(float(item.get_attribute("r")))
print("Đã lấy xong các node")
#tìm các label
# ghi = open('ConectpaperFile.txt', "r+", encoding="utf-8")
Labels = driver.find_elements(By.XPATH,"//*[name()='text' and @visibility='visible']")
for item in Labels:
    Labels_List.append(item.text)
    X_Labels_List.append(item.get_attribute("x"))
    Y_Labels_List.append(item.get_attribute("y"))
    temp_list.append("Rong")
    j = j+1
print("Đã chạy 2")
print("nodes: ", i, ", Labels: ",j)

#tìm các cạnh

Edges = driver.find_elements(By.XPATH,"//*[name()='g' and @class='edges']//*[local-name() = 'line']")
for item in Edges:
    Edges_X1.append(item.get_attribute("x1"))
    Edges_Y1.append(item.get_attribute("y1"))
    Edges_X2.append(item.get_attribute("x2"))
    Edges_Y2.append(item.get_attribute("y2"))
    Edges_Strength.append(float(item.get_attribute("stroke-width")))


#tìm hệ số hiệu chỉnh vị trí text


k = 0
Coefficient = 0
for k in range(len(CX_List)):
#   print(CX_List[k],CY_List[k])
    for m in range(len(X_Labels_List)):
        if X_Labels_List[m] == CX_List[k]:
            CoefficientLC = float(Y_Labels_List[m]) - float(CY_List[k])
            break
for n in range(len(Y_Labels_List)):
    Y_Labels_List[n] = float(Y_Labels_List[n]) - CoefficientLC

#sap xep lai :Labels theo CX, CY
ghi = open('LabelsNode.txt',"r+", encoding="utf-8")
ghi.write("id	label	x	y	cluster	weight<Links>	weight<Total link strength>	weight<Documents>	weight<Citations>	weight<Norm. citations>	score<Avg. pub. year>	score<Avg. citations>	score<Avg. norm. citations>"+"\n")
for i in range(len(X_Labels_List)):
    ID_Labels = CX_List.index(X_Labels_List[i])
    if float(Y_Labels_List[i]) == float(CY_List[ID_Labels]):
        temp_list[ID_Labels]=Labels_List[i]
        print(Labels_List[i])
#ghi vào file ID, tên, tọa độ x, y, cluster = 1, Weight, còn lại = 1 
for i in range(len(temp_list)):
    ghi.write(str((i+1))+"\t"+temp_list[i]+"\t"+CX_List[i]+"\t"+CY_List[i]+"\t"+"1"+"\t"+str((1000*Weight_List[i]/min(Weight_List)))+"\t"+"1"+"\t"+"1"+"\t"+"1"+"\t"+"1"+"\t"+"1"+"\t"+"1"+"\t"+"1"+"\n")
ghi.close()

#Xử lý các edges
ghi2 = open('ConectpaperFile.txt',"r+", encoding="utf-8")
for l in range(len(Edges_X1)):
    ID = CX_List.index(Edges_X1[l])
    ID2 = CX_List.index(Edges_X2[l])
    ghi2.write(str(ID+1)+"\t"+str(ID2+1)+"\t"+str(10*Edges_Strength[l]/min(Edges_Strength))+"\n")  
ghi2.close()    
# for l in range(len(Edges_X1)):
#     print("x1: ", Edges_X1[l],"y1: ", Edges_Y1[l],"x2: ",Edges_X2[l],"y2: ",Edges_Y2[l], "Strength:", Edges_Strength[l])
print("Hoàn thành!")
x = input()
if x == 0: driver.quit