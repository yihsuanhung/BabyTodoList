export default function sendReq(url, config){
    fetch(url, config)
        .then(
            response => {
                response.json()
            }
        )
}
