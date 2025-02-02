import { createContext, useState, useContext } from "react";

const StockContext = createContext()

//i need to expose "historical_data": stock_data, "stock_info": stock_info,"predictions": metric
export const StockProvider = ({children}) =>{
    const [stockData, setStockData] = useState({
        historicalData: null,
        stockInfo: null,
        predictionResults: null,
        loading: false,
        error: null
    })

    const updateStockData = (data) => {
        setStockData(prev => ({
            ...prev,
            historicalData: data.historicalData,
            stockInfo: data.stockInfo,
            predictionResults: data.predictionResults,
            loading: false,
            error: null
        }))
    }

    const setLoading = (isLoading) =>{
        setStockData(prev=>({
            ...prev,
            loading: isLoading,
            error:null
        }))
    }

    const setError = (error) =>{
        setStockData(prev =>({
            ...prev,
            loading: false,
            error: error
        }))
    }
    const value = {
        stockData,
        updateStockData,
        setLoading,
        setError
      };
    return(
        <StockContext.Provider value={value}>
            {children}
        </StockContext.Provider>
    )
    
}

export const useStock = () =>{
    const context = useContext(StockContext)
    if(!context){
        throw new Error("useStock needs to be wrapped in provider")
    }
    return context
}
            
            