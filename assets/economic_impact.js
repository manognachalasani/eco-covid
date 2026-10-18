
/* ==========================================================
   CHAPTER 2 — SCROLL STORY ENGINE
   Scoped to #economic-story.
   No external libraries required.
   ========================================================== */

(() => {
    "use strict";

    const ROOT_ID = "economic-story";
    let observer = null;
    let activeRoot = null;
    let progressFrame = null;

    function initializeStory() {
        const root = document.getElementById(ROOT_ID);

        // Dash can replace page layouts during navigation.
        if (!root || root === activeRoot) return;

        if (observer) {
            observer.disconnect();
            observer = null;
        }

        activeRoot = root;
        playChapterIntro(root);

        const reduceMotion = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

        const sections = root.querySelectorAll(".reveal");

        if (reduceMotion || !("IntersectionObserver" in window)) {
            root.classList.remove("story-animations-ready");
            sections.forEach((section) => {
                section.classList.add("is-visible");
            });
            return;
        }

        // Avoid showing all the story at once before the observer
        // has been attached.
        observer = new IntersectionObserver(
            (entries, currentObserver) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        currentObserver.unobserve(entry.target);
                    }
                });
            },
            {
                root: null,
                rootMargin: "0px 0px -7% 0px",
                threshold: 0.08,
            }
        );

        sections.forEach((section) => {
            observer.observe(section);
        });

        root.classList.add("story-animations-ready");

        // Update the reading progress indicator.
        function updateProgress() {
            progressFrame = null;

            if (!activeRoot || !activeRoot.isConnected) return;

            const rect = activeRoot.getBoundingClientRect();
            const viewportHeight = window.innerHeight;

            const totalScrollable = Math.max(
                1,
                activeRoot.offsetHeight - viewportHeight
            );

            const travelled = Math.max(
                0,
                Math.min(totalScrollable, -rect.top)
            );

            const progress = travelled / totalScrollable;

            const fill = activeRoot.querySelector(
                "#story-progress-fill"
            );

            if (fill) {
                fill.style.width = `${progress * 100}%`;
            }
        }

        function requestProgressUpdate() {
            if (progressFrame !== null) return;

            progressFrame = window.requestAnimationFrame(updateProgress);
        }

        window.addEventListener("scroll", requestProgressUpdate, {
            passive: true,
        });

        window.addEventListener("resize", requestProgressUpdate, {
            passive: true,
        });

        // A scroll or resize event updates progress efficiently.
        updateProgress();
    }

    // Standard initial page load.
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initializeStory, {
            once: true,
        });
    } else {
        initializeStory();
    }

    // Support Dash applications that switch pages without reloading.
    const navigationObserver = new MutationObserver(() => {
        const root = document.getElementById(ROOT_ID);

        if (root && root !== activeRoot) {
            initializeStory();
        }
    });

    navigationObserver.observe(document.documentElement, {
        childList: true,
        subtree: true,
    });
})();

function playChapterIntro(root) {
    const overlay = root.querySelector("#chapter-intro-overlay");

    if (!overlay || overlay.dataset.played === "true") return;

    // Respect accessibility preferences.
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        overlay.remove();
        return;
    }

    overlay.dataset.played = "true";
    overlay.classList.add("is-playing");

    // Remove it after the animation so it cannot block the page.
    window.setTimeout(() => {
        overlay.remove();
    }, 3900);
}
