import React, { Component, Fragment } from 'react';
import ReactDom from "react-dom";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import Form from './Form';
import Medicine from './Medicine';
import FormUpdate from './FormUpdate';



export class ManageMedicine extends Component {
    render() {
        return (

                <Fragment>
                    <div className="row">
                        
                        <div className="col-lg-6">

                            <Form/>

                        </div>
                        
                        <div className="col-lg-6">
                            
                            <FormUpdate/>
                        </div>                    
                        
                    </div>
                    <div className="row">
                        <div className="col-lg-12">
                            <Medicine/>
                        </div>    
                    </div>
                </Fragment>

            

                
                
        )
    }
}

export default ManageMedicine;
