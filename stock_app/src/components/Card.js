
export const Card = ( {children}) =>{
    return(
        //full width of parent
        //full height of parent
        //border radius
        //position
        //padding
        <div className="w-full h-full rounded-md relative p-8 bg-gray-900 border-gray-800">
            {children}
             </div>
    )
}