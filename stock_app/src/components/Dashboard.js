import { useStock } from "../contexts/StockContext";
import StockSearchForm from "./StockSearchForm";
import StockDetails from "./StockDetails";
import StockOverview from "./StockOverview"
import StockChart from "./StockChart";
import React from "react";

const Dashboard = () =>{
    const {stockData} = useStock()
    const stockInfo = stockData.stockInfo
    const historicalData = stockData.historicalData
    const predictionResults = stockData.predictionResults
    const selectedModel = stockData.selectedModel

    return(
    <div className="h-screen grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 grid-rows-8 md-grid-rows-7 xl:grid-rows-5 auto-rows-fr gap-6 p-10 font-quicksand bg-gray-900 text-gray-300">
        <div className="col-span-1 md:col-span-2 xl:col-span-3 row-span-1 flex justify-start items-center">
            <StockSearchForm></StockSearchForm>
        </div>

        <div className="md:col-span-2 row-span-4">
            <StockChart historicalData={historicalData} predictionResults= {predictionResults} selectedModel={selectedModel}></StockChart>
        </div>
        <div>
        <StockOverview stockInfo = {stockInfo} historicalData={historicalData} ></StockOverview>
        </div>
        <div className="row-span-2 xl:row-span-3">
            <StockDetails stockInfo={stockInfo}/>
        </div>
    </div>
    )
}

export default Dashboard