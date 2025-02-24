import { Card } from "./Card";

const StockDetails = ({stockInfo}) =>{
    if(!stockInfo) return null

    const detailsList = {
        "Name": stockInfo.longName,
        "Country": stockInfo.country,
        "Sector": stockInfo.sector,
        "Market Capitalization" : stockInfo.marketCap,
        "Number Of Analyst Opinions": stockInfo.numberOfAnalystOpinions,
        "Recommendation": stockInfo.recommendationKey,
    }

    const convertMillToBill = (number) =>{
        return (number / 1000000000).toFixed(2); 
    }

    return(
        <Card>
            <ul className="w-full h-full flex flex-col justify-between divide-y-1">
                {Object.entries(detailsList).map(([key, value]) => (
                     <li key={key} className="flex-1 flex justify-between items-center">
                        <span>{key}</span>
                        <span>{key === "Market Capitalization" ? `${convertMillToBill(value)}B` : value}</span>
                    </li>
                ))}
            </ul>
        </Card>
    )
}

export default StockDetails