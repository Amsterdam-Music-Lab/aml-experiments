import React from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Redirect
} from "react-router-dom";
import { URLS, EXPERIMENT_SLUG } from "../../config";
import Experiment from "../Experiment/Experiment";
import Profile from "../Profile/Profile";
import Reload from "../Reload/Reload";
import StoreProfile from "../StoreProfile/StoreProfile.js";

// App is the root component of our application
const App = () => {
    return (
        <Router className="aha__app">
            <Switch>
                {/* Request reload for given participant */}
                <Route path={URLS.reloadParticipant}>
                    <Reload/>
                </Route>

                {/* Default experiment */}
                <Route path="/" exact>
                    <Redirect
                        to={URLS.experiment.replace(":slug", EXPERIMENT_SLUG)}
                    />
                </Route>
                
                {/* Profile */}
                <Route path={URLS.profile} exact>
                    <Profile slug={EXPERIMENT_SLUG} />
                </Route>

                {/* Experiment */}
                <Route path={URLS.experiment} component={Experiment} />

                <Route path={URLS.session} />

                {/* Store profile */}
                <Route
                    path={URLS.storeProfile}
                    exact
                    component={StoreProfile}
                />


            </Switch>
        </Router>
    );
};

export default App;
