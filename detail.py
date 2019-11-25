#coding=utf-8
from selenium import webdriver
import pandas as pd
driver=webdriver.Chrome()
driver.get("https://www.basketball-reference.com/leagues/NBA_2020.html")
content=driver.find_element_by_id("misc_stats").text
driver.close()
columns = [str.split() for str in content.split("\n")][1][:25]
temp_list=[str.split() for str in content.split("\n")[2:]]
result_list=[]
for str_list in temp_list:
    if len(str_list)>27:
        if str_list[3].isalpha():
            str_list[1]=str_list[1]+" "+str_list[2]+" "+str_list[3]
            str_list.pop(2)
            str_list.pop(2)
            result_list.append(str_list[:25])
        else:
            str_list[1] = str_list[1] + " " + str_list[2]
            str_list.pop(2)
            result_list.append(str_list[:25])
result_list.pop(20)
df=pd.DataFrame(result_list,columns=columns)
df.to_csv("temp.csv")