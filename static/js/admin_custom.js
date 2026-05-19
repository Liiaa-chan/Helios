/**
 * HELIOS ADMIN CUSTOM SCRIPT - FULL FEATURED PRODUCTION VERSION
 * Mengintegrasikan Quill JS (Full Toolbar + Cloudinary Image Handler), 
 * FilePond (Cloudinary Shadow Input), Custom Select2 (Ikon Devicon), 
 * dan Flatpickr secara aman dengan Flask-Admin.
 */

document.addEventListener("DOMContentLoaded", function () {
    
    // =========================================================================
    // 1. INTEGRASI PREMIUM QUILL JS (FULL TOOLBAR + CLOUD IMAGE INTERCEPTOR)
    // =========================================================================
    const textareaContent = document.getElementById("content");

    if (textareaContent) {
        // Sembunyikan textarea asli agar tidak merusak visual halaman
        textareaContent.style.display = "none";

        // Buat kontainer div baru untuk Quill JS secara dinamis
        const quillContainer = document.createElement("div");
        quillContainer.id = "quill-editor";
        quillContainer.style.height = "450px"; // Dimensi lega untuk penulisan artikel panjang
        quillContainer.style.backgroundColor = "#121214"; 
        quillContainer.style.color = "#ffffff"; 
        quillContainer.className = "rounded-b-lg border border-zinc-800";

        // Sisipkan div editor tepat di atas textarea lama
        textareaContent.parentNode.insertBefore(quillContainer, textareaContent);

        // Ambil konten lama dari database (jika sedang mengedit data)
        quillContainer.innerHTML = textareaContent.value;

        // DAFTAR PENGATURAN TOOLBAR LENGKAP (Highlighter, Font, Media & Format)
        const fullToolbarOptions = [
            [{ 'header': [1, 2, 3, 4, false] }],
            [{ 'font': [] }, { 'size': [] }],
            ["bold", "italic", "underline", "strike"],        
            [{ 'color': [] }, { 'background': [] }],          // <--- HIGHLIGHTER KALIMAT (Background & Text Color)
            [{ 'script': 'sub'}, { 'script': 'super' }],      
            [{ 'list': 'ordered'}, { 'list': 'bullet' }, { 'indent': '-1'}, { 'indent': '+1' }],
            [{ 'direction': 'rtl' }, { 'align': [] }],        
            ["link", "image", "video", "blockquote", "code-block"], // <--- MEDIA INTEGRATION
            ["clean"]                                         
        ];

        // Inisialisasi Quill JS
        const quill = new Quill("#quill-editor", {
            theme: "snow",
            modules: {
                toolbar: fullToolbarOptions
            },
        });

        // =====================================================================
        // KUSTOM HANDLER: Cegah Penyimpanan Base64 & Alirkan Gambar ke Cloudinary
        // =====================================================================
        const toolbar = quill.getModule('toolbar');
        toolbar.addHandler('image', function() {
            const fileInput = document.createElement('input');
            fileInput.setAttribute('type', 'file');
            fileInput.setAttribute('accept', 'image/*');
            fileInput.click();

            fileInput.onchange = () => {
                const file = fileInput.files[0];
                if (file) {
                    const formData = new FormData();
                    formData.append('file', file); // Menggunakan payload form upload

                    // Ubah kursor menjadi loading/wait
                    quill.root.style.cursor = 'wait';

                    // Alirkan langsung ke endpoint API /api/upload
                    fetch('/api/upload', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.text())
                    .then(url => {
                        if (url && url.startsWith('http')) {
                            // Ambil letak kursor aktif di editor
                            const range = quill.getSelection();
                            // Masukkan URL HTTPS permanen dari Cloudinary sebagai tag <img>
                            quill.insertEmbed(range.index, 'image', url);
                        } else {
                            console.error('Unggahan gagal atau balikan URL tidak sesuai.');
                        }
                    })
                    .catch(err => console.error('Quill Cloudinary Upload Error:', err))
                    .finally(() => {
                        // Kembalikan kursor ke bentuk semula
                        quill.root.style.cursor = 'auto';
                    });
                }
            };
        });

        // SINKRONISASI 1: Sinkronkan setiap perubahan teks ke textarea asli secara real-time
        quill.on("text-change", function () {
            textareaContent.value = quill.root.innerHTML;
        });

        // SINKRONISASI 2: Jaminan akhir saat form dikirim (submit) agar data tidak kosong
        const form = textareaContent.closest("form");
        if (form) {
            form.addEventListener("submit", function () {
                textareaContent.value = quill.root.innerHTML;
            });
        }
    }

    // =========================================================================
    // 2. INTEGRASI PREMIUM FILEPOND (METODE SHADOW INPUT UNTUK CLOUDINARY)
    // =========================================================================
    if (typeof FilePond !== "undefined") {
        if (typeof FilePondPluginImagePreview !== "undefined") {
            FilePond.registerPlugin(FilePondPluginImagePreview);
        }

        // Cari semua input teks URL media yang ingin kita hubungkan dengan FilePond
        const targetTextInputs = document.querySelectorAll('input[name="image_url"], input[name="file_name"]');

        targetTextInputs.forEach(textInput => {
            // Sembunyikan input teks asli bawaan Flask-Admin
            textInput.style.display = "none";

            // Buat elemen input file bayangan (shadow input) untuk memicu FilePond
            const shadowFileInput = document.createElement("input");
            shadowFileInput.setAttribute("type", "file");
            shadowFileInput.className = "filepond-shadow-input";
            
            // Sisipkan input file bayangan tepat sebelum input teks asli
            textInput.parentNode.insertBefore(shadowFileInput, textInput);

            // Ambil URL yang sudah ada sebelumnya (jika dalam mode edit data)
            const existingUrl = textInput.value;
            const initialFiles = [];

            if (existingUrl && existingUrl.startsWith("http")) {
                initialFiles.push({
                    source: existingUrl,
                    options: {
                        type: 'local' // Beritahu FilePond bahwa ini berkas dari server awan
                    }
                });
            }

            // Inisialisasi FilePond pada input bayangan
            const pond = FilePond.create(shadowFileInput, {
                labelIdle: 'Seret & lepas berkas di sini atau <span class="filepond--label-action">Telusuri</span>',
                allowMultiple: false,
                credits: false,
                imagePreviewHeight: 180,
                imageCropAspectRatio: "16:9",
                files: initialFiles,

                // Server API Connector ke Flask Backend
                server: {
                    process: '/api/upload', // Arahkan ke rute Cloudinary Flask
                    revert: null,
                    // Mendukung load gambar lama saat edit agar pratinjau muncul otomatis
                    load: (source, load, error, progress, abort, headers) => {
                        fetch(source)
                            .then(res => res.blob())
                            .then(load)
                            .catch(error);
                    }
                }
            });

            // SINKRONISASI 1: Ketika berkas sukses diunggah ke Cloudinary, simpan URL ke input teks asli
            pond.on('processfile', (err, file) => {
                if (!err && file.serverId) {
                    textInput.value = file.serverId; // Menyimpan URL HTTPS Cloudinary
                }
            });

            // SINKRONISASI 2: Jika berkas dihapus dari FilePond, kosongkan kembali nilai input teks asli
            pond.on('removefile', (err, file) => {
                textInput.value = "";
            });
        });
    }

    // =========================================================================
    // 3. INTEGRASI PREMIUM SELECT2 (IKON DEVICON + NAMA SKILL)
    // =========================================================================
    if (typeof $ !== "undefined" && $.fn.select2) {
        const $selectSkill = $('select[name="skills"]');

        if ($selectSkill.length > 0) {
            // Hancurkan render ID bawaan Flask-Admin terlebih dahulu agar tidak bentrok
            if ($selectSkill.hasClass("select2-hidden-accessible")) {
                $selectSkill.select2("destroy");
            }

            // Bangun ulang Select2 dengan format kustom berikon
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

    // =========================================================================
    // 4. INTEGRASI PREMIUM FLATPICKR DATEPICKER
    // =========================================================================
    const dateInput = document.querySelector('input[name="date"]');
    if (dateInput) {
        // Muat stylesheet CSS Flatpickr secara dinamis jika belum terpasang
        if (!document.getElementById("flatpickr-css")) {
            const link = document.createElement("link");
            link.id = "flatpickr-css";
            link.rel = "stylesheet";
            link.href = "https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css";
            document.head.appendChild(link);
        }

        // Muat pustaka JS Flatpickr secara dinamis jika belum ada
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
    const isCreateMode = !element.value;

    flatpickr(element, {
        dateFormat: "Y-m-d", // Format data asli yang dikirim ke database
        altInput: true,      // Mengaktifkan kolom samaran tampilan ramah pengguna
        altFormat: "j F Y",  // Tampilan tanggal lokal (contoh: 15 Mei 2026)
        allowInput: true,
        defaultDate: isCreateMode ? "today" : undefined, // Otomatis isi hari ini jika data baru
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

    // Regex memisahkan nama skill dan kelas ikonnya
    const regex = /(.*)\s\((devicon-.*|fa-.*)\)/;
    const match = state.text.match(regex);

    if (match) {
        const skillName = match[1];
        const iconClass = match[2]; // SOLUSI: Deklarasikan variabel iconClass secara eksplisit!
        return `<span><i class="${iconClass} colored mr-2" style="font-size: 1.25rem; display: inline-block; vertical-align: middle;"></i> ${skillName}</span>`;
    }

    return state.text;
}
