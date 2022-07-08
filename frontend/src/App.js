import React from "react";
import Home from './components/Home'
import Details from './components/Details'
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom'
import Login from "./components/Login";
function App() {

  

  return (
    <Router>
      <div className="App">
        <Switch>
          {/* <Route path="/login" component={Login} /> */}
          <Route path="/" exact component={Home} />
          <Route path="/details/:finn_code" component={Details} />
          
        </Switch>

      </div>
    </Router>
  );
}

export default App;
