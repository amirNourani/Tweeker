import React from "react";
import { apiTweetAction } from "./lookup";


export function ActionBtn(props){
    const {tweet, action, didPerformAction} = props
    const likes = tweet.likes ? tweet.likes : 0
    const className = props.className ? props.className : "btn btn-outline-primary btn-sm text-white"
    const actionDisplay = action.display ? action.display : "Acion"
    
    const handleActionBackendEvent = (response, status) => {
        if ((status === 200 || status === 201) && didPerformAction) {
            didPerformAction(response, status)
        }
        else {
            console.log("something wend wrong with the action")
            console.log(response, status)
        }

    }

    const handleClick = (event) =>{
        event.preventDefault()
        apiTweetAction(tweet.id, action.type, handleActionBackendEvent)  
    }

    const btnLabel = action.type === "like" ? `${likes} ${actionDisplay}` : actionDisplay 
    
    return <button className={className} onClick={handleClick}>{btnLabel}</button>
}
