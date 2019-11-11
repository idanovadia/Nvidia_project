
var localhost_address = "http://localhost:5000/"


async function postMethod(jsonObj,directed_url){
    return await fetch('http://localhost:5000/'+directed_url, {
        mode:'cors',
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonObj),
        }).then(response => {
            return response.json();
        }).then(jsonResponse => {
        return jsonResponse;
        }).catch (error => {
        console.log(error)
        });
}


async function getMethod(){
    return await fetch('http://localhost:5000/'+url, {
        mode:'cors',
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        }).then(response => {
            return response.json();
        }).then(jsonResponse => {
        return jsonResponse;
        }).catch (error => {
        console.log(error)
        });
}


async function generate(){
    var url = document.getElementById("origin_url").value;
    var jsonObj = {"url" : url};
    var json_url_response = await postMethod(jsonObj,'generate');
    document.getElementById("new_url").value = localhost_address+json_url_response.url
}