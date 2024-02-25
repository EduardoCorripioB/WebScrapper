import bs4
import requests
import pyodbc
from datetime import *

#CreatelistFunction
def createlist(bsvar):
    list = []
    for n in bsvar:
        list.append(n.text)
    return list


#Getpagedata
paginabase = 'https://www.coindesk.com/data/'
requestwebpage = requests.get(paginabase)
bswebpage = bs4.BeautifulSoup(requestwebpage.text, 'lxml')

#Constant directions
coinandabradd = '.inner-column'
coinpriceadd = '.typography__StyledTypography-sc-owin6q-0.lnOdBs'


#Getdata
#Coinnames
coindatabs = bswebpage.select(coinandabradd)
coinnamelist = createlist(coindatabs)
#Coinprices
coinpricebs = bswebpage.select(coinpriceadd)
coinpricelist = createlist(coinpricebs)

todaydate = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')

#########################################
#SQL Database conection
databaseconnection = pyodbc.connect('''Driver={ODBC Driver 18 for SQL Server};
Server=tcp:cryptodataproject.database.windows.net,1433;
Database=cryptodata;Uid=crypto;Pwd=Contrasena1!;
Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30''')

database = databaseconnection.cursor()

#SQL push data to database
i = 0
while i<1:
    database.execute(f'''INSERT INTO dbo.Crypto(Coin,Price,Date) 
    VALUES 
    ('{coinnamelist[i]}','{coinpricelist[i][1:]}','{todaydate}')''')

    i += 1

database.commit()
