import React, { Component } from 'react';
import * as tf from '@tensorflow/tfjs';

var xhr = new XMLHttpRequest();
var url = 'http://localhost:3003/metadata';
xhr.open('GET', url, true);
xhr.send();

const model = tf.loadLayersModel('http://localhost:3003/model');
var alphabet = '';
var alphabet_vectors = {};
var zeroVec = [];

class App extends Component {
	constructor(props) {
		super(props);
		this.state = { model: 'loading', metadata: 'loading', word: [] };
		this.keyPressHandler.bind(this);
		this.vectorize_word.bind(this);
		model
			.then(value => {
				this.setState({ model: value });
				console.log(value);
			})
			.catch(reason => {
				this.setState({ model: 'failed' });
				console.error(reason);
			});
		xhr.onreadystatechange = () => {
			if (xhr.readyState === 4 && xhr.status === 200) {
				var jsonData = JSON.parse(xhr.responseText);
				jsonData = JSON.parse(jsonData);
				this.setState({ metadata: jsonData });
				alphabet_vectors = {};
				alphabet = jsonData.alphabet;
				for (let i = 0; i < alphabet.length; i++) {
					let vec = [];
					for (let j = 0; j < alphabet.length; j++) {
						vec.push(0);
					}
					vec[i] = 1;
					alphabet_vectors[alphabet.charAt(i)] = vec;
				}

				zeroVec = [];
				for (let i = 0; i < alphabet.length; i++) {
					zeroVec.push(0);
				}
				console.log(jsonData);
			}
		};
	}

	componentDidMount() {
		document.addEventListener('keydown', this.keyPressHandler, false);
	}
	componentWillUnmount() {
		document.removeEventListener('keydown', this.keyPressHandler, false);
	}

	keyPressHandler = event => {
		let newWord = this.state.word;
		if (event.key === 'Backspace') {
			newWord.pop();
		} else if ((event.keyCode >= 65 && event.keyCode <= 90) || (event.keyCode >= 97 && event.keyCode <= 122)) {
			newWord.push(event.key);
		}
		newWord = newWord.slice(0, this.state.metadata.maxWordLength);
		this.setState({ word: newWord });
		this.predict();
	};

	vectorize_word(wordArr) {
		var parsedWord = [];
		for (const idx in wordArr) {
			if (Object.keys(alphabet_vectors).indexOf(wordArr[idx]) === -1) {
				parsedWord.push(zeroVec);
			}
			parsedWord = parsedWord.push(alphabet_vectors[wordArr[idx]]);
		}
		const zeroVecsToAdd = this.state.metadata.maxWordLength - parsedWord.length;
		for (let i = 0; i < zeroVecsToAdd; i++) {
			parsedWord.push(zeroVec);
		}
		// return tf.tensor(parsedWord, (null, 520));
		return tf.tensor2d(parsedWord);
	}

	predict = () => {
		let vec_word = this.vectorize_word(this.state.word);
		// vec_word = tf.reshape(vec_word, [null, 520]);
		console.log(this.state.model.predict(vec_word));
	};

	render() {
		if (this.state.model === 'loading' || this.state.metadata === 'loading') {
			return (
				<div className="center">
					<h1>Loading...</h1>
				</div>
			);
		} else if (this.state.model === 'failed' || this.state.metadata === 'failed') {
			return (
				<div className="center">
					<h1>Loading model failed! Reload the page to try again</h1>
				</div>
			);
		} else {
			console.log(this.state);
			const letterSpaces = [];
			for (let i = 0; i < this.state.metadata.maxWordLength; i++) {
				if (i < this.state.word.length) {
					letterSpaces.push(this.state.word[i]);
				} else {
					letterSpaces.push('_');
				}
			}
			return (
				<div style={{ width: '100%' }}>
					<div style={{ textAlign: 'center' }}>
						<p>LOADED MODEL MATE</p>
					</div>
					<div style={{ textAlign: 'center' }}>
						{letterSpaces.map((value, index) => (
							<div key={index} style={{ float: 'left', margin: '0.5em' }}>
								<h1>{value}</h1>
							</div>
						))}
					</div>
				</div>
			);
		}
	}
}

export default App;
