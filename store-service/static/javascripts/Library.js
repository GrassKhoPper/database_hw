function loadGameDetails(gameId) {
	fetch(`/game-details/${gameId}`)
		.then(response => response.text())
		.then(html => {
			document.getElementById('game-details-container').innerHTML = html;
		})
		.catch(error => {
			console.error('Error fetching game details:', error);
			document.getElementById('game-details-container').innerHTML = '<p>Error loading game details.</p>';
		});
}