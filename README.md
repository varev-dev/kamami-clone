# E-Business Project: Kamami.pl Clone

## 1. Project Description
This project is a fully functional e-commerce store based on **PrestaShop 1.7.8**, developed as part of the E-Business course. The store is a clone of *Kamami.pl* and is populated with data automatically scraped from the source site.

The system runs in a Dockerized environment, featuring a custom theme, Polish payment/shipping methods, and automated testing scripts.

## 2. Team Composition
The project was developed using Git flow (Feature Branches, Pull Requests, Issues).

* **Dawid Wołoszyn** - *Back-End, DevOps*
* **Patryk Przybysz** - *Front-End, Automation Testing*
* **Kacper Doga** - *Scraping, Data Processing*

## 3. Project Structure
The repository follows a strict structure as required:

```text
.
├── config/                 # Configuration files (Docker, SSL, env)
│   ├── .env                # Environment variables
│   ├── docker-compose.yml  # Container orchestration
│   ├── Dockerfile          # Custom PrestaShop image build
│   └── ssl/                # Self-signed certificates
├── data/                   # Scraped data & Backup
│   ├── categories.json     # Scraped categories
│   ├── products_all.json   # Scraped products with attributes/images
│   └── dump.sql            # Full database backup (Settings Export)
├── importer/               # API Importer source code
├── scraper/                # Scraper source code
├── sources/                # Store source code
├── tests/                  # Selenium automation scripts
├── makefile                # Project management commands
├── MAKEFILE.md             # Development Env Makefile documentation
├── TOOLS.md                # Scraper & Importer documentattion
└── README.md               # Project documentation
```

## 4. Prerequisites

* **OS:** Linux/Unix (or WSL2 for Windows)
* **Docker** & **Docker Compose**
* **Python 3.x** (for tools)

## 5. Quick Start Workflow

1. **Generate SSL Certificates:** Required for HTTPS (self-signed).
```bash
make gen-key
```

2. **Start the Environment:** Builds images and starts PrestaShop + MySQL in the background.
```bash
make start
```

3. **Fix Permissions (if needed):** Run this if images are missing or you encounter write errors.
```bash
make permissions
```

4. **Run E2E Tests:** Executes automated Selenium tests (requires venv setup in `tests/`)
```bash
make test
```

5. **Stop & Backup:** Stops containers and automatically exports the database settings to `data/dump.sql`
```bash
make stop
```

More about available commands, and usage available here: [MAKEFILE.md](MAKEFILE.md)
Detailed description on how to use scraper and importer: [TOOLS.md](TOOLS.md)
For detailed test documentation: [tests/README.md](tests/README.md) 