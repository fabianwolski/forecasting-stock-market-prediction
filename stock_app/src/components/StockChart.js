import React from 'react';
import { Card } from "./Card";
import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
} from "recharts";

const StockChart = ({ historicalData }) => {
    if (!historicalData || historicalData.length < 2) return;
    return (
        <Card>
            <ResponsiveContainer width="100%" height={400}>
                <AreaChart data={historicalData}>
                    <defs>
                        <linearGradient id="colorClose" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#0284C7" stopOpacity={0.8}/>
                            <stop offset="95%" stopColor="#0284C7" stopOpacity={0}/>
                        </linearGradient>
                    </defs>
                    <Area 
                        type="monotone" 
                        dataKey="Close" 
                        stroke="#0284C7" 
                        fill="url(#colorClose)"
                        fillOpacity={1} 
                        strokeWidth={0.5}
                    />
                    <XAxis dataKey="Date" />
                    <YAxis domain={['auto', 'auto']} />
                    <Tooltip 
                        contentStyle={{ 
                            backgroundColor: '#111827',
                            border: '1px solid #374151',
                            borderRadius: '0.375rem'
                        }}
                        itemStyle={{ color: '#0284C7' }}
                        labelStyle={{ color: '#D1D5DB' }}
                    />
                </AreaChart>
            </ResponsiveContainer>
        </Card>
    );
};

export default StockChart;