/**
 * HELIOS ADMIN CUSTOM SCRIPT
 * Mengintegrasikan Quill JS, FilePond, Custom Select2 (Ikon Devicon),
 * dan Flatpickr Datepicker secara aman dengan sistem bawaan Flask-Admin.
 */

document.addEventListener("DOMContentLoaded", function () {
    // =======================================================
    // 1. INTEGRASI PREMIUM QUILL JS RICH TEXT EDITOR
    // =======================================================
    const textareaContent = document.getElementById("content");

    if (textareaContent) {
        // Sembunyikan textarea asli agar tidak merusak visual halaman
        textareaContent.style.display = "none";

        // Buat kontainer div baru untuk Quill JS secara dinamis
        const quillContainer = document.createElement("div");
        quillContainer.id = "quill-editor";
        quillContainer.style.height = "350px";
        quillContainer.style.backgroundColor = "#fff";
        quillContainer.style.color = "#1f2937"; // Teks gelap agar nyaman dibaca di latar putih editor
        quillContainer.className = "rounded-b-lg border border-zinc-200";

        // Sisipkan div editor tepat di atas textarea lama
        textareaContent.parentNode.insertBefore(
            quillContainer,
            textareaContent,
        );

        // Ambil konten lama dari database (jika sedang mengedit data)
        quillContainer.innerHTML = textareaContent.value;

        // Inisialisasi Quill JS dengan toolbar kustom yang kaya fitur
        const quill = new Quill("#quill-editor", {
            theme: "snow",
            modules: {
                toolbar: [
                    [{ header: [1, 2, 3, false] }],
                    ["bold", "italic", "underline", "strike"],
                    [{ list: "ordered" }, { list: "bullet" }],
                    ["link", "blockquote", "code-block"],
                    ["clean"],
                ],
            },
        });

        // SINKRONISASI AKTIF 1: Sinkronkan setiap perubahan teks ke textarea asli secara real-time
        quill.on("text-change", function () {
            textareaContent.value = quill.root.innerHTML;
        });

        // SINKRONISASI AKTIF 2: Jaminan akhir saat form dikirim (submit) agar data tidak kosong
        const form = textareaContent.closest("form");
        if (form) {
            form.addEventListener("submit", function () {
                textareaContent.value = quill.root.innerHTML;
            });
        }
    }

    // =======================================================
    // 2. INTEGRASI PREMIUM FILEPOND UNTUK UNGGAH GAMBAR
    // =======================================================
    // Targetkan spesifik ke input file dengan nama "image_url" agar lebih aman
    const fileInput = document.querySelector('input[name="image_url"]');

    if (fileInput && typeof FilePond !== "undefined") {
        // Daftarkan plugin pratinjau gambar FilePond
        FilePond.registerPlugin(FilePondPluginImagePreview);

        // Buat instance FilePond di atas input file
        FilePond.create(fileInput, {
            storeAsFile: true, // Memaksa FilePond bertindak seperti input file standar dalam form submit Flask
            labelIdle:
                'Seret & lepas gambar di sini atau <span class="filepond--label-action">Telusuri</span>',
            imagePreviewHeight: 200,
            imageCropAspectRatio: "16:9",
            credits: false, // Menghilangkan watermark kredit FilePond
            labelFileProcessing: "Mengunggah...",
            labelFileProcessingComplete: "Unggahan berhasil",
            labelTapToCancel: "Ketuk untuk membatalkan",
            labelTapToUndo: "Ketuk untuk menghapus gambar",
        });
    }

    // =======================================================
    // 3. INTEGRASI PREMIUM SELECT2 (IKON DEVICON + NAMA SKILL)
    // =======================================================
    if (typeof $ !== "undefined" && $.fn.select2) {
        const $selectSkill = $('select[name="skills"]');

        if ($selectSkill.length > 0) {
            // Hancurkan render ID bawaan Flask-Admin terlebih dahulu agar tidak bentrok
            if ($selectSkill.hasClass("select2-hidden-accessible")) {
                $selectSkill.select2("destroy");
            }

            // Bangun ulang Select2 menggunakan template pencetak ikon kustom kita
            $selectSkill.select2({
                templateResult: formatSkillOption,
                templateSelection: formatSkillOption,
                escapeMarkup: function (markup) {
                    return markup;
                },
                width: "100%",
            });
        }
    }

    // =======================================================
    // 4. INTEGRASI PREMIUM FLATPICKR DATEPICKER
    // =======================================================
    const dateInput = document.querySelector('input[name="date"]');
    if (dateInput) {
        // Muat stylesheet CSS Flatpickr secara dinamis jika belum ada
        if (!document.getElementById("flatpickr-css")) {
            const link = document.createElement("link");
            link.id = "flatpickr-css";
            link.rel = "stylesheet";
            link.href =
                "https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css";
            document.head.appendChild(link);
        }

        // Muat pustaka JS Flatpickr secara dinamis jika belum terdefinisi
        if (typeof flatpickr === "undefined") {
            const script = document.createElement("script");
            script.src = "https://cdn.jsdelivr.net/npm/flatpickr";
            script.onload = function () {
                initFlatpickr(dateInput);
            };
            document.head.appendChild(script);
        } else {
            initFlatpickr(dateInput);
        }
    }
});

/**
 * Inisialisasi instansi Flatpickr pada elemen input tanggal
 */
function initFlatpickr(element) {
    // Deteksi jika input kosong (artinya mode 'Create' data baru)
    const isCreateMode = !element.value;

    flatpickr(element, {
        dateFormat: "Y-m-d", // Format data asli yang dikirim ke database Flask
        altInput: true, // Mengaktifkan kolom samaran tampilan ramah pengguna
        altFormat: "j F Y", // Format tampilan tanggal ramah bahasa lokal (contoh: 15 Mei 2026)
        allowInput: true,
        defaultDate: isCreateMode ? "today" : undefined, // Isi otomatis hari ini jika membuat data baru
        locale: {
            firstDayOfWeek: 1,
        },
    });
}

/**
 * Memproses teks string option "__str__" dari database
 * Mengubah format: "Laravel (devicon-laravel-original)" -> Tag HTML Berikon Devicon
 */
function formatSkillOption(state) {
    if (!state.id) {
        return state.text;
    }

    // Regex memisahkan nama skill dan kelas ikonnya (telah diperbaiki dari format LaTeX)
    const regex = /(.*)\s\((devicon-.*|fa-.*)\)/;
    const match = state.text.match(regex);

    if (match) {
        const skillName = match[1];
        return `<span><i class="${iconClass} colored mr-2" style="font-size: 1.25rem; display: inline-block; vertical-align: middle;"></i> ${skillName}</span>`;
    }

    return state.text;
}

document.addEventListener("DOMContentLoaded", function () {
    // 1. Daftarkan plugin pratinjau gambar (otomatis dilewati jika filenya adalah PDF)
    if (typeof FilePondPluginImagePreview !== "undefined") {
        FilePond.registerPlugin(FilePondPluginImagePreview);
    }

    // 2. Cari semua elemen input file di halaman admin secara otomatis
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach((input) => {
        // Inisialisasi FilePond untuk setiap input file yang ditemukan
        FilePond.create(input, {
            labelIdle:
                'Seret & lepas berkas di sini atau <span class="filepond--label-action">Telusuri</span>',
            allowMultiple: false,
            instantUpload: false, // Biarkan form Flask-Admin yang mengurus submit datanya
            credits: false, // Menghapus watermark bertenaga FilePond di pojok bawah
        });
    });
});
