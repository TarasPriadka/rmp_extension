import React from 'react';

import { Form, Input, Button } from 'antd';
import { DynamicFields } from './DynamicField.jsx'

// import {postData} from '../utils/utils'

import 'antd/dist/antd.css'
import '../../css/main.css'

let App = () => {

    let handleClick = (teachers) =>{
        const formData = new FormData();
        // const teachers = ['Manish Goel', 'Delia Garbacea'];
        formData.append('names',teachers.join(','));

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
        .then(data=>console.log(data));

        // let doc = postData('http://127.0.0.1:5000/scrape', formData);
        // console.log(doc);

    }

    return <>
        <h1 className='title'>Rate My Professor Interface</h1>
        <DynamicFields handleClick={handleClick}/>

    </>
}

export default App;