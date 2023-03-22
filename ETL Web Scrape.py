from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import re
import csv
import shutil

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

URL = 'https://ramuk.intertekconnect.com//WebClients/ITS/DLP/products.nsf/vwSearch?SearchView&Query=FIELD%20ListHead%20Contains%2051519%20or%20FIELD%20CatCode%20Contains%2051519%20or%20FIELD%20Title%20Contains%2051519%20or%20FIELD%20ProductInformation%20Contains%2051519%20or%20FIELD%20ProductInfo%20Contains%2051519&SearchOrder=1&SearchMax=1000&SearchWV=FALSE&SearchThesaurus=FALSE&SearchFuzzy=TRUE'
modelfile='ETL Database Results.csv'
#dateparse = lambda x: datetime.strptime(x, '%Y-%m-%d)
driver.get(URL)
models=pd.read_csv(modelfile,header=0,parse_dates=True)
print(models)
pack=models[models.columns[0]].tolist()
models=models[models.columns[1]].tolist()
#esw=pd.DataFrame(models[models.columns[3]])
#esw=esw.tolist()
#notes=models["notes"].tolist()
#esw=models["esw"].tolist()
#lsw=models["lsw"].tolist()

#print(models)
#models =['ZB-18','2141','10300','110618-KIT','1319','9322CH','AF-20-2']
header=["packnumber","Model#","Intertek Results"]
finalresult=[]
for model in models:
    ###enters model number in search bar and "hits enter"
    driver.find_element(By.ID, "SearchInfo").send_keys(model + Keys.ENTER)

    ###"collects the number of results returned"
    results = driver.find_elements(By.XPATH,"//span[contains(@class, 'smTxt')]")

    for r in results:
        ###removes all characters except the number 
        
        final=[int(s) for s in re.findall(r'\b\d+\b', r.get_attribute('innerHTML'))][1]
        finalresult.append(final)
        
#print(finalresult)
        #print([int(s) for s in re.findall(r'\b\d+\b', r.get_attribute('innerHTML'))][1])

filename = datetime.now().strftime('ETL Results.csv')
with open(filename, 'w',newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(zip(pack,models,finalresult))    
        
driver.quit()
df1=pd.read_csv(filename)
df2=pd.read_csv(modelfile)
lj=pd.merge(df1,df2,on='packnumber',how='left')

lj.to_csv('etlresults %m%d%Y.csv')
#srcpath=r"C:\Users\113423\\"
#destpath=r"\\page\data\Global_Compliance\Groups\Jordan\\"
#shutil.move(srcpath+filename,destpath+filename)
#pandas.close(modelfile)
