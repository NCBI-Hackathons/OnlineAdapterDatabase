import React from 'react';
import { Router, Route } from 'react-router';
import { createBrowserHistory } from 'history';
import $ from 'jquery';

const history = createBrowserHistory();

/* This jquery turns the absolute navigation actions into browser history actions */
$('.react-nav a').click(function(ev) {
    ev.stopPropagation();
    history.push(this.getAttribute('href'), null);
});

class KitList extends React.Component {
    render() {
        return <h3>List of kits</h3>
    }
}

class AdapterList extends React.Component {
    render() {
        return <h3>List of adapters</h3>
    }
}

class RunList extends React.Component {
    render() {
        return <h3>List of runs</h3>
    }
}

class App extends React.Component {
    render() {
        return (
            <Router history={history}>
                <div>
                    <Route path='/admin/kit' component={KitList} />
                    <Route path='/admin/adapter' component={AdapterList} />
                    <Route path='/admin/run' component={RunList} />
                </div>
            </Router>
        )
    };
}

export default App;
