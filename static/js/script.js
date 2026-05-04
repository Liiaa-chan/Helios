/**
 * HELIOS INTERACTIVE NAVIGATION LOGIC
 * Menangani animasi FAB dan sinkronisasi orientasi layar.
 */

document.addEventListener("DOMContentLoaded", () => {
    const fabTrigger = document.getElementById("fab-trigger");
    const fabMenu = document.getElementById("fab-menu");
    const iconMenu = document.getElementById("fab-icon-menu");
    const iconClose = document.getElementById("fab-icon-close");

    let isMenuOpen = false;

    // Fungsi untuk Toggle Menu FAB
    const toggleMenu = () => {
        isMenuOpen = !isMenuOpen;

        if (isMenuOpen) {
            // Buka Menu
            fabMenu.classList.remove(
                "scale-75",
                "opacity-0",
                "pointer-events-none",
            );
            fabMenu.classList.add("scale-100", "opacity-100");
            iconMenu.classList.add("hidden");
            iconClose.classList.remove("hidden");
        } else {
            // Tutup Menu
            fabMenu.classList.add(
                "scale-75",
                "opacity-0",
                "pointer-events-none",
            );
            fabMenu.classList.remove("scale-100", "opacity-100");
            iconMenu.classList.remove("hidden");
            iconClose.classList.add("hidden");
        }
    };

    // Event Listeners
    if (fabTrigger) {
        fabTrigger.addEventListener("click", (e) => {
            e.stopPropagation();
            toggleMenu();
        });
    }

    // Klik di luar menu untuk menutup
    document.addEventListener("click", (e) => {
        if (
            isMenuOpen &&
            !fabMenu.contains(e.target) &&
            e.target !== fabTrigger
        ) {
            toggleMenu();
        }
    });

    // Menangani perubahan orientasi layar (Portrait/Landscape)
    const handleResize = () => {
        const isPortrait = window.innerHeight > window.innerWidth;
        const topNavbar = document.getElementById("top-navbar");
        const fabContainer = document.getElementById("mobile-fab-container");

        if (window.innerWidth < 640) {
            // Mobile Breakpoint
            if (isPortrait) {
                if (topNavbar) topNavbar.classList.add("hidden");
                if (fabContainer) fabContainer.classList.remove("hidden");
            } else {
                if (topNavbar) topNavbar.classList.remove("hidden");
                if (fabContainer) fabContainer.classList.add("hidden");
                if (isMenuOpen) toggleMenu(); // Tutup FAB menu saat rotasi ke landscape
            }
        }
    };

    window.addEventListener("resize", handleResize);
    handleResize(); // Inisialisasi awal
});
