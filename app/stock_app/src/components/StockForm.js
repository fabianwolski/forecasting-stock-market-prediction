import React, { useState } from 'react'

function StockForm() {
    const handleSubmit = async (event) => {
        event.preventDefault()
        const formData =  new FormData(event.target);
        const ticker = formData.get('ticker');
        //DD-MM-YYYY to YYYY-MM-DD
        const startDate = formData.get('startDate').split('-').reverse().join('-'); 
        const endDate = formData.get('endDate').split('-').reverse().join('-');     

    try{
        const response = await fetch('http://localhost:5000/stock', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ ticker, start: startDate, end: endDate })
        });
        const data = await response.json();  //api returns json so .json needed
            if (data.success) {
                alert(`Success: ${data.message}`);
                console.log('Data:', data);
            } else {
                alert(`Error: ${data.error}`);
            }
    }catch(error){
        alert('Error: ', error)
    }
    };

    return(
        <form onSubmit={handleSubmit}>
        <input name="ticker" placeholder="Ticker (example: AAPL)" required />
        <input name="startDate" placeholder="Start DD-MM-YYYY" required />
        <input name="endDate" placeholder="End DD-MM-YYYY" required />
        <button type="submit">Submit</button>
    </form>
    );
}

export default StockForm