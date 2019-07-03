import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Error404 extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}
	render() {
		return (
			<div className="center" style={{ textAlign: 'center', marginTop: '-7vmin' }}>
				<h1 style={{ fontSize: '10vmin' }}>404</h1>{' '}
				<p>
					you can head back to the <Link to="/">main menu</Link>
				</p>
			</div>
		);
	}
}

export default Error404;
