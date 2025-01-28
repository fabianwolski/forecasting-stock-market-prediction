import React, { useState } from 'react'

function StockForm() {
    const [predictionResults, setPredictionResults] = useState(null);
    const [selectedModel, setSelectedModel] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault()
        const formData =  new FormData(event.target);
        const ticker = formData.get('ticker');
        //DD-MM-YYYY to YYYY-MM-DD
        const startDate = formData.get('startDate').split('-').reverse().join('-'); 
        const endDate = formData.get('endDate').split('-').reverse().join('-');     
        //TO:DO ADD array for models since we are directly doing it (Not best practise)
    try{
        const response = await fetch('http://localhost:5000/stock', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ ticker, start: startDate, end: endDate,  model_type: selectedModel})
        });
        const data = await response.json();  //api returns json so .json needed 
            if (data.success) {
                alert(`Success: ${data.message}`);
                console.log('Stock Data:', data.data);
                if (data.predictions) {
                    console.log('Prediction Metrics:', data.predictions);
                    setPredictionResults(data.predictions);
                }
            } else {
                alert(`Error: ${data.error}`);
            }
    }catch(error){
        alert('Error: ', error)
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
                    <option value="regression">Linear Regression</option>
                    <option value="lstm">LSTM</option>
                    {/*<option value="prophet">Prophet</option>*/}
                    {/*<option value="arima">ARIMA</option>*/}
                </select>
                <button type="submit">Predict</button>
            </form>

            {predictionResults && (
                <div>
                    <h3>Prediction Results:</h3>
                    <pre>{JSON.stringify(predictionResults, null, 2)}</pre>
                </div>
            )}
        </div>
    );
}

export default StockForm