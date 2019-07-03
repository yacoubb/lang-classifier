import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Main from './main';
import App from './app';
import Error404 from './404';

class Home extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}
	render() {
		return (
			<Router>
				<Switch>
					<Route path="/" exact={true}>
						<Main />
					</Route>
					<Route path="/app" exact={true}>
						<App />
					</Route>
					<Route path="/" exact={false}>
						<Error404 />
					</Route>
				</Switch>
			</Router>
		);
	}
}

export default Home;
