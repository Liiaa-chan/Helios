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

function initCodeHighlighter() {
    // =========================================================================
    // A. ENGINE KOMPATIBILITAS: Konversi Format Quill 2.0 ke Standard Pre Tag
    // =========================================================================
    const quill2Containers = document.querySelectorAll(
        ".ql-code-block-container",
    );

    quill2Containers.forEach(function (container) {
        // Cari semua baris kode bertipe ql-code-block
        const lines = container.querySelectorAll(".ql-code-block");
        let codeText = "";

        lines.forEach(function (line, index) {
            // Satukan teks dengan enters (\n)
            codeText +=
                line.textContent + (index < lines.length - 1 ? "\n" : "");
        });

        // Fallback jika baris tidak ditemukan
        if (lines.length === 0) {
            codeText = container.textContent.trim();
        }

        // Buat elemen pre standard pengganti
        const preElement = document.createElement("pre");
        preElement.className = "ql-syntax";
        preElement.textContent = codeText;

        // Ganti kontainer lama milik Quill 2.0 dengan pre standard buatan kita
        container.parentNode.replaceChild(preElement, container);
    });

    // =========================================================================
    // B. PEWARNAAN SINTAKSIS & GENERATOR TOMBOL COPY
    // =========================================================================
    const codeBlocks = document.querySelectorAll("pre.ql-syntax");

    codeBlocks.forEach(function (block) {
        // Mencegah duplikasi inisialisasi jika fungsi terpanggil dua kali
        if (block.classList.contains("hljs-initialized")) return;
        block.classList.add("hljs-initialized");

        // Ambil teks murni sebelum tombol disisipkan
        const codeText = block.textContent.trim();

        // 1. Jalankan pewarnaan sintaksis menggunakan Highlight.js
        hljs.highlightElement(block);

        // 2. Buat elemen tombol Copy secara dinamis
        const button = document.createElement("button");
        button.className = "btn-copy-code";
        button.type = "button";
        button.innerText = "Copy";

        // Masukkan tombol ke dalam blok kode
        block.appendChild(button);

        // 3. Fungsi Event Listener Klik untuk Menyalin
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
                    button.style.color = "#2dd4bf"; // Ubah warna teks jadi teal

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

// Eksekusi instan jika DOM sudah selesai dimuat untuk mengantisipasi keterlambatan CDN
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initCodeHighlighter);
} else {
    initCodeHighlighter();
}
