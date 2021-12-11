import React, { Fragment } from 'react';
import ReactDom from "react-dom";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";





export default function Dashboard() {
    return (

            <Fragment>
                <div className="row">
                    
                    <div className="col-lg-6">
                        <Link to="/manage-medicine">
                            <div className="homepage-tile vertically-middle text-center horizontal-middle-flex round-border-all red-background">
                                <div>
                                    <img className="homepage-title-icon" src="images/manage.svg"></img>
                                    <h2 className="white text-center w-100">Manage Medicine</h2>
                                </div>
                            </div>
                        </Link>
                    </div>
                    
                    <div className="col-lg-6">
                        <Link to="/medicine-history">
                            <div className="homepage-tile vertically-middle text-center horizontal-middle-flex round-border-all red-background">
                                <div>
                                    <img className="homepage-title-icon" src="images/history.svg"></img>
                                    <h2 className="white text-center w-100">View Medicine Records</h2>
                                </div>
                                
                                
                            </div>
                        </Link>
                    </div>                    
                    
                </div>

            </Fragment>

        

            
            

    )
}
