import React from "react";
import { apiTweetCreate } from "./lookup";

export function TweetCreate(props){
    const textAreaRef = React.createRef()
    const {didTweet} = props

    const handleBackendUpdate = (response, status) => {
        if (status === 201){
            didTweet(response)
        } else {
            alert(response.content)
        }
    }

    const handleSubmit = (event) => {
        event.preventDefault()
        const tweetContent = textAreaRef.current.value
        // backend api request
        apiTweetCreate(tweetContent, handleBackendUpdate)
        textAreaRef.current.value = ""
    }
    
    return <div className={props.className}>
                <form onSubmit={handleSubmit}>
                <textarea ref={textAreaRef} required={true} className="form-control" name="tweet" placeholder="What's happening...?"></textarea>
                <button type="submit" className="btn btn-outline-primary text-white my-3 px-3">Tweet</button>
                </form>
            </div>
}
