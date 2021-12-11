import React, { Component } from 'react';
import ReactDom from "react-dom";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

export class Header extends Component {
    render() {
        return (
            <nav className="navbar navbar-expand-sm green-background">
              <Link to="/" className="navbar-brand mx-auto white white-hover w-100 text-center"><img src={'images/old-man.svg' } style={{height:"50px"}}/> Elderly Assistance System</Link>
              <button className="navbar-toggler white d-none" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
                <img src={'images/menu.svg' } style={{height:"30px"}}/>
              </button>
              <div className="collapse navbar-collapse" id="navbarTogglerDemo01">
                
                

              </div>


            </nav>
        )
    }
}

export default Header
