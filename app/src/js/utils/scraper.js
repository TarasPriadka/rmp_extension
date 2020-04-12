
export function fetchRequest(theUrl) {
    
    let xmlhttp = null;

    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    }

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            console.log(xmlhttp);
            return xmlhttp;
        }
    }

    xmlhttp.open("GET", theUrl, false);
    xmlhttp.send();
    return xmlhttp;
}


export function parseXML(xml){
    let parser = new DOMParser();
    var doc = parser.parseFromString(xml.responseText, "text/html");
    let result = doc.evaluate("//body//ul[contains(@class,'listing')]//@href", doc, null, XPathResult.STRING_TYPE, null);
    console.log(result);
}

