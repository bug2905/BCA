// Countdown Timer
const countdown = document.getElementById("countdown");
const birthday = new Date("September 19, 2025 00:01:00").getTime();
const interval = setInterval(() => {
  const now = new Date().getTime();
  const distance = birthday - now;

  if (distance < 0) {
    countdown.innerHTML = "🎉 It's Falguni's Birthday Today!";
    clearInterval(interval);
    return;
  }

  const days = Math.floor(distance / (1000 * 60 * 60 * 24));
  const hours = Math.floor((distance / (1000 * 60 * 60)) % 24);
  const minutes = Math.floor((distance / (1000 * 60)) % 60);
  const seconds = Math.floor((distance / 1000) % 60);
  countdown.innerHTML = `⏳ ${days}d ${hours}h ${minutes}m ${seconds}s until her birthday!`;
}, 1000);

// Music Toggle
function toggleMusic() {
  const music = document.getElementById("bg-music");
  if (music.paused) {
    music.play();
  } else {
    music.pause();
  }
}

// Lightbox
function openLightbox(img) {
  const lightbox = document.getElementById("lightbox");
  const lightboxImg = document.getElementById("lightbox-img");
  lightboxImg.src = img.src;
  lightbox.style.display = "flex";
}
function closeLightbox() {
  document.getElementById("lightbox").style.display = "none";
}

// Wishes Board
document.getElementById("wish-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const name = document.getElementById("name").value;
  const wish = document.getElementById("wish").value;
  const wishBoard = document.getElementById("wish-board");

  const card = document.createElement("div");
  card.className = "poem-card";
  card.innerHTML = `<p>${wish}</p><p class="signature">– ${name}</p>`;
  wishBoard.prepend(card);

  this.reset();
});
