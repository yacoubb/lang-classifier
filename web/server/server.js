const app = require('express')();
const cors = require('cors');

var allowedOrigins = ['http://localhost:3000', 'https://yacoubahmed.me'];
app.use(
	cors({
		origin: function(origin, callback) {
			// allow requests with no origin
			// (like mobile apps or curl requests)
			if (!origin) return callback(null, true);
			if (allowedOrigins.indexOf(origin) === -1) {
				var msg = 'The CORS policy for this site does not ' + 'allow access from the specified Origin.';
				return callback(new Error(msg), false);
			}
			return callback(null, true);
		}
	})
);
const fs = require('fs');
const https = require('http');
const port = 3003;
const credentials = {};
const secureServer = https.createServer(credentials, app);
secureServer.listen(port, err => {
	if (err) console.error(err);
	console.log(`HTTPS typing_game server running on port ${port}`);
});

const model = JSON.parse(fs.readFileSync('./converted_model/model.json'));

app.get('/', (req, res) => {
	res.end(
		`<div>
			<h1>Keras Model Server</h1>
			<p>You shouldn't be back here!</p>
		</div>`
	);
});

app.get('/model', (req, res) => {
	res.json(model);
});

app.get('/group1-shard1of1.bin', (req, res) => {
	const readStream = fs.createReadStream('./converted_model/group1-shard1of1.bin');
	readStream.pipe(res);
});

const metadata = JSON.parse(fs.readFileSync('./converted_model/metadata.json'));

app.get('/metadata', (req, res) => {
	res.json(metadata);
});
