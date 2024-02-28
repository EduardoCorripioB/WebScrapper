def cryptoscrapper():
    import bs4
    import requests
    import pyodbc
    from datetime import datetime
    import time

    #CreatelistFunction
    def createlist(bsvar):
        list = []
        for n in bsvar:
            list.append(n.text)
        return list

    def testSQL():
        databaseconnection = pyodbc.connect('''Driver={ODBC Driver 18 for SQL Server};
            Server=tcp:cryptodataproject.database.windows.net,1433;
            Database=cryptodata;Uid=account1;Pwd=Contrasena1;
            Encrypt=yes;TrustServerCertificate=no;Connection Timeout=45''')
        return databaseconnection

    sleeptimer = 5


    #Getpagedata
    paginabase = 'https://www.coindesk.com/data/'
    requestwebpage = requests.get(paginabase)
    bswebpage = bs4.BeautifulSoup(requestwebpage.text, 'lxml')

    #Constant directions
    coinandabradd = '.inner-column'
    coinpriceadd = '.typography__StyledTypography-sc-owin6q-0.lnOdBs'
    coindayperc = '.percentage'

    #Getdata
    #Coinnames
    coindatabs = bswebpage.select(coinandabradd)
    coinnamelist = createlist(coindatabs)
    #Coinprices
    coinpricebs = bswebpage.select(coinpriceadd)
    coinpricelist = createlist(coinpricebs)
    #Coinpercentage
    coinpercbs = bswebpage.select(coindayperc)
    coinperclist = createlist(coinpercbs)

    todaydate = datetime.today().strftime('%Y-%m-%dT%H:%M:%S')

    #########################################
    j = 1
    while j == 1:
        try:
           testSQL()
        except:
            print('Error en Conexion, intentando nuevamente')
            time.sleep(sleeptimer)
        else:
            j = 2
            print('Conexion y tarea exitosa')
            databaseconnection = testSQL()
            database = databaseconnection.cursor()
            i = 0
            while i<len(coinnamelist):
                database.execute(f'''INSERT INTO dbo.Crypto(Coin,Price,Date, Percentage) 
                VALUES 
                ('{coinnamelist[i]}','{coinpricelist[i][1:]}','{todaydate}','{coinperclist[i]}')''')
                i += 1
            database.commit()
