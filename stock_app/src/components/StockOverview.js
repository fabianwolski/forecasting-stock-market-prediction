import React, { useState, useEffect } from 'react';
import { Card } from "./Card";

const StockOverview = ({ stockInfo, historicalData }) => {
    const [change, setChange] = useState({ value: 0, percentage: 0 });
    
    useEffect(() => {
        if (!historicalData || historicalData.length < 2) return;

        const sortedData = [...historicalData].sort((a, b) => 
            new Date(a.Date) - new Date(b.Date)
        );
        
        //first and last closing price
        const firstClose = sortedData[0].Close;
        const lastClose = sortedData[sortedData.length - 1].Close;
        
        const absoluteChange = lastClose - firstClose;
        const percentageChange = ((lastClose - firstClose) / firstClose) * 100;
        
        setChange({
            value: absoluteChange.toFixed(2),
            percentage: percentageChange.toFixed(2)
        });
    }, [historicalData]);

    if (!stockInfo || !historicalData) return null;

    const price = stockInfo.currentPrice;
    const isPositive = change.value > 0;

    return (
        <Card>
            <div className="h-full w-full flex items-center justify-around">
                <span className="xl:text-4xl text-2xl 2xl:text-5xl flex items-center gap-1">
                    {price?.toFixed(2)}
                    <span className='text-lg xl:text-xl 2xl:text-2xl text-netural-400'>USD</span>
                </span>
                <div className="flex items-center gap-1">
                    <span className={`text-lg xl:text-xl 2xl:text-2xl ${isPositive ? "text-lime-500" : "text-red-500"}`}>
                        {isPositive ? "+" : ""}${change.value}
                    </span>
                    <span className={`text-sm xl:text-base 2xl:text-lg ${isPositive ? "text-lime-500" : "text-red-500"}`}>
                        ({isPositive ? "+" : ""}{change.percentage}%)
                    </span>
                </div>
            </div>
        </Card>
    );
};

export default StockOverview;