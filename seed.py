import os
import json
from datetime import date  # 1. TAMBAHKAN IMPORT INI
from main import create_app
from model.models import (
    db,
    NavItem,
    Skill,
    Social,
    Equipment,
    Experience,
    Category,  # 2. TAMBAHKAN IMPORT INI
    Article,
    Project,
)


def seed_database():
    app = create_app()
    with app.app_context():
        print("🚀 Memulai proses seeding data dengan skema kategori dinamis...")

        # 1. Reset Database: Drop all dan buat ulang dengan skema baru
        db.drop_all()
        db.create_all()
        print("🧹 Database lama dibersihkan. Tabel baru telah berhasil dibuat.")

        # 2. Seed Navigation Items
        nav_data = [
            {"name": "About", "url": "/", "icon": "fa-user"},
            {"name": "Resume", "url": "/resume", "icon": "fa-file-lines"},
            {"name": "Articles", "url": "/articles", "icon": "fa-book-open"},
            {"name": "Projects", "url": "/projects", "icon": "fa-layer-group"},
        ]
        for nav in nav_data:
            db.session.add(NavItem(name=nav["name"], url=nav["url"], icon=nav["icon"]))
        print("🔗 Data Navigation disiapkan.")

        # 3. Seed Social Media
        social_data = [
            {
                "name": "Github",
                "link": "https://github.com/Liiaa-chan",
                "icon": "fa-brands fa-github",
            },
            {
                "name": "LinkedIn",
                "link": "https://www.linkedin.com/in/dian-wicaksono",
                "icon": "fa-brands fa-linkedin-in",
            },
            {
                "name": "Instagram",
                "link": "https://www.instagram.com/dian_wicaksono9",
                "icon": "fa-brands fa-instagram",
            },
        ]
        for soc in social_data:
            db.session.add(Social(name=soc["name"], link=soc["link"], icon=soc["icon"]))
        print("📱 Data Social Media disiapkan.")

        # 4. Seed Skills (Devicon Integration)
        skills_data = [
            ("HTML", "devicon-html5-plain"),
            ("CSS", "devicon-css3-plain"),
            ("Javascript", "devicon-javascript-plain"),
            ("Bootstrap", "devicon-bootstrap-plain"),
            ("Tailwindcss", "devicon-tailwindcss-original"),
            ("PHP", "devicon-php-plain"),
            ("Laravel", "devicon-laravel-original"),
            ("Filament", "devicon-filamentphp-original"),
            ("Python", "devicon-python-plain"),
            ("Flask", "devicon-flask-original"),
            ("C", "devicon-c-original"),
            ("Arduino", "devicon-arduino-plain"),
            ("Linux", "devicon-linux-plain"),
            ("Raspberry Pi", "devicon-raspberrypi-plain"),
            ("Vim", "devicon-vim-plain"),
            ("Git", "devicon-git-plain"),
            ("Github", "devicon-github-original"),
            ("Github Actions", "devicon-githubactions-plain"),
            ("Filezila", "devicon-filezilla-plain"),
            ("Cloudflare", "devicon-cloudflare-plain"),
            ("Postman", "devicon-postman-plain"),
            ("Figma", "devicon-figma-plain"),
        ]

        skill_objects = {}
        for name, icon in skills_data:
            skill = Skill(name=name, icon=icon)
            db.session.add(skill)
            skill_objects[name] = skill
        print("🛠️ Data Skills (22 item) disiapkan.")

        # 5. Seed Equipment
        equipment_data = [
            {
                "type": "software",
                "category": "Code Editor / Text Editor",
                "name": "Visual Studio Code",
                "data_list": '["Visual Studio Code", "Arduino IDE", "Nano", "Vim"]',
            },
            {
                "type": "software",
                "category": "Terminal",
                "name": "Windows Terminal",
                "data_list": '["Windows Terminal", "oh-my-posh", "Termux", "Linux Terminal"]',
            },
            {
                "type": "software",
                "category": "Design",
                "name": "Figma",
                "data_list": '["Figma", "Whimsical"]',
            },
            {
                "type": "hardware",
                "category": "Laptop",
                "name": "Advan Workmate",
                "data_list": '["AMD Ryzen 5 3500U", "AMD Radeon RX Vega 8 Graphics", "8GB DDR4 RAM", "256GB SSD NVME M.2", "14 Inch IPS, Resolution WUXGA (1920x1200)"]',
            },
            {
                "type": "hardware",
                "category": "Peripherals",
                "name": "Setup",
                "data_list": '["Keyboard: Unitech MXI", "Mouse: Philips Wire Standar", "TWS: Lenovo EA230"]',
            },
        ]
        for eq in equipment_data:
            db.session.add(
                Equipment(
                    type=eq["type"],
                    category=eq["category"],
                    name=eq["name"],
                    data_list=eq["data_list"],
                )
            )
        print("💻 Data Equipment disiapkan.")

        # 6. Seed Experience
        experiences_data = [
            {
                "title": "Lead Front-end Engineer",
                "company": "Propbar",
                "location": "🇬🇧 United Kingdom",
                "work_type": "Full-Time",
                "duration": "Mar 2023 - Present",
                "description": "Led the front-end work from the project inception, establishing architectural patterns using Next.js and TypeScript.|Maintained a complex browser extension, widget, and web application as a unified monorepo structure.|Architected a highly complex real-estate map service with high-performance rendering capabilities.|Implemented a sophisticated data grid for property comparables with advanced filtering and sorting.",
            },
            {
                "title": "Senior Front-end Engineer",
                "company": "LolaDB",
                "location": "🇺🇸 United States",
                "work_type": "Contract",
                "duration": "Jun 2022 - Feb 2023",
                "description": "Solved complex performance problems using the latest Web Standards and optimization techniques.|Architected the product's core front-end structure for scalability and maintainability.|Accomplished the development of a sophisticated UI component library used across multiple projects.",
            },
        ]
        for exp in experiences_data:
            db.session.add(
                Experience(
                    title=exp["title"],
                    company=exp["company"],
                    location=exp["location"],
                    work_type=exp["work_type"],
                    duration=exp["duration"],
                    description=exp["description"],
                )
            )
        print("💼 Data Work Experience disiapkan.")

        # 7. Seed Articles (Perbaikan Nilai Objek Tanggal Asli)
        articles_data = [
            {
                "title": "Membangun Kebiasaan Menulis di Sela Debugging",
                "description": "Bagaimana menulis 15 menit sehari bisa menjernihkan pikiran developer dari kerumitan logika program yang berat.",
                "categories": "Personal, Reflections",
                "date": date(2026, 5, 15),  # Diubah menjadi objek date asli
                "image_url": "https://images.unsplash.com/photo-1499750310107-5fef28a66643?q=80&w=800",
                "content": "<p>Menulis adalah terapi terbaik bagi seorang software engineer...</p>",
                "skills_needed": [],
            }
        ]
        for art_info in articles_data:
            article = Article(
                title=art_info["title"],
                description=art_info["description"],
                date=art_info["date"],
                image_url=art_info["image_url"],
                content=art_info["content"],
            )
            article.generate_slug()

            # PARSING OTOMATIS: Mengubah string kategori menjadi entitas relasi tabel tunggal
            if art_info["categories"]:
                names = [c.strip() for c in art_info["categories"].split(",")]
                for cat_name in names:
                    category = Category.query.filter_by(
                        name=cat_name, kode_kategori="article"
                    ).first()
                    if not category:
                        category = Category(name=cat_name, kode_kategori="article")
                        db.session.add(category)
                    article.categories.append(category)

            for skill_name in art_info["skills_needed"]:
                if skill_name in skill_objects:
                    article.skills.append(skill_objects[skill_name])
            db.session.add(article)
        print("📝 Data Articles disiapkan.")

        # 8. Seed Projects (Perbaikan Nilai Objek Tanggal Asli)
        projects_data = [
            {
                "title": "Sistem Produksi Pakan Otomatis",
                "description": "Aplikasi manajemen inventori bahan baku, kalkulasi komposisi campuran formula pakan, dan pelacakan stok real-time.",
                "date": date(2026, 5, 12),  # Diubah menjadi objek date asli
                "image_url": "https://images.unsplash.com/photo-1595246140625-573b715d11dc?q=80&w=800",
                "github_link": "https://github.com/Liiaa-chan/produksi-pakan",
                "demo_link": "https://pakan.heliostech.my.id",
                "categories": "Software, Internet of Things",
                "content": "<h3>Deskripsi Teknis</h3><p>Sistem ini dirancang untuk menangani kompleksitas pencatatan bahan baku pakan ternak.</p>",
                "tech_stack": ["PHP", "Laravel", "Filament", "Tailwindcss"],
            },
            {
                "title": "Wood Price Management System",
                "description": "Sistem log audit perubahan harga kayu dan manajemen otorisasi persetujuan (approval) multi-user.",
                "date": date(2026, 4, 1),  # Diubah menjadi objek date asli
                "image_url": "https://images.unsplash.com/photo-1520052205664-74d2766adef3?q=80&w=800",
                "github_link": "https://github.com/Liiaa-chan/wood-price-audit",
                "demo_link": "",
                "categories": "Web App, Security",
                "content": "<h3>Sistem Keamanan Harga</h3><p>Proyek ini fokus pada transparansi riwayat data harga kayu olahan.</p>",
                "tech_stack": ["PHP", "Laravel", "Filament"],
            },
            {
                "title": "Helios Portfolio Control Hub",
                "description": "Dashboard portfolio personal interaktif berbasis web dengan tema cyborg dark mode terintegrasi panel admin.",
                "date": date(2026, 2, 15),  # Diubah menjadi objek date asli
                "image_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?q=80&w=800",
                "github_link": "https://github.com/Liiaa-chan/helios-portfolio",
                "demo_link": "https://heliostech.my.id",
                "categories": "Web App, Frontend, Portfolio",
                "content": "<h3>Boilerplate Portofolio Minimalis</h3><p>Membangun sistem portofolio modular menggunakan micro-framework Flask Python.</p>",
                "tech_stack": ["Python", "Flask", "Tailwindcss", "HTML", "CSS"],
            },
        ]

        for proj_info in projects_data:
            project = Project(
                title=proj_info["title"],
                description=proj_info["description"],
                date=proj_info["date"],
                image_url=proj_info["image_url"],
                github_link=proj_info["github_link"],
                demo_link=proj_info["demo_link"],
                content=proj_info["content"],
            )
            project.generate_slug()

            # PARSING OTOMATIS: Mengubah string kategori menjadi entitas relasi tabel tunggal
            if proj_info["categories"]:
                names = [c.strip() for c in proj_info["categories"].split(",")]
                for cat_name in names:
                    category = Category.query.filter_by(
                        name=cat_name, kode_kategori="project"
                    ).first()
                    if not category:
                        category = Category(name=cat_name, kode_kategori="project")
                        db.session.add(category)
                    project.categories.append(category)

            for skill_name in proj_info["tech_stack"]:
                if skill_name in skill_objects:
                    project.skills.append(skill_objects[skill_name])

            db.session.add(project)

        print("🏗️ Data Projects disiapkan bersama data kategori ganda.")

        # 9. Jalankan Commit Akhir
        db.session.commit()
        print("\n✨ SEEDING BERHASIL! Database telah berhasil diredesain dan diisi.")


if __name__ == "__main__":
    seed_database()
