"use strict";

// Native <details> supplies the mobile disclosure, including without JavaScript.
document.querySelectorAll("[data-mobile-menu]").forEach((menu) => {
    const summary = menu.querySelector("summary");
    const desktopLinks = menu.closest("nav").querySelector(".nav-links-desktop");
    const mobile = window.matchMedia("(max-width: 900px)");
    const closeMenu = (restoreFocus) => {
        menu.open = false;
        if (restoreFocus) summary.focus();
    };
    menu.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && menu.open) {
            event.preventDefault();
            closeMenu(true);
        }
    });
    menu.addEventListener("click", (event) => {
        if (event.target.closest("a")) closeMenu(true);
    });
    document.addEventListener("click", (event) => {
        if (menu.open && !menu.contains(event.target)) closeMenu(false);
    });
    mobile.addEventListener("change", () => {
        if (!mobile.matches && menu.contains(document.activeElement)) {
            desktopLinks.querySelector("a")?.focus();
        } else if (mobile.matches && desktopLinks.contains(document.activeElement)) {
            summary.focus();
        }
        closeMenu(false);
    });
});
