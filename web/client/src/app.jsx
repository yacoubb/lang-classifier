import React, { Component } from 'react';
import * as tf from '@tensorflow/tfjs';

var xhr;
var model;
var alphabet = '';
var alphabet_vectors = {};
var zeroVec = [];

class App extends Component {
	constructor(props) {
		super(props);
		this.state = { model: 'loading', metadata: 'loading', word: [], predictedLanguage: '' };
		this.keyPressHandler.bind(this);
		this.vectorize_word.bind(this);
		xhr = new XMLHttpRequest();
		var url = 'http://localhost:3003/metadata';
		xhr.open('GET', url, true);
		xhr.send();

		model = tf.loadLayersModel('http://localhost:3003/model');
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
				console.log(xhr.responseText);
				var jsonData = JSON.parse(xhr.responseText);
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
		if (newWord.length > 0) {
			this.predict();
		} else {
			this.setState({ predictedLanguage: '' });
		}
	};

	vectorize_word(wordArr) {
		var parsedWord = [];
		for (const idx in wordArr) {
			if (Object.keys(alphabet_vectors).indexOf(wordArr[idx]) === -1) {
				parsedWord.push(zeroVec);
				continue;
			}
			parsedWord.push(alphabet_vectors[wordArr[idx]]);
		}
		const zeroVecsToAdd = this.state.metadata.maxWordLength - parsedWord.length;
		for (let i = 0; i < zeroVecsToAdd; i++) {
			parsedWord.push(zeroVec);
		}
		// return tf.tensor(parsedWord, (null, 520));
		return tf.tensor3d([parsedWord]);
	}

	predict = () => {
		let vec_word = this.vectorize_word(this.state.word);
		const prediction = this.state.model.predict(vec_word);
		const tList = this.tensorToList(prediction);
		this.setState({ predictedLanguage: this.state.metadata.languages[this.argMax(tList)] });
	};

	tensorToList(tensor) {
		const tStr = tensor.toString();
		const tList = tStr
			.split('[')[2]
			.split(']')[0]
			.split(', ');

		return tList.map((v, i) => parseFloat(v));
	}

	argMax(array) {
		return array.map((x, i) => [x, i]).reduce((r, a) => (a[0] > r[0] ? a : r))[1];
	}

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
					<div className="centerHoriz" style={{ paddingTop: '10vh', textAlign: 'center' }}>
						{letterSpaces.map((value, index) => (
							<div key={index} style={{ float: 'left', margin: '0.5em' }}>
								<h1>{value}</h1>
							</div>
						))}
					</div>
					<div className="centerHoriz" style={{ paddingTop: '10%' }}>
						<h1>{this.state.predictedLanguage}</h1>
					</div>
				</div>
			);
		}
	}
}

export default App;
