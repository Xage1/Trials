document.addEventListener('DOMContentLoaded', () => {
	fetchWeather();
});

function fetchWeather() {
	const socket = io();
	socket.on('weatherData', (data) => {
		const weatherDiv = document.getElementById('weather');
		weatherDiv.innerHTML = `
		<h2>Weather Forecast for ${data.location}</h2>
		<p>Forecast: ${data.forecast}<p>
		<p>Temperature: ${data.temperature}</p>
		`;
	});
}
