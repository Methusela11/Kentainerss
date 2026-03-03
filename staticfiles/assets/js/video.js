document.addEventListener("DOMContentLoaded", function () {

    const video = document.getElementById("heroVideo");
    const muteBtn = document.getElementById("muteBtn");
    const volumeSlider = document.getElementById("volumeSlider");
    const timeLabel = document.getElementById("timeLabel");
    const fullscreenBtn = document.getElementById("fullscreenBtn");

    /* ---------------- MUTE / UNMUTE ---------------- */
    muteBtn.addEventListener("click", () => {
        video.muted = !video.muted;
        muteBtn.textContent = video.muted ? "🔇" : "🔊";
    });

    /* ---------------- VOLUME SLIDER ---------------- */
    volumeSlider.addEventListener("input", () => {
        video.volume = volumeSlider.value;
        if (video.volume > 0) {
            video.muted = false;
            muteBtn.textContent = "🔊";
        }
    });

    /* ---------------- TIME DISPLAY ---------------- */
    function formatTime(seconds) {
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60).toString().padStart(2, "0");
        return `${m}:${s}`;
    }

    video.addEventListener("loadedmetadata", () => {
        timeLabel.textContent = `0:00 / ${formatTime(video.duration)}`;
    });

    video.addEventListener("timeupdate", () => {
        timeLabel.textContent = `${formatTime(video.currentTime)} / ${formatTime(video.duration)}`;
    });

    /* ---------------- FULLSCREEN ---------------- */
    fullscreenBtn.addEventListener("click", () => {
        if (video.requestFullscreen) video.requestFullscreen();
        else if (video.webkitRequestFullscreen) video.webkitRequestFullscreen();
        else if (video.msRequestFullscreen) video.msRequestFullscreen();
    });
});

