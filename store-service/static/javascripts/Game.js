const screenshotContainer = document.getElementById("scroll_screenshots");
const selected_screenshot = document.getElementById("selected_screenshot");
const screenshots = Array.from(document.querySelectorAll(".screenshot"));

let currentIndex = 0;

function preloadImages() {
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

preloadImages();
