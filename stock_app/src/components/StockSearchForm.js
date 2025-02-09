import React, { useState } from 'react'
import { useStock } from '../contexts/StockContext';
import { BsSearch} from "react-icons/bs";
import { Card } from './Card';

const MODEL_OPTIONS = [
    {value: "regression", label: "Linear Regression"},
    {value: "lstm", label: "LSTM"},
    {value: "prophet", label: "Prophet"},
    {value: "arima", label: "ARIMA"}
];

function StockSearchForm() {
    const [selectedModel, setSelectedModel] = useState('');
    const {stockData, updateStockData, setLoading, setError} = useStock()

    const handleSubmit = async (event) => {
        event.preventDefault()
        const formData =  new FormData(event.target);
        const ticker = formData.get('ticker');
        //DD-MM-YYYY to YYYY-MM-DD
        const startDate = formData.get('startDate').split('-').reverse().join('-'); 
        const endDate = formData.get('endDate').split('-').reverse().join('-');     
        //TO:DO ADD array for models since we are directly doing it (Not best practise)
    try{
        setLoading(true)
        const response = await fetch('http://localhost:5000/stock', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ ticker, start: startDate, end: endDate,  model_type: selectedModel})
        });
        const data = await response.json();  //api returns json so .json needed 
            
        if (data.success) {
            alert(`Success: ${data.message}`);
            updateStockData(data)
            console.log('Stock Data:', data);
        } else {
            alert(`Error: ${data.error}`);
            setError(data.error)
        }
        }catch(error){
            alert('Error: ', error)
            setError(error.message)
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit} className="p-4 bg-gray-900 border border-gray-800 rounded-lg">
                <input 
                    name="ticker" 
                    placeholder="Ticker (example: AAPL)" 
                    className="mx-4 p-2 bg-gray-800 text-gray-300 border border-gray-700 rounded-md placeholder-gray-500 focus:outline-none focus:border-sky-600" 
                    required 
                    autoComplete="off"
                />
                <input 
                    name="startDate" 
                    placeholder="Start DD-MM-YYYY" 
                    className="mx-2 p-2 bg-gray-800 text-gray-300 border border-gray-700 rounded-md placeholder-gray-500 focus:outline-none focus:border-sky-600" 
                    required 
                    autoComplete="off"
                />
                <input 
                    name="endDate" 
                    placeholder="End DD-MM-YYYY" 
                    className="p-2 bg-gray-800 text-gray-300 border border-gray-700 rounded-md placeholder-gray-500 focus:outline-none focus:border-sky-600" 
                    required  
                    autoComplete="off"
                />
                <select 
                    value={selectedModel} 
                    onChange={(e) => setSelectedModel(e.target.value)}
                    name="modelType"
                    className="mx-4 p-2 bg-gray-800 text-gray-300 border border-gray-700 rounded-md focus:outline-none focus:border-sky-600"
                >
                    <option value="" className="bg-gray-800">Select Model</option>
                    {MODEL_OPTIONS.map(option => (
                        <option 
                            key={option.value} 
                            value={option.value}
                            className="bg-gray-800"
                        >
                            {option.label}
                        </option>
                    ))}
                </select>
                <button 
                    type="submit" 
                    disabled={stockData?.loading}
                    className="bg-sky-600 hover:bg-sky-700 rounded-md p-2 transition-colors duration-200"
                > 
                    <BsSearch className="h-4 w-4 text-gray-100" />
                </button>
            </form>
        </div>
    );
}

export default StockSearchForm