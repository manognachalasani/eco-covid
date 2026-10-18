(function () {
    function initialisePandemicAnimations() {
        const page = document.querySelector(".pandemic-story");

        if (!page) return;

        const elements = page.querySelectorAll(
            ".p-demo-note, .p-section, .p-panel, .p-metric, .p-ending"
        );

        elements.forEach((element) => {
            element.classList.add("js-reveal");
        });

        if (!("IntersectionObserver" in window)) {
            elements.forEach((element) => {
                element.classList.add("is-visible");
            });
            return;
        }

        if (page.dataset.animationObserverReady === "true") return;

        page.dataset.animationObserverReady = "true";

        const observer = new IntersectionObserver(
            (entries, currentObserver) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        currentObserver.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.12,
                rootMargin: "0px 0px -30px 0px"
            }
        );

        elements.forEach((element) => {
            observer.observe(element);
        });
    }

    function start() {
        initialisePandemicAnimations();

        const pageChanges = new MutationObserver(() => {
            function start() {
    removeIntroOverlay();
    initialisePandemicAnimations();

    const pageChanges = new MutationObserver(() => {
        initialisePandemicAnimations();
    });

    pageChanges.observe(document.body, {
        childList: true,
        subtree: true
    });
}
            initialisePandemicAnimations();
        });

        pageChanges.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start);
    } else {
        start();
    }

    function removeIntroOverlay() {
    const intro = document.querySelector("#pandemic-intro");
    if (!intro) return;

    intro.addEventListener("animationend", (event) => {
        if (event.animationName === "pandemic-intro-exit") {
            intro.remove();
        }
    }, { once: true });
}
})();