const loadMoreButton = document.getElementById('load-more-button');
const gamesContainer = document.getElementById('games-container');

loadMoreButton.addEventListener('click', () => {
	const lastGameId = loadMoreButton.dataset.lastGameId;
	fetch(`/load-more-games?last_game_id=${lastGameId}`)
		.then(response => {
			if (response.status === 204) {
				loadMoreButton.style.display = 'none';
				throw new Error('No more content');
			}
			return response.text();
		})
		.then(html => {
			gamesContainer.insertAdjacentHTML('beforeend', html);
			const newGames = gamesContainer.querySelectorAll('.item');
			const newLastGameId = newGames.length > 0 ? newGames[newGames.length - 1].querySelector('a').href.split('/').pop() : lastGameId;

			loadMoreButton.dataset.lastGameId = newLastGameId;
		})
		.catch(error => {
			console.error('Error:', error);
		});
});