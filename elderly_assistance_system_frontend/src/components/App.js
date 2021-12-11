import React, { Component, Fragment } from "react";
import ReactDom from "react-dom";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import {Provider as AlertProvider } from 'react-alert';
import AlertTemplate from 'react-alert-template-basic';

import Header from "./layout/Header";
import Dashboard from "./medicineModule/Dashboard";
import Alerts from "./layout/Alerts";
import ManageMedicine from './medicineModule/medicine/ManageMedicine';
import MedicineHistory from './medicineModule/medicineHistory/MedicineHistory';


import { Provider } from "react-redux";
import store from "../store";

// Alert Options
const alertOptions = {
  timeout: 3000,
  position: 'top center'
}

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <AlertProvider template={AlertTemplate} {...alertOptions}>
          <Router>
          <Fragment>
            <Header />
            <Alerts />
              
              <div className="container py-5">
                <Switch>
                  <Route exact path="/" component={Dashboard}/>
                  
                  <Route exact path="/manage-medicine">
                    <ManageMedicine/>
                  </Route>
                  <Route exact path="/medicine-history">

                    <MedicineHistory/>
                  </Route>
                </Switch>
              </div>
              
            
          </Fragment>
          </Router>
        </AlertProvider>
      </Provider>
    );
  }
}

ReactDom.render(<Router><App /></Router>, document.getElementById("app"));
