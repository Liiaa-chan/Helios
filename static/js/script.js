function initHeliosWorkstation() {
    // =======================================================
    // 1. LOGIKA NAVIGASI DOCK, FAB, DAN NAVBAR
    // =======================================================
    const topNavbar = document.getElementById("top-navbar");
    const dockContainer = document.getElementById("mobile-dock-container");
    const fabContainer = document.getElementById("mobile-fab-container");
    const fabTrigger = document.getElementById("fab-trigger");
    const fabMenu = document.getElementById("fab-menu");
    const iconMenu = document.getElementById("fab-icon-menu");
    const iconClose = document.getElementById("fab-icon-close");

    let isMenuOpen = false;

    // Fungsi Toggle untuk Menu FAB
    const toggleMenu = () => {
        isMenuOpen = !isMenuOpen;

        if (isMenuOpen) {
            // Buka Menu
            if (fabMenu) {
                fabMenu.classList.remove(
                    "scale-75",
                    "opacity-0",
                    "pointer-events-none",
                );
                fabMenu.classList.add("scale-100", "opacity-100");
            }
            if (iconMenu) iconMenu.classList.add("hidden");
            if (iconClose) iconClose.classList.remove("hidden");
        } else {
            // Tutup Menu
            if (fabMenu) {
                fabMenu.classList.add(
                    "scale-75",
                    "opacity-0",
                    "pointer-events-none",
                );
                fabMenu.classList.remove("scale-100", "opacity-100");
            }
            if (iconMenu) iconMenu.classList.remove("hidden");
            if (iconClose) iconClose.classList.add("hidden");
        }
    };

    // Event Listener untuk Tombol FAB Trigger
    if (fabTrigger) {
        fabTrigger.addEventListener("click", (e) => {
            e.stopPropagation();
            toggleMenu();
        });
    }

    // Fungsi penutup ketika pengguna mengeklik di luar menu FAB
    const handleOutsideClick = (e) => {
        if (
            isMenuOpen &&
            fabMenu &&
            !fabMenu.contains(e.target) &&
            e.target !== fabTrigger
        ) {
            toggleMenu();
        }
    };
    document.addEventListener("click", handleOutsideClick);

    // Fungsi untuk menangani visibilitas navigasi & orientasi layar (Portrait/Landscape)
    const handleNavigationVisibility = () => {
        const isPortrait = window.innerHeight > window.innerWidth;
        const isMobile = window.innerWidth < 640;

        if (isMobile) {
            // Tampilan Ponsel (Mobile Breakpoint)
            if (isPortrait) {
                if (topNavbar) topNavbar.classList.add("hidden");
                if (dockContainer) dockContainer.classList.remove("hidden");
                if (fabContainer) fabContainer.classList.remove("hidden");
            } else {
                if (topNavbar) topNavbar.classList.remove("hidden");
                if (dockContainer) dockContainer.classList.add("hidden");
                if (fabContainer) fabContainer.classList.add("hidden");
                if (isMenuOpen) toggleMenu(); // Tutup FAB menu saat rotasi ke landscape
            }
        } else {
            // Tampilan Desktop (Desktop Breakpoint)
            if (topNavbar) topNavbar.classList.remove("hidden");
            if (dockContainer) dockContainer.classList.add("hidden");
            if (fabContainer) fabContainer.classList.add("hidden");
        }
    };
    const sections = document.querySelectorAll("section[id]");
    const onScrollHandler = () => {
        let current = "";
        sections.forEach((section) => {
            const sectionTop = section.offsetTop;
            if (window.pageYOffset >= sectionTop - 100) {
                current = section.getAttribute("id");
            }
        });
    };
    window.addEventListener("scroll", onScrollHandler);
    window.addEventListener("resize", handleNavigationVisibility);
    handleNavigationVisibility();
    function initCodeHighlighter() {
        const quill2Containers = document.querySelectorAll(
            ".ql-code-block-container",
        );

        quill2Containers.forEach(function (container) {
            const lines = container.querySelectorAll(".ql-code-block");
            let codeText = "";

            lines.forEach(function (line, index) {
                codeText +=
                    line.textContent + (index < lines.length - 1 ? "\n" : "");
            });

            if (lines.length === 0) {
                codeText = container.textContent.trim();
            }

            const preElement = document.createElement("pre");
            preElement.className = "ql-syntax";
            preElement.textContent = codeText;

            container.parentNode.replaceChild(preElement, container);
        });

        // Pengaman jika pustaka highlight.js terlambat dimuat di peramban
        if (typeof hljs === "undefined") {
            setTimeout(initCodeHighlighter, 50);
            return;
        }

        const codeBlocks = document.querySelectorAll("pre.ql-syntax");

        codeBlocks.forEach(function (block) {
            if (block.classList.contains("hljs-initialized")) return;
            block.classList.add("hljs-initialized");

            const codeText = block.textContent.trim();
            hljs.highlightElement(block);

            // Membuat tombol Copy secara dinamis
            const button = document.createElement("button");
            button.className = "btn-copy-code";
            button.type = "button";
            button.innerText = "Copy";
            block.appendChild(button);

            button.addEventListener("click", function () {
                const tempTextArea = document.createElement("textarea");
                tempTextArea.value = codeText;
                tempTextArea.style.position = "fixed";
                document.body.appendChild(tempTextArea);
                tempTextArea.select();

                try {
                    const successful = document.execCommand("copy");
                    if (successful) {
                        button.innerText = "Copied!";
                        button.style.color = "#2dd4bf";

                        setTimeout(function () {
                            button.innerText = "Copy";
                            button.style.color = "";
                        }, 2000);
                    }
                } catch (err) {
                    button.innerText = "Failed";
                }

                document.body.removeChild(tempTextArea);
            });
        });
    }

    initCodeHighlighter();
}

document.addEventListener("DOMContentLoaded", initHeliosWorkstation);

// Pengondisian cadangan apabila dokumen selesai dimuat lebih awal sebelum skrip selesai dieksekusi
if (document.readyState !== "loading") {
    initHeliosWorkstation();
}
