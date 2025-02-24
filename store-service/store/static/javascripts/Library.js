var selected_screenshot;
var screenshots;

function loadGameDetails(gameId) {
	fetch(`/game-details/${gameId}`)
		.then((response) => response.text())
		.then((html) => {
			document.getElementById("game-details-container").innerHTML = html;
			preloadImages();
		})
		.catch((error) => {
			console.error("Error fetching game details:", error);
			document.getElementById("game-details-container").innerHTML =
				"<p>Error loading game details.</p>";
		});
}

let currentIndex = 0;

function preloadImages() {
	selected_screenshot = document.getElementById("selected_screenshot");

	screenshots = Array.from(document.querySelectorAll(".screenshot"));
	screenshots.forEach((img) => {
		const imgToLoad = new Image();
		imgToLoad.src = img.src;
	});
}

function selectScreenshot(screenshot) {
	screenshots.forEach((s) => s.classList.remove("selected"));
	screenshot.classList.add("selected");
	selected_screenshot.src = screenshot.src;
}
