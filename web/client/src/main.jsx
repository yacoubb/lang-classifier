import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Main extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}
	render() {
		return (
			<div className="centerHoriz" style={{ marginTop: '25vh', width: '50%', textAlign: 'justify' }}>
				<h1>Predicting Languages Using Neural Networks</h1>
				<p>
					After watching carykh's video on attempting to predict the language of a word using a neural network
					it inspired me to finally have a stab at doing some machine learning myself. This is my
					implementation of the same thing, a machine learning algorithm that attempts to guess the language
					of origin of a word given just the word itself. You can check out the result{' '}
					<Link to="app">here</Link>.
					<br />A You can find cary's video <a href="https://www.youtube.com/watch?v=evTx5BoKcc8">here</a>.
					<br />
				</p>
				{/* <h2>The Algorithm</h2> */}
				{/* Datasets <br />I got a large language */}
			</div>
		);
	}
}

export default Main;
