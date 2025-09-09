window.onclick = () => {
    // Create an audio element and play the sound
    let audio = new Audio('VIP Entrance.mp3');
    audio.play();
    audio.volume = 0.5;

    setTimeout(() => {
        document.querySelector('.left').style.transform = "translateX(-100%)";
        document.querySelector('.right').style.transform = "translateX(100%)";

        setTimeout(() => {
            document.querySelector('.content').style.opacity = "1";
        }, 2000); // Ensure content appears after the gates fully open
    }, 1000); // Delay before animation starts
};
