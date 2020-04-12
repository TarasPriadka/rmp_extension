// Example POST method implementation:
export async function postData(url = '', data) {
    // Default options are marked with *
    const headers = new Headers();
    headers.append('Access-Control-Allow-Origin', '*');
    
    fetch(url,{
        method: 'POST',
        mode: 'no-cors',
        body:data
    }).then(r=>{console.log(r);});

    // const response = await fetch(url, {
    //     method: 'POST', // *GET, POST, PUT, DELETE, etc.
    //     mode: 'no-cors', // no-cors, *cors, same-origin
    //     // cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    //     // credentials: 'same-origin', // include, *same-origin, omit
    //     // headers: {
    //     //     // 'Content-Type': 'application/json'
    //         // 'Access-Control-Allow-Origin': '*'
    //     //     // 'Content-Type': 'application/x-www-form-urlencoded',
    //     // },
    //     // redirect: 'follow', // manual, *follow, error
    //     // referrerPolicy: 'no-referrer', // no-referrer, *client
    //     body: data // body data type must match "Content-Type" header
    // });
    return await response; // parses JSON response into native JavaScript objects
}