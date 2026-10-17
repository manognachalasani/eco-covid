/* ==========================================================
   DATA & METHODOLOGY — STORY ENGINE
   Intro animation, scroll reveals and reading progress.
   Works with Dash page navigation (no full reload needed).
   Put this file in the Dash assets/ folder.
   IDs below must match the ones in data_methodology.py.
   ========================================================== */

(() => {
    "use strict";

    const ROOT_ID = "methodology-story";
    const INTRO_ID = "methodology-chapter-intro";
    const PROGRESS_ID = "methodology-progress-fill";
    const INTRO_DURATION_MS = 3300;

    let activeRoot = null;
    let revealObserver = null;
    let progressHandler = null;
    let progressFrame = null;
    let introTimer = null;
    let rootCheckFrame = null;

    const prefersReducedMotion = () =>
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    /* ---------- cleanup when the page is left or replaced ---------- */

    function cleanup() {
        if (revealObserver) {
            revealObserver.disconnect();
            revealObserver = null;
        }
        if (progressHandler) {
            window.removeEventListener("scroll", progressHandler);
            window.removeEventListener("resize", progressHandler);
            progressHandler = null;
        }
        if (progressFrame !== null) {
            window.cancelAnimationFrame(progressFrame);
            progressFrame = null;
        }
        if (introTimer !== null) {
            window.clearTimeout(introTimer);
            introTimer = null;
        }
    }

    /* ---------- intro ---------- */

    function playIntro(root) {
        const overlay = root.querySelector(`#${INTRO_ID}`);
        if (!overlay) return;

        if (prefersReducedMotion()) {
            overlay.remove();
            return;
        }

        overlay.classList.remove("is-playing");
        void overlay.offsetWidth; // restart the CSS animation
        overlay.classList.add("is-playing");

        // Remove the overlay when finished so it can never block the page.
        introTimer = window.setTimeout(() => {
            if (overlay.isConnected) overlay.remove();
            introTimer = null;
        }, INTRO_DURATION_MS);
    }

    /* ---------- scroll reveals ---------- */

    function setupReveals(root) {
        const items = root.querySelectorAll(".reveal");

        if (prefersReducedMotion() || !("IntersectionObserver" in window)) {
            root.classList.remove("story-animations-ready");
            items.forEach((el) => el.classList.add("is-visible"));
            return;
        }

        revealObserver = new IntersectionObserver(
            (entries, observer) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { root: null, rootMargin: "0px 0px -7% 0px", threshold: 0.08 }
        );

        items.forEach((el) => {
            el.classList.remove("is-visible");
            revealObserver.observe(el);
        });

        root.classList.add("story-animations-ready");
    }

    /* ---------- reading progress ---------- */

    function setupProgress(root) {
        function update() {
            progressFrame = null;
            if (activeRoot !== root || !root.isConnected) return;

            const fill = root.querySelector(`#${PROGRESS_ID}`);
            if (!fill) return;

            const scrollable = Math.max(1, root.offsetHeight - window.innerHeight);
            const travelled = Math.max(0, Math.min(scrollable, -root.getBoundingClientRect().top));
            fill.style.width = `${(travelled / scrollable) * 100}%`;
        }

        progressHandler = () => {
            if (progressFrame === null) {
                progressFrame = window.requestAnimationFrame(update);
            }
        };

        window.addEventListener("scroll", progressHandler, { passive: true });
        window.addEventListener("resize", progressHandler, { passive: true });
        update();
    }

    /* ---------- page initialisation ---------- */

    function initialize() {
        const root = document.getElementById(ROOT_ID);

        if (!root) {
            // The page is not mounted (the user went somewhere else).
            if (activeRoot !== null) {
                cleanup();
                activeRoot = null;
            }
            return;
        }

        if (root === activeRoot) return; // ordinary DOM update, nothing to do

        cleanup();
        activeRoot = root;

        playIntro(root);
        setupReveals(root);
        setupProgress(root);
    }

    function scheduleCheck() {
        if (rootCheckFrame !== null) return;
        rootCheckFrame = window.requestAnimationFrame(() => {
            rootCheckFrame = null;
            initialize();
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", scheduleCheck, { once: true });
    } else {
        scheduleCheck();
    }

    // Dash replaces page layouts without reloading: watch for it.
    new MutationObserver(scheduleCheck).observe(document.documentElement, {
        childList: true,
        subtree: true,
    });

    window.addEventListener("pageshow", scheduleCheck);
    window.addEventListener("popstate", scheduleCheck);
})();
