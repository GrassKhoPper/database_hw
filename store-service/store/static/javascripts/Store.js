const gamesContainer = document.getElementById("games-container");
let isLoading = false;
let hasMore = true;

function throttle(func, delay) {
    let lastCall = 0;
    return (...args) => {
        const now = Date.now();
        if (now - lastCall < delay) return;
        lastCall = now;
        func(...args);
    };
}

async function loadMoreGames() {
    if (isLoading || !hasMore) return;
    
    isLoading = true;
    try {
        const lastGameId = gamesContainer.dataset.lastGameId;
        const response = await fetch(`/load-more-games?last_game_id=${lastGameId}`);
        
        if (response.status === 204) {
            hasMore = false;
            return;
        }

        const html = await response.text();
        gamesContainer.insertAdjacentHTML("beforeend", html);
        
        const newGames = gamesContainer.querySelectorAll(".item");
        if (newGames.length > 0) {
            const lastGameLink = newGames[newGames.length - 1].querySelector("a").href;
            gamesContainer.dataset.lastGameId = lastGameLink.split("/").pop();
        }
    } catch (error) {
        console.error("Error loading more games:", error);
    } finally {
        isLoading = false;
    }
}

function checkScroll() {
    const threshold = 70;
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    
    if (scrollTop + clientHeight >= scrollHeight - threshold) {
        loadMoreGames();
    }
}

window.addEventListener("scroll", throttle(checkScroll, 200));
document.addEventListener("DOMContentLoaded", checkScroll);
