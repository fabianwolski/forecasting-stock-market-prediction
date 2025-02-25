import React from 'react';
import { Card } from "./Card";
import InfoTooltip from './InfoToolTip';
import ModelInfo from './ModelInfo';
import {
    ComposedChart,
    Area,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    Line,
    Legend
} from "recharts";

const SERIES_COLORS = {
    "Actual Price": "#0284C7",
    "Training Predictions": "#4ADE80",
    "Test Predictions": "#FFFF00"
}

const StockChart = ({ historicalData, predictionResults, selectedModel }) => {
    if (!historicalData || historicalData.length < 2) return;
    // console.log("Full prediction results:", predictionResults);
    // console.log("Train predictions structure:", predictionResults?.train);
    // console.log("Test predictions structure:", predictionResults?.test);
    const trainPredictions = predictionResults?.train?.predictions || [];
    const testPredictions = predictionResults?.test?.predictions || [];

    const getSeriesColor = () => SERIES_COLORS || "#D1D5DB";

    return (
        <Card>
            <ResponsiveContainer width="100%" height={400}>
                <ComposedChart>
                    <defs>
                        <linearGradient id="colorClose" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#0284C7" stopOpacity={0.8}/>
                            <stop offset="95%" stopColor="#0284C7" stopOpacity={0}/>
                        </linearGradient>
                    </defs>
                    
                    <Area 
                        data={historicalData}
                        type="monotone" 
                        dataKey="Close" 
                        stroke="#0284C7" 
                        fill="url(#colorClose)"
                        fillOpacity={1} 
                        strokeWidth={0.5}
                        name="Actual Price"
                        xAxisId="date"
                    />

                    <Line
                        data={trainPredictions}
                        type="monotone"
                        dataKey="Prediction"
                        stroke="#4ADE80"
                        strokeDasharray="5 5"
                        dot={false}
                        name="Training Predictions"
                        xAxisId="date"
                    />

                    <Line
                        data={testPredictions}
                        type="monotone"
                        dataKey="Prediction"
                        stroke="#FFFF00"
                        strokeWidth={2}
                        dot={false}
                        name="Test Predictions"
                        xAxisId="date"
                    />

                    <XAxis 
                        dataKey="Date" 
                        xAxisId="date"
                        type="category"
                        allowDuplicatedCategory={false}
                    />
                    <YAxis domain={['auto', 'auto']} />
                    <Tooltip 
                        contentStyle={{ 
                            backgroundColor: '#111827',
                            border: '1px solid #374151',
                            borderRadius: '0.375rem'
                        }}
                        itemStyle={({ name }) => ({ 
                            color: getSeriesColor(name) 
                        })}
                        labelStyle={{ color: '#D1D5DB' }}
                        cursor={{ stroke: '#374151' }}
                    />
                    <Legend />
                </ComposedChart>
            </ResponsiveContainer>

            <div className="mt-4 grid grid-cols-2 gap-4">
                <div>
                    <div className="flex items-center">
                        <h3 className="font-medium text-gray-200">Training Metrics</h3>
                        <InfoTooltip content="Shows how well the model fits the historical training data. Lower RMSE and MAPE values indicate better performance. Higher R²(closer to 100%) indicates a better fit." />
                    </div>
                    <div className="text-sm text-gray-400">
                        <p className="flex items-center">
                            RMSE: {predictionResults?.train?.metrics?.rmse.toFixed(2)}
                        </p>
                        <p className="flex items-center">
                            R²: {(predictionResults?.train?.metrics?.r2 * 100).toFixed(2)}%
                        </p>
                        <p className="flex items-center">
                            MAPE: {predictionResults?.train?.metrics?.mape.toFixed(2)}%
                        </p>
                    </div>
                </div>
                <div>
                    <div className="flex items-center">
                        <h3 className="font-medium text-gray-200">Test Metrics</h3>
                        <InfoTooltip content="Shows how well the model predicts new, unseen data. Major factor in identifying true predictive performance." />
                    </div>
                    <div className="text-sm text-gray-400">
                        <p className="flex items-center">
                            RMSE: {predictionResults?.test?.metrics?.rmse.toFixed(2)}
                            <InfoTooltip content="Root Mean Square Error - measures the average magnitude of errors made by prediction (lower is better)" />
                        </p>
                        <p className="flex items-center">
                            R²: {(predictionResults?.test?.metrics?.r2 * 100).toFixed(2)}%
                            <InfoTooltip content="R-squared - indicates how well the model explains the variance in data (higher is better, max 100%)" />
                        </p>
                        <p className="flex items-center">
                            MAPE: {predictionResults?.test?.metrics?.mape.toFixed(2)}%
                            <InfoTooltip content="Mean Absolute Percentage Error - average percentage difference between predicted and actual values (lower is better)" />
                        </p>
                    </div>
                </div>
            </div>

            <div className="mt-2">
                <ModelInfo selectedModel={selectedModel} />
            </div>
        </Card>
    );
};

export default StockChart;