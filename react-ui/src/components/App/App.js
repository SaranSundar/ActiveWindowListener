import React, {Fragment} from 'react';
import './App.css';
import {Route, Switch} from "react-router-dom";
import WebSocketExample from "../WebSocketExample/WebSocketExample";
import NoMatch from "../NoMatch/NoMatch";
import CssBaseline from "@material-ui/core/CssBaseline";
import Home from "../Home/Home";
import ChartPage from "../ChartPage/ChartPage";

function App() {
    return (
        <Fragment>
            <CssBaseline/>
            <div className="App">
                {/*<NavBar/>*/}
                <Switch>
                    <Route exact path="/" component={ChartPage}/>
                    <Route exact path="/home" component={Home}/>
                    <Route exact path="/example" component={WebSocketExample}/>
                    <Route component={NoMatch}/>
                </Switch>
            </div>
        </Fragment>
    );
}

export default App;
