HKSymbol <- function(){
    url <- "https://www.hkex.com.hk/eng/services/trading/securities/securitieslists/ListOfSecurities.xlsx"
    response <- as.data.frame(readtext::readtext(url))
    names(response) <- unname(unlist(response[2, ]))
    response <- response[3:nrow(response), ]
    response[, 1] <- NULL
    
    return(response)
}

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
