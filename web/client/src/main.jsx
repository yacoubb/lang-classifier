import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Main extends Component {
	constructor(props) {
		super(props);
		this.state = {};
	}
	render() {
		return (
			<div
				className="centerHoriz"
				style={{ marginTop: '5vh', paddingBottom: '10vh', width: '70%', textAlign: 'justify' }}
			>
				<h1>Predicting Languages Using Neural Networks</h1>
				<p>
					After watching carykh's <a href="https://www.youtube.com/watch?v=evTx5BoKcc8">video</a> on
					attempting to predict the language of a word using a neural network it inspired me to finally have a
					stab at doing some machine learning myself. This is my implementation of the same thing, a machine
					learning algorithm that attempts to guess the language of origin of a word given just the word
					itself.
					<br />
					You can check out the result <Link to="app">here</Link> and the sourcecode{' '}
					<a href="https://github.com/yacoubb/lang-classifier">here</a>.
					<br />
				</p>
				<h2>The Algorithm</h2>
				<p>
					Text training data is encoded using a series of one-hot vectors limited to just the roman alphabet
					i.e. "abc...". So the vector representation of "ab" would be [[1000...], [0100...]]. Special
					characters from other languages are dealt with in a number of ways. Several diacritics (å, ö etc)
					are translated using a dictionary written by hand that attempts to represent those letters
					phonteically. For example the Swedish ä is read ae, so in the diacritic translation dict would be a
					key-value pair that looks something like "ä":"ae". Diacritics that are not handled are simply
					stripped, so super uncommon ones like ł just become l. Chinese characters also had to be romanised,
					and luckily there is a standard that already exists for this called{' '}
					<a href="https://en.wikipedia.org/wiki/Pinyin">pinyn</a>. And it gets better, there already exists a{' '}
					<a href="https://pypi.org/project/pinyin/">python library</a> that supports full
					chinese-character-to-pinyin translation.
					<br />
					<br />
					Now that I had a transliteration method set up I had to find a dataset.{' '}
					<a href="https://www.kaggle.com">Kaggle</a> is an excellent resource for machine learning datasets
					and on there I found <a href="https://www.kaggle.com/alvations/old-newspapers">this</a> large text
					corpus that contained data in 67 different languages. Out of that massive .tsv file I extracted 7
					languages that I especially wanted to train on; English, Mandarin, Swedish, Welsh, Portugese, German
					and Dutch. I then applied the romanisation technique I mentioned earlier and ended up with more than
					a million words for each language. I chose not to use a dictionary from each language sice I
					suspected using a real world text example would also accurately represent the frequencies of
					different words in the languages, e.g. 'dom' is a word in english (the name Dom) as well as a word
					in Swedish (the word for they). The name 'Dom' is going to come up significantly less often than the
					word for 'they', so we would want the neural network to expect the word dom to be a Swedish word.
				</p>
				<p>
					Following cary's video I decided to keep the structure of the model simple and easy to implement.
					The basic overview of the model consists of a 20 x 26-node input layer, one 128-node hidden layer
					and an 8-node output layer. The shape of the input layer is determined by the maximum word length
					that the model can handle and the number of characters it is trained on, in this case words are
					limited to a maximum of 20 characters using the 26 character latin alphabet. Then the shape of the
					output layer is determined by the number of languages the network is trained on. Since the network
					was trained on 7 real-life languages the network can output any one of those 7 languages or "Random"
					if it suspects the input word was just a series of randomly selected characters.
				</p>
			</div>
		);
	}
}

export default Main;
