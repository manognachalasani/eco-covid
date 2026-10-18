
/* ============================================================
   PANDEMISCOPE — NAVIGATION DROPDOWN CONTROLLER

   Behavior:
   1. Click a heading to open its dropdown.
   2. Click the same heading again to close it.
   3. Opening another heading closes the previous dropdown.
   4. Clicking outside the navigation closes all dropdowns.
   5. Clicking a navigation link closes all dropdowns.
   6. Pressing Escape closes all dropdowns.
   ============================================================ */

(function () {
    "use strict";

    // Close every open navigation group, except an optional group.
    function closeAll(exceptGroup) {
        document.querySelectorAll(".nav-group[open]").forEach(function (group) {
            if (group !== exceptGroup) {
                group.removeAttribute("open");
            }
        });
    }

    // Handle clicks on navigation headings and elsewhere on the page.
    document.addEventListener("click", function (event) {
        var summary = event.target.closest(".nav-group > summary");

        // A navigation heading was clicked.
        if (summary) {
            event.preventDefault();

            var group = summary.closest(".nav-group");
            var wasOpen = group.hasAttribute("open");

            // Close all menus first.
            closeAll();

            // Reopen this menu only if it was previously closed.
            if (!wasOpen) {
                group.setAttribute("open", "");
            }

            return;
        }

        // A page link inside a dropdown was clicked.
        if (event.target.closest(".nav-dropdown a")) {
            closeAll();
            return;
        }

        // A click outside all navigation groups closes the menus.
        if (!event.target.closest(".nav-group")) {
            closeAll();
        }
    });

    // Allow keyboard users to dismiss the menus.
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeAll();
        }
    });

    // Close menus after browser navigation changes.
    window.addEventListener("hashchange", function () {
        closeAll();
    });

    // Dash navigation uses links and may update pathname without a hash.
    // Observe URL changes caused by navigation clicks through link handling.
    document.addEventListener(
        "click",
        function (event) {
            if (event.target.closest(".nav-dropdown a")) {
                closeAll();
            }
        },
        true
    );
})();
