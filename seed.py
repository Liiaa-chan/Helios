import os
from main import create_app
from model import db, NavItem, Skill, Social, Equipment


def seed_database():
    app = create_app()
    with app.app_context():
        print("🚀 Memulai proses seeding data terbaru untuk Helios...")

        # 1. Bersihkan Data Lama
        db.drop_all()
        db.create_all()
        print("🧹 Database dibersihkan dan tabel baru disiapkan.")

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
        for name, icon in skills_data:
            db.session.add(Skill(name=name, icon=icon))  # Default color
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

        # Simpan Perubahan
        db.session.commit()
        print(
            "\n✨ Seeding selesai! Database Helios kini berisi data navigasi, skill, sosial, dan peralatan Anda."
        )


if __name__ == "__main__":
    seed_database()
