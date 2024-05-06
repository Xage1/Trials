const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const axios = require('axios');


const app = express();
const server = http.createServer(app);
const io = socketIo(server);

const API_URL = 'http://localhost:5000/weather';


io.on('connection', (socket) => {
	console.log('New Client connected');


	axios.get(API_URL)
		.then(response => {
			const weatherData = response.data;
			socket.emit('weatherData', weatherData);
		})
		.catch(error => {
			console.error('Error fetching Weather data:', error.message);
		});
	socket.on('disconnect', () => {
		console.log('Client disconnected');
	});
});

const PORT = process.env.PORT || 4000;
server.listen(PORT, () => {
	console.log(`Socket.io server running on port ${PORT}`);
});
