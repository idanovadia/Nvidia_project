



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


async function getMethod(url,jsonObj){
    return await fetch('http://localhost:5000/'+url, {
        mode:'cors',
        method: 'GET',
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


function generate(){
    var url = document.getElementById("origin_url").value;
    var jsonObj = {"url" : url};
    document.getElementById("new_url").value = postMethod(jsonObj,'generate');
}