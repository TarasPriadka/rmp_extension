import React from 'react';
import ReactDOM from 'react-dom';
import { Button } from 'antd';
import 'antd/dist/antd.css'
import {fetchRequest, parseXML} from '../utils/scraper'

let App = () => {

    let handleClick = () =>{
        let doc = fetchRequest('https://www.ratemyprofessors.com/search.jsp?query=julie+wilson');
       parseXML(doc);
    }

    return <>
        <h1>Rate My Professor Interface</h1>
        <Button onClick={handleClick} type="primary">Analyze Page</Button>
    </>
}

export default App;