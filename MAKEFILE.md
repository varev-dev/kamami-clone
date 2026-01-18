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

```text
├── config/                 # Configuration files (Docker, SSL, env)
│   ├── .env                # Environment variables
│   ├── docker-compose.yml  # Container orchestration
│   ├── Dockerfile          # Custom PrestaShop image build
│   └── ssl/                # Self-signed certificates
├── data/                   # Scraped data & Backup
│   ├── categories.json     # Scraped categories (UTF-8)
│   ├── products_all.json   # Scraped products with attributes/images
│   └── dump.sql            # Full database backup (Settings Export)
├── importer/               # API Importer source code
├── scraper/                # Python To
├── sources/                # Store source code
├── tests/                  # Selenium automation scripts
├── makefile                # Project management commands
├── TOOLS.md                # Scraper & Importer documentation
└── README.md               # Project documentation
```

# PrestaShop Development Environment - Makefile

## Description

This Makefile simplifies the management of a Docker-based PrestaShop development environment. It automates common tasks such as starting containers, managing permissions, and creating database backups.

## Requirements

- Docker and Docker Compose
- `.env` file in the project root directory with variables from `example.env`
- Linux/Unix system

## Available Commands

### `make start`

Starts Docker containers in detached mode (in the background).

### `make stop`

Stops and removes Docker containers. Automatically creates a database dump before stopping.

### `make permissions`

Configures permissions for the `./prestashop` directory:
- Changes ownership to `www-data` (uid:gid 33:33)
- Sets permissions to 775 (rwxrwxr-x)
- Checks if the current user is in the `www-data` group
- If not, adds the user to the `www-data` group

**Note:** After adding the user to the group, you may need to log out and log back in for the changes to take effect.

### `make dump`

Creates a MySQL database dump to the `new_dump.sql` file in the project root directory.

### `make gen-key`

Creates SSL self-signed certificates in `ssl/certs` directory. Required for the website to work.

## Example Workflow

1. Generate certificates:
```bash
make gen-key
```

2. Start the environment:
```bash
   make start
```

3. If you encounter file permission issues:
```bash
   make permissions
```

4. Stop the environment (automatically creates a backup):
```bash
   make stop
```

## Project Structure
```
.
├── .env                   # Environment variables
├── Makefile               # Make targets
├── prestashop/            # PrestaShop files directory
├── new_dump.sql           # Database dump (generated)
├── docker-compose.yml     # Docker Compose configuration
├── dump.sql               # Dump that will be used on startup
├── tools/                 # Python scripts (scraper, REST API)
└── ssl/                   # SSL certificates and Apache config
```

## Notes

- SSL certificates have to be created before startup
- Database dump is automatically created with every `make stop` call
- The `permissions` command requires sudo privileges
- Dump is created with the `-x` option (lock tables), ensuring data consistency
- The MySQL container must be running to create a dump

## Troubleshooting

### "Permission denied" error when accessing PrestaShop files

Run `make permissions` to fix file permissions.

### Database dump fails with an error

Make sure that:
- The `prestashop-mysql` container is running
- The `MYSQL_ROOT_PASSWORD` variable in the `.env` file is correct
- The database name is `prestashop`

### ERR_CONNECTION_REFUSED in the browser

Make sure that SSL certificates are generated before startup.
