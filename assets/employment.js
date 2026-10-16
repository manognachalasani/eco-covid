
/* ==========================================================
   CHAPTER 3 — EMPLOYMENT STORY ENGINE
   Cinematic intro, scroll reveals and reading progress.
   Supports Dash page navigation without a full reload.
   ========================================================== */

(() => {
    "use strict";

    const ROOT_ID = "employment-story";
    const INTRO_ID = "employment-chapter-intro";
    const INTRO_DURATION_MS = 4100;

    let activeRoot = null;
    let revealObserver = null;
    let progressHandler = null;
    let progressFrame = null;
    let introTimer = null;
    let rootCheckFrame = null;

    /* ------------------------------------------------------
       CLEANUP
       ------------------------------------------------------ */

    function cleanupPageListeners() {
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

    /* ------------------------------------------------------
       CINEMATIC CHAPTER INTRO
       ------------------------------------------------------ */

    function playIntro(root) {
        const overlay = root.querySelector(`#${INTRO_ID}`);

        if (!overlay) {
            console.warn(
                "[employment.js] Could not find #employment-chapter-intro."
            );
            return;
        }

        const reduceMotion = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

        if (reduceMotion) {
            overlay.remove();
            return;
        }

        // Reset any previous animation state.
        overlay.classList.remove("is-playing");

        // Ensure the overlay is visible before the animation begins.
        overlay.style.opacity = "1";
        overlay.style.visibility = "visible";
        overlay.style.pointerEvents = "auto";

        // Force the browser to apply the reset before restarting.
        void overlay.offsetWidth;

        overlay.classList.add("is-playing");

        // Remove the overlay after the cinematic intro finishes.
        introTimer = window.setTimeout(() => {
            if (overlay.isConnected) {
                overlay.remove();
            }

            introTimer = null;
        }, INTRO_DURATION_MS);
    }

    /* ------------------------------------------------------
       SCROLL REVEALS
       ------------------------------------------------------ */

    function setupReveals(root) {
        const sections = root.querySelectorAll(".reveal");

        const reduceMotion = window.matchMedia(
            "(prefers-reduced-motion: reduce)"
        ).matches;

        if (
            reduceMotion ||
            !("IntersectionObserver" in window)
        ) {
            root.classList.remove("story-animations-ready");

            sections.forEach((section) => {
                section.classList.add("is-visible");
            });

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
            {
                root: null,
                rootMargin: "0px 0px -7% 0px",
                threshold: 0.08,
            }
        );

        sections.forEach((section) => {
            section.classList.remove("is-visible");
            revealObserver.observe(section);
        });

        root.classList.add("story-animations-ready");
    }

    /* ------------------------------------------------------
       READING PROGRESS
       ------------------------------------------------------ */

    function setupProgress(root) {
        function updateProgress() {
            progressFrame = null;

            if (
                !activeRoot ||
                activeRoot !== root ||
                !root.isConnected
            ) {
                return;
            }

            const fill = root.querySelector(
                "#employment-progress-fill"
            );

            if (!fill) {
                return;
            }

            const rect = root.getBoundingClientRect();

            const totalScrollable = Math.max(
                1,
                root.offsetHeight - window.innerHeight
            );

            const travelled = Math.max(
                0,
                Math.min(totalScrollable, -rect.top)
            );

            fill.style.width =
                `${(travelled / totalScrollable) * 100}%`;
        }

        progressHandler = () => {
            if (progressFrame !== null) {
                return;
            }

            progressFrame =
                window.requestAnimationFrame(updateProgress);
        };

        window.addEventListener(
            "scroll",
            progressHandler,
            { passive: true }
        );

        window.addEventListener(
            "resize",
            progressHandler,
            { passive: true }
        );

        updateProgress();
    }

    /* ------------------------------------------------------
       PAGE INITIALIZATION
       ------------------------------------------------------ */

    function initializeEmploymentStory() {
        const root = document.getElementById(ROOT_ID);

        // Chapter 3 is not currently mounted.
        if (!root) {
            if (activeRoot !== null) {
                cleanupPageListeners();
                activeRoot = null;
            }

            return;
        }

        // Don't initialize repeatedly for ordinary DOM updates.
        if (root === activeRoot) {
            return;
        }

        cleanupPageListeners();
        activeRoot = root;

        playIntro(root);
        setupReveals(root);
        setupProgress(root);
    }

    /* ------------------------------------------------------
       DASH NAVIGATION SUPPORT
       ------------------------------------------------------ */

    function scheduleRootCheck() {
        if (rootCheckFrame !== null) {
            return;
        }

        rootCheckFrame = window.requestAnimationFrame(() => {
            rootCheckFrame = null;
            initializeEmploymentStory();
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            scheduleRootCheck,
            { once: true }
        );
    } else {
        scheduleRootCheck();
    }

    // Detect when Dash replaces one page with another.
    const navigationObserver = new MutationObserver(
        scheduleRootCheck
    );

    navigationObserver.observe(
        document.documentElement,
        {
            childList: true,
            subtree: true,
        }
    );

    // Also check after browser history navigation.
    window.addEventListener("pageshow", scheduleRootCheck);
    window.addEventListener("popstate", scheduleRootCheck);
})();
