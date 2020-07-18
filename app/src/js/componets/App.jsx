import React, { useState, useEffect } from 'react';

import { Button } from 'antd';


import { DynamicFields } from './DynamicField.jsx'
import { getElementXPath } from '../utils/utils'


import 'antd/dist/antd.css'
import '../../css/main.css'

let App = () => {

    const [received, setReceived] = useState('nothin');
    const [selectingXpath, setSelectingXpath] = useState(0);
    const [xpath, setXpath] = useState('');
    // const [detectionMode, setDetectionMode] = useState(false);

    useEffect(()=>{
        if (xpath){
            console.log(xpath)
            let xpath_elem = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (!xpath_elem.className.includes('app-element')){
                xpath_elem.setAttribute("style", "border-style: solid; border-color: red;"); 
            }
        }
    },[xpath])

    let clear_attributes = () => {
        if (xpath) {
            let xpath_elem = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (!xpath_elem.className.includes('app-element')) {
                xpath_elem.setAttribute("style", "border-style: none;");
            }
            setXpath('')
        }
    }

    let handleSubmit = (teachers) => {
        const formData = new FormData();
        formData.append('names', teachers.join(','));

        let url = 'http://127.0.0.1:5000/scrape';

        fetch(url, {
            method: 'POST',
            headers: {
                'Access-Control-Allow-Origin': '*'
            },
            // mode: 'no-cors',
            body: formData
        }).then(r => r.json())
            .catch(error => console.log(error))
            .then(d => {
                let data = d.data;
                // console.log(data);
                // console.log(teachers);
                teachers.map((t) => {
                    console.log(t, data[t][0]);
                })
                setReceived('Gotit');
            });

    }


    window.onclick = e => {
        if (selectingXpath === 2) {
            console.log('Clicked in window')
            if (e.target.tagName !== 'html') {
                let t_xpath = getElementXPath(e.target);
                setXpath(t_xpath);
           } else {
                setXpath('');
            }
            setSelectingXpath(false)
        } else if (selectingXpath === 1) {
            setSelectingXpath(2)
        }
    }

    return <>
        <h1 className='title app-element'>Rate My Professor Interface</h1>
        <DynamicFields className='app-element' handleClick={handleSubmit} />
        <hr />
        <Button className="app-element" onClick={() => { setSelectingXpath(1) }}>Start Table Detection</Button>
        <Button className="app-element" onClick={() => { clear_attributes() }}>Clear</Button>
    </>
}

export default App;