def HKSymbol():
    import re
    import requests
    import openpyxl
    import pandas as pd
    from io import BytesIO

    url = "https://www.hkex.com.hk/eng/services/trading/securities/securitieslists/ListOfSecurities.xlsx"
    wb = openpyxl.load_workbook(filename=BytesIO(requests.get(url).content))
    response = pd.DataFrame(wb.active.values)
    
    response.columns = response.iloc[2].to_list()
    response = response.drop([0, 1, 2] + [i for i, x in enumerate(list(response["Stock Code"])) if x is None])
    
    response["Board Lot"] = response["Board Lot"].apply(lambda x: int(re.sub("\,", "", x)))
    return(response)

def USSymbol():
    import pandas as pd
    file = "nasdaqtraded.txt"
    url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/" + file
    
    response = pd.read_csv(url, sep = "|")
    response = response.iloc[[i for i, x in enumerate(response["Test Issue"].to_list()) if x != "Y"]][:-1]
    
    response["Symbol"] = response["NASDAQ Symbol"]
    response["Exchange"] = response["Listing Exchange"]
    
    response["Symbol"] = response["Symbol"].str.replace("-", "-P", regex = True)
    response["Symbol"] = response["Symbol"].str.replace("=", "-UN", regex = True)
    response["Symbol"] = response["Symbol"].str.replace("#", "-WI", regex = True)
    response["Symbol"] = response["Symbol"].str.replace("\.", "-", regex = True)
    response["Symbol"] = response["Symbol"].str.replace("\+", "-WT", regex = True)
    response["Symbol"] = response["Symbol"].str.replace("\^", "-RI", regex = True)
    
    response = response[["Symbol", "Security Name", "Exchange", "ETF", "Round Lot Size"]]
    return(response)

def FXSymbol():
    import xmltodict
    import requests
    import pandas as pd
    response = requests.get("https://www.currency-iso.org/dam/downloads/lists/list_one.xml")
    
    xml = xmltodict.parse(response.text).get("ISO_4217").get("CcyTbl").get("CcyNtry")
    xml = list(map(lambda x: pd.DataFrame.from_dict(dict(xml[x]), orient = "index").transpose(), range(len(xml))))
    xml = pd.concat(xml)
    xml.columns = ["Entity", "Currency", "Symbol", "Num Symbol", "Minor Unit"]
    return(xml)
