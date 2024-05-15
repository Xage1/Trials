const express = require('express');
const Redis = require('ioredis');

const app = express()
const redis = new Redis();

app.post('/set', (req, res) => {
	const { key, value } = req.body;
	redis.set(key, value)
		.then(() => res.send('Key-value pair set successfully'))
		.catch((err) => {
			console.error('Error:', err);
			res.status(500).send('Internal Server Error');
		});
});

app.get('/get/:key', (req, res) => {
	const { key } = req.params;
	redis.get(key)
		.then((result) => res.send(result))
		.catch((err) => {
			console.error('Error:', err);
			res.status(500).send('Internal Server Error');
		});
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
	console.log(`Server is running on port ${PORT}`);
});

app.use((err, req, res, next) => {
	console.error('Error:', err);
	res.status(500).send('Internal Server Error');
});

process.on('SIGINT', () => {
	redis.quit();
	console.log('Redis connection closed');
	process.exit();
});
