Acquiring Stock Symbols
================

## Introduction

This document aims to obtain a list of stock symbols for the stock
listed on either HKEX, the US stock exchanges or the FX market. The
symbol describing the same equity might be vary in different
websites/documents, especially for those ETF symbols in the US market.
The symbols obtained from this document are compatible with those used
in Yahoo Finance API.

## Equity Symbols in HKEX

A full list of security symbols can be found from the [HKEX
website](https://www.hkex.com.hk/Services/Trading/Securities/Overview/Trading-Mechanism?sc_lang=en).
The direct url to the Excel spreadsheet is listed below.

``` text
https://www.hkex.com.hk/eng/services/trading/securities/securitieslists/ListOfSecurities.xlsx
```

### Using Python

``` python
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

def HKSymbolForYahooAPI():
    # This function extracts the symbols and converts them into those 
    # can be used in the Yahoo Finance API.
    import re
    response = HKSymbol()
    symbols = response["Stock Code"].loc[response["Category"].isin(
        ["Real Estate Investment Trusts", "Exchange Traded Products", "Equity"]
    )]
    symbols = symbols.apply(lambda x: re.sub("^0", "", x) + ".HK")
    return(list(symbols))
```

Below shows the results of the above functions.

``` python
symbolTbl = HKSymbol()
```

|     | Stock Code | Name of Securities | Category | Sub-Category                   | Board Lot | Par Value  | ISIN         | Expiry Date | Subject to Stamp Duty | Shortsell Eligible | CAS Eligible | VCM Eligible | Admitted to Stock Options | Admitted to Stock Futures | Admitted to CCASS | ETF / Fund Manager | Debt Securities Board Lot (Nominal) | Debt Securities Investor Type | POS Eligble | Spread Table, 4 = Part A = Part B = Part D | NaN  |
|:----|:-----------|:-------------------|:---------|:-------------------------------|----------:|:-----------|:-------------|:------------|:----------------------|:-------------------|:-------------|:-------------|:--------------------------|:--------------------------|:------------------|:-------------------|:------------------------------------|:------------------------------|:------------|:-------------------------------------------|:-----|
| 3   | 00001      | CKH HOLDINGS       | Equity   | Equity Securities (Main Board) |       500 | HKD 1.0000 | KYG217651051 | NULL        | Y                     | Y                  | Y            | Y            | Y                         | Y                         | Y                 | NULL               | NULL                                | NULL                          | Y           | 1                                          | NULL |
| 4   | 00002      | CLP HOLDINGS       | Equity   | Equity Securities (Main Board) |       500 |            | HK0002007356 | NULL        | Y                     | Y                  | Y            | Y            | Y                         | Y                         | Y                 | NULL               | NULL                                | NULL                          | Y           | 1                                          | NULL |
| 5   | 00003      | HK & CHINA GAS     | Equity   | Equity Securities (Main Board) |      1000 |            | HK0003000038 | NULL        | Y                     | Y                  | Y            | Y            | Y                         | Y                         | Y                 | NULL               | NULL                                | NULL                          | Y           | 1                                          | NULL |
| 6   | 00004      | WHARF HOLDINGS     | Equity   | Equity Securities (Main Board) |      1000 |            | HK0004000045 | NULL        | Y                     | Y                  | Y            | Y            | Y                         | Y                         | Y                 | NULL               | NULL                                | NULL                          | Y           | 1                                          | NULL |
| 7   | 00005      | HSBC HOLDINGS      | Equity   | Equity Securities (Main Board) |       400 | USD 0.5000 | GB0005405286 | NULL        | Y                     | Y                  | Y            | Y            | Y                         | Y                         | Y                 | NULL               | NULL                                | NULL                          | Y           | 1                                          | NULL |
| 8   | 00006      | POWER ASSETS       | Equity   | Equity Securities (Main Board) |       500 |            | HK0006000050 | NULL        | Y                     | Y                  | Y            | Y            | Y                         | Y                         | Y                 | NULL               | NULL                                | NULL                          | Y           | 1                                          | NULL |

The Yahoo Finance AIP recognizes the following symbols.

``` python
symbols = HKSymbolForYahooAPI()
symbols[0:10]
```

    ## ['0001.HK', '0002.HK', '0003.HK', '0004.HK', '0005.HK', '0006.HK', '0007.HK', '0008.HK', '0009.HK', '0010.HK']

### Using R

``` r
HKSymbol <- function(){
    url <- "https://www.hkex.com.hk/eng/services/trading/securities/securitieslists/ListOfSecurities.xlsx"
    response <- as.data.frame(readtext::readtext(url))
    names(response) <- unname(unlist(response[2, ]))
    response <- response[3:nrow(response), ]
    response[, 1] <- NULL
    
    return(response)
}

HKSymbolForYahooAPI <- function(){
    # This function extracts the symbols and converts them into those 
    # can be used in the Yahoo Finance API.
    response <- HKSymbol()
    symbols <- response$`Stock Code`[response$Category %in% c("Real Estate Investment Trusts", "Exchange Traded Products", "Equity")]
    symbols <- paste0(gsub("^0", "", symbols), ".HK")
    return(symbols)
}
```

Below shows the results of the above functions.

``` r
response <- HKSymbol()
names(response) <- gsub("\r\n", "\\\\n", names(response))
knitr::kable(head(response))
```

|     | Stock Code | Name of Securities | Category | Sub-Category                   | Board Lot | Par Value  | ISIN         | Expiry Date | Subject to Stamp Duty | Shortsell Eligible | CAS Eligible | VCM Eligible | Admitted to Stock Options | Admitted to Stock Futures | Admitted to CCASS | ETF / Fund Manager | Debt Securities Board Lot (Nominal) | Debt Securities Investor Type | POS Eligble | Spread Table1, 4 = Part A = Part B = Part D |
|:----|:-----------|:-------------------|:---------|:-------------------------------|:----------|:-----------|:-------------|:------------|:----------------------|:-------------------|:-------------|:-------------|:--------------------------|:--------------------------|:------------------|:-------------------|:------------------------------------|:------------------------------|:------------|:--------------------------------------------|
| 3   | 00001      | CKH HOLDINGS       | Equity   | Equity Securities (Main Board) | 500       | HKD 1.0000 | KYG217651051 | NA          | Y                     | Y                  | Y            | Y            | Y                         | Y                         | Y                 | NA                 | NA                                  | NA                            | Y           | 1                                           |
| 4   | 00002      | CLP HOLDINGS       | Equity   | Equity Securities (Main Board) | 500       | NA         | HK0002007356 | NA          | Y                     | Y                  | Y            | Y            | Y                         | Y                         | Y                 | NA                 | NA                                  | NA                            | Y           | 1                                           |
| 5   | 00003      | HK & CHINA GAS     | Equity   | Equity Securities (Main Board) | 1,000     | NA         | HK0003000038 | NA          | Y                     | Y                  | Y            | Y            | Y                         | Y                         | Y                 | NA                 | NA                                  | NA                            | Y           | 1                                           |
| 6   | 00004      | WHARF HOLDINGS     | Equity   | Equity Securities (Main Board) | 1,000     | NA         | HK0004000045 | NA          | Y                     | Y                  | Y            | Y            | Y                         | Y                         | Y                 | NA                 | NA                                  | NA                            | Y           | 1                                           |
| 7   | 00005      | HSBC HOLDINGS      | Equity   | Equity Securities (Main Board) | 400       | USD 0.5000 | GB0005405286 | NA          | Y                     | Y                  | Y            | Y            | Y                         | Y                         | Y                 | NA                 | NA                                  | NA                            | Y           | 1                                           |
| 8   | 00006      | POWER ASSETS       | Equity   | Equity Securities (Main Board) | 500       | NA         | HK0006000050 | NA          | Y                     | Y                  | Y            | Y            | Y                         | Y                         | Y                 | NA                 | NA                                  | NA                            | Y           | 1                                           |

The Yahoo Finance AIP recognizes the following symbols.

``` r
head(HKSymbolForYahooAPI())
```

    ## [1] "0001.HK" "0002.HK" "0003.HK" "0004.HK" "0005.HK" "0006.HK"

## Equity Symbols in US Market

A list of equity symbols can be found from
[nasdaqtrader.com](http://www.nasdaqtrader.com/trader.aspx?id=symboldirdefs).

### Using Python

``` python
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
```

Yahoo Finance API recognizes the following symbols.

``` python
response = USSymbol()
```

|     | Symbol | Security Name                                                                                                              | Exchange | ETF | Round Lot Size |
|:----|:-------|:---------------------------------------------------------------------------------------------------------------------------|:---------|:----|---------------:|
| 0   | A      | Agilent Technologies, Inc. Common Stock                                                                                    | N        | N   |            100 |
| 1   | AA     | Alcoa Corporation Common Stock                                                                                             | N        | N   |            100 |
| 2   | AAA    | Listed Funds Trust AAF First Priority CLO Bond ETF                                                                         | P        | Y   |            100 |
| 3   | AAAU   | Goldman Sachs Physical Gold ETF Shares                                                                                     | P        | Y   |            100 |
| 4   | AAC    | Ares Acquisition Corporation Class A Ordinary Shares                                                                       | N        | N   |            100 |
| 5   | AAC-UN | Ares Acquisition Corporation Units, each consisting of one Class A ordinary share, and one-fifth of one redeemable warrant | N        | N   |            100 |

### Using R

``` r
getUSSymbolsList <- function(){
    files <- "nasdaqtraded.txt"
    column.names <- c("^Symbol$", "^Security.Name$", "^Exchange$", "^ETF$", "^Round.Lot.Size$")
    
    url <- paste0("ftp://ftp.nasdaqtrader.com/SymbolDirectory/", files)
    response <- read.csv(url, header = T, sep = "|", as.is = T)
    response <- response[response$Test.Issue != "Y", ]
    response <- response[-nrow(response), ]
    
    response$Symbol <- response$NASDAQ.Symbol
    response$Exchange <- response$Listing.Exchange
    
    pattern <- c("-", "=", "#", "\\.", "\\+", "\\^")
    replace <- c("-P", "-UN", "-WI", "-", "-WT", "-RI")
    
    invisible(mapply(function(x, y){
        response$Symbol <<- gsub(x, y, response$Symbol)
    }, pattern, replace))
    
    col.loc <- sapply(column.names, grep, names(response))
    response <- response[, c(col.loc, recursive = T)]
    
    return(response)
}
```

Yahoo Finance API recognizes the following symbols.

``` r
knitr::kable(head(getUSSymbolsList()))
```

| Symbol | Security.Name                                                                                                              | Exchange | ETF | Round.Lot.Size |
|:-------|:---------------------------------------------------------------------------------------------------------------------------|:---------|:----|---------------:|
| A      | Agilent Technologies, Inc. Common Stock                                                                                    | N        | N   |            100 |
| AA     | Alcoa Corporation Common Stock                                                                                             | N        | N   |            100 |
| AAA    | Listed Funds Trust AAF First Priority CLO Bond ETF                                                                         | P        | Y   |            100 |
| AAAU   | Goldman Sachs Physical Gold ETF Shares                                                                                     | P        | Y   |            100 |
| AAC    | Ares Acquisition Corporation Class A Ordinary Shares                                                                       | N        | N   |            100 |
| AAC-UN | Ares Acquisition Corporation Units, each consisting of one Class A ordinary share, and one-fifth of one redeemable warrant | N        | N   |            100 |

## Forex Symbols

Most of the currency in the world have can be represented by
[ISO-4217](https://www.iso.org/iso-4217-currency-codes.html), a three
letters combination. An XML table mapping the curreny to the ISO-4217
can be found form the below url.

``` text
https://www.currency-iso.org/dam/downloads/lists/list_one.xml
```

Yahoo Finance API takes a forex symbol in the form of `CUR1CUR2=X`,
where `CUR1` and `CUR2` are two distinct ISO-4217 currency code. For
example, the forex symbol converting `HKD` to `USD` is given by
`HKDUSD=X`.

### Using Python

``` python
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
```

``` python
df = FXSymbol()
```

| Entity         | Currency       | Symbol | Num Symbol | Minor Unit |
|:---------------|:---------------|:-------|:-----------|:-----------|
| AFGHANISTAN    | Afghani        | AFN    | 971        | 2          |
| ÅLAND ISLANDS  | Euro           | EUR    | 978        | 2          |
| ALBANIA        | Lek            | ALL    | 008        | 2          |
| ALGERIA        | Algerian Dinar | DZD    | 012        | 2          |
| AMERICAN SAMOA | US Dollar      | USD    | 840        | 2          |
| ANDORRA        | Euro           | EUR    | 978        | 2          |

Below converts the ISO-4217 currency code into symbols that are used in
Yahoo Finance API. As we usually only interested in the conversion
between one currency and another *major* currency. We define the *major*
currency as the following list.

``` text
["HKD", "USD", "EUR", "GBP", "JPY", "AUD", "NZD", "CAD", "CHF"]
```

``` python
import itertools
currency = list(set(list(df["Symbol"])))
currency = [x for x in currency if ((isinstance(x, str)) and (len(x) == 3))]
imp_currency = ["HKD", "USD", "EUR", "GBP", "JPY", "AUD", "NZD", "CAD", "CHF"]

symbols = [[y + x + "=X" for y in currency] for x in imp_currency]
symbols = list(itertools.chain(*symbols))

symbols_rev = [[x + y + "=X" for y in currency] for x in imp_currency]
symbols_rev = list(itertools.chain(*symbols_rev))

remove_symbols = [x + x + "=X" for x in imp_currency]

symbols = list(set(symbols) - set(remove_symbols))

symbols[0:10]
```

    ## ['MMKCAD=X', 'RSDUSD=X', 'XBBAUD=X', 'CADAUD=X', 'XPTAUD=X', 'XCDHKD=X', 'ARSHKD=X', 'SRDGBP=X', 'MXNCAD=X', 'KRWEUR=X']

### Using R

``` r
getFXSymbolsList <- function(){
    response <- httr::content(httr::GET("https://www.currency-iso.org/dam/downloads/lists/list_one.xml"))
    tbl <- rvest::html_nodes(response, "CcyNtry")
    
    attr_names <- c("CtryNm", "CcyNm", "Ccy", "CcyNbr", "CcyMnrUnts")
    
    result <- as.data.frame(t(sapply(tbl, function(x){
        sapply(attr_names, function(y){
        node_result <- rvest::html_text(rvest::html_nodes(x, y))
        return(ifelse(identical(node_result, character(0)), NA, node_result))
        })
    })))
    
    names(result) <- c("Entity", "Currency", "Symbol", "Num.Symbol", "Minor.Unit")
    return(result)
}
```

``` r
df <- getFXSymbolsList()
knitr::kable(head(df))
```

| Entity         | Currency       | Symbol | Num.Symbol | Minor.Unit |
|:---------------|:---------------|:-------|:-----------|:-----------|
| AFGHANISTAN    | Afghani        | AFN    | 971        | 2          |
| ÅLAND ISLANDS  | Euro           | EUR    | 978        | 2          |
| ALBANIA        | Lek            | ALL    | 008        | 2          |
| ALGERIA        | Algerian Dinar | DZD    | 012        | 2          |
| AMERICAN SAMOA | US Dollar      | USD    | 840        | 2          |
| ANDORRA        | Euro           | EUR    | 978        | 2          |

Below converts the ISO-4217 currency code into symbols that are used in
Yahoo Finance API. As we usually only interested in the conversion
between one currency and another *major* currency. We define the *major*
currency as the following list.

``` text
["HKD", "USD", "EUR", "GBP", "JPY", "AUD", "NZD", "CAD", "CHF"]
```

``` r
currency <- unique(df$Symbol)
currency <- currency[!is.na(currency)]

imp_currency <- c("HKD", "USD", "EUR", "GBP", "JPY", "AUD", "NZD", "CAD", "CHF")

symbols <- c(sapply(imp_currency, function(x){
    return(paste0(currency, x, "=X"))
}))

symbols <- append(symbols, c(sapply(imp_currency, function(x){
    return(paste0(x, currency, "=X"))
})))

symbols <- unique(symbols[-which(symbols %in% paste0(imp_currency, imp_currency, "=X"))])

head(symbols, 10)
```

    ##  [1] "AFNHKD=X" "EURHKD=X" "ALLHKD=X" "DZDHKD=X" "USDHKD=X" "AOAHKD=X"
    ##  [7] "XCDHKD=X" "ARSHKD=X" "AMDHKD=X" "AWGHKD=X"
