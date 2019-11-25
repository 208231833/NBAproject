from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import time

start = time.time()

months = ["october","november","december","january","february","march","april"]

col_header = ["Date","Start(ET)","Visitor/Neutral","PTS","Home/Neutral","PTS","","","Attend","Notes"]
url = "https://www.basketball-reference.com/leagues/NBA_{}_games-"
for z in range(2020,2021):
    NBA_Schedule_and_results = []
    for month in months:
        urls = url.format(z) + month + ".html"
        html = urlopen(urls)
        soup = BeautifulSoup(html,"lxml")
        start_1 = time.time()
        print(month)
        for i in range(len(soup.tbody.findAll("tr"))):
            Schedule = []
            date = soup.tbody.findAll("tr")[i].findAll("th")[0].getText()
            Schedule.append(date)
            for j in range(len(soup.findAll("tr")[i].findAll("td"))):
                data = soup.findAll("tr")[i].findAll("td")[j].getText()
                Schedule.append(data)
            NBA_Schedule_and_results.append(Schedule)
        end_1 = time.time()
        print(month,round(end_1 - start_1,2),"s")
    df = pd.DataFrame(NBA_Schedule_and_results,columns = col_header)
    df.to_csv("NBA_{}_{}_Schedule_and_results.csv".format(z - 1, z))
end = time.time()
print("The total time used:",round(end - start,2),"s")



































