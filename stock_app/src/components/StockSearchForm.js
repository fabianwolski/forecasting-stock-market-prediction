import React, { useState } from 'react'
import { useStock } from '../contexts/StockContext';

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

    return(
            <div>
            <form onSubmit={handleSubmit}>
                <input name="ticker" placeholder="Ticker (example: AAPL)" required />
                <input name="startDate" placeholder="Start DD-MM-YYYY" required />
                <input name="endDate" placeholder="End DD-MM-YYYY" required />
                <select 
                    value={selectedModel} 
                    onChange={(e) => setSelectedModel(e.target.value)}
                    name="modelType"
                >
                   <option value="">Select Model</option>
                   {MODEL_OPTIONS.map(option =>(
                    <option key={option.value} value={option.value}>        
                        {option.label}
                    </option>
                   ))}
                </select>
                <button type="submit" disabled={stockData?.oading}> 
                    {stockData?.loading ? 'Loading...' : 'Predict'}
                    </button>
            </form>
        </div>
    );
}

export default StockSearchForm