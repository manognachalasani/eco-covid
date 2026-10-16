
/* =========================================================
   OVERVIEW INTRO VIDEO CONTROLLER
   Vanilla JavaScript; no additional dependencies.
   ========================================================= */

(() => {
    "use strict";

    function initializeIntroVideo() {
        const openButton = document.getElementById("open-intro-video");
        const overlay = document.getElementById("intro-video-overlay");
        const video = document.getElementById("intro-video-player");
        const closeButton = document.getElementById("close-intro-video");
        const skipButton = document.getElementById("skip-intro-video");
        const status = document.getElementById("intro-video-status");

        if (
            !openButton ||
            !overlay ||
            !video ||
            !closeButton ||
            !skipButton
        ) {
            return;
        }

        // Prevent duplicate listeners if Dash remounts the page.
        if (overlay.dataset.initialized === "true") return;
        overlay.dataset.initialized = "true";

        let isOpen = false;
        let previousOverflow = "";
        let previousFocus = null;

        function showStatus(message) {
            if (status) status.textContent = message;
        }

        function openVideo() {
            if (isOpen) return;

            isOpen = true;
            previousFocus = document.activeElement;
            previousOverflow = document.body.style.overflow;

            overlay.classList.remove("is-closing");
            overlay.classList.add("is-open");
            overlay.setAttribute("aria-hidden", "false");

            // Keep the page underneath stationary while the video plays.
            document.body.style.overflow = "hidden";

            video.pause();
            video.currentTime = 0;
            video.muted = false;
            video.volume = 1;

            showStatus("");

            // User interaction initiated playback, allowing sound
            // where browser autoplay policy permits it.
            const playback = video.play();

            if (playback && typeof playback.catch === "function") {
                playback.catch(() => {
                    showStatus(
                        "Playback did not start automatically. " +
                        "Press Play on the video to begin."
                    );
                });
            }

            closeButton.focus({ preventScroll: true });
        }

        function closeVideo() {
            if (!isOpen) return;

            isOpen = false;

            video.pause();

            overlay.classList.remove("is-open");
            overlay.classList.add("is-closing");
            overlay.setAttribute("aria-hidden", "true");

            document.body.style.overflow = previousOverflow;

            // Reset after playback stops, ready for another viewing.
            try {
                video.currentTime = 0;
            } catch (_) {
                // Some browsers may reject seeking before metadata loads.
            }

            showStatus("");

            window.setTimeout(() => {
                overlay.classList.remove("is-closing");
            }, 280);

            if (previousFocus && typeof previousFocus.focus === "function") {
                previousFocus.focus({ preventScroll: true });
            } else {
                openButton.focus({ preventScroll: true });
            }
        }

        openButton.addEventListener("click", openVideo);
        closeButton.addEventListener("click", closeVideo);
        skipButton.addEventListener("click", closeVideo);

        // Automatically return to Overview when the video ends.
        video.addEventListener("ended", closeVideo);

        // Escape closes the video when the overlay is active.
        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && isOpen) {
                closeVideo();
            }
        });

        // If the video file cannot load, explain the problem.
        video.addEventListener("error", () => {
            if (isOpen) {
                showStatus(
                    "The video could not be loaded. " +
                    "Check that assets/intro.mp4 exists and is a valid MP4."
                );
            }
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            initializeIntroVideo,
            { once: true }
        );
    } else {
        initializeIntroVideo();
    }

    // Support Dash page navigation without a full browser reload.
    const observer = new MutationObserver(() => {
        initializeIntroVideo();
    });

    observer.observe(document.documentElement, {
        childList: true,
        subtree: true,
    });
})();
