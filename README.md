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
```bash
make start
```

### `make stop`

Stops and removes Docker containers. Automatically creates a database dump before stopping.
```bash
make stop
```

### `make permissions`

Configures permissions for the `./prestashop` directory:
- Changes ownership to `www-data` (uid:gid 33:33)
- Sets permissions to 775 (rwxrwxr-x)
- Checks if the current user is in the `www-data` group
- If not, adds the user to the `www-data` group
```bash
make permissions
```

**Note:** After adding the user to the group, you may need to log out and log back in for the changes to take effect.

### `make dump`

Creates a MySQL database dump to the `new_dump.sql` file in the project root directory.
```bash
make dump
```

## Example Workflow

1. Start the environment:
```bash
   make start
```

2. If you encounter file permission issues:
```bash
   make permissions
```

3. Stop the environment (automatically creates a backup):
```bash
   make stop
```

## Project Structure
```
.
├── .env                    # Environment variables
├── Makefile               # This file
├── prestashop/            # PrestaShop files directory
├── new_dump.sql           # Database dump (generated)
└── docker-compose.yml     # Docker Compose configuration
```

## Notes

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