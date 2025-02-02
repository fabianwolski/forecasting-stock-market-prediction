import Dashboard  from './components/Dashboard';
import { StockProvider } from './contexts/StockContext';
import StockSearchForm from './components/StockSearchForm';
function App() {
    return (
    <StockProvider>
    <div>
    <Dashboard/>
    </div>
    </StockProvider>
);
}

export default App;