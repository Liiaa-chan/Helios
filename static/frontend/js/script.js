// Active Button For Navigation Button
document.addEventListener("DOMContentLoaded", function () {
    const sections = document.querySelectorAll("section[id]");
    const navLinks = document.querySelectorAll(".nav-link");

    window.addEventListener("scroll", () => {
        let current = "";

        sections.forEach((section) => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;

            // Logika: Jika scroll sudah melewati 1/3 bagian section
            if (pageYOffset >= sectionTop - sectionHeight / 3) {
                current = section.getAttribute("id");
            }
        });

        navLinks.forEach((link) => {
            link.classList.remove("active");
            // Cek apakah href link sama dengan id section yang sedang aktif
            if (link.getAttribute("href").includes(current)) {
                link.classList.add("active");
            }
        });
    });
});
