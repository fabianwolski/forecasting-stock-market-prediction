import { createContext, useState, useContext } from "react";

const StockContext = createContext()

export const StockProvider = ({children}) => {
    const [stockData, setStockData] = useState({
        historicalData: null,
        stockInfo: null,
        predictionResults: null,
        selectedModel: null, 
        loading: false,
        error: null
    })

    const updateStockData = (data) => {
        setStockData(prev => ({
            ...prev,
            historicalData: data.historical_data,
            stockInfo: data.stock_info,
            predictionResults: data.predictions,
            selectedModel: data.selectedModel, 
            loading: false,
            error: null
        }))
    }

    const setLoading = (isLoading) => {
        setStockData(prev => ({
            ...prev,
            loading: isLoading,
            error: null
        }))
    }

    const setError = (error) => {
        setStockData(prev => ({
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
    
    return (
        <StockContext.Provider value={value}>
            {children}
        </StockContext.Provider>
    )
}

export const useStock = () => {
    const context = useContext(StockContext)
    if(!context) {
        throw new Error("useStock needs to be wrapped in provider")
    }
    return context
}