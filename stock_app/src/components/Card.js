
export const Card = ( {children}) =>{
    return(
        //full width of parent
        //full height of parent
        //border radius
        //position
        //padding
        <div className="w-full h-full rounded-md relative p-8 border-2 bg-white border-neutral-300">
            {children}
             </div>
    )
}