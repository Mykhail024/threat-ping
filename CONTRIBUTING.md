# Contributing

## Commit Messages

This project follows [Conventional Commits](https://www.conventionalcommits.org/).

## Naming Conventions

### Files and Folders

- Use `snake_case` for all file and folder names
- No spaces, no Cyrillic characters
- Names must be descriptive: `ukraine_alerts.py`, not `ua.py`

### Python

- Class names: `PascalCase` — `class AlertProvider`
- Variables and functions: `snake_case` — `alert_region`, `def fetch_alerts()`
- Constants: `SCREAMING_SNAKE_CASE` — `POLL_INTERVAL = 5`
- Modules: `snake_case` — `alert_provider.py`, `notification_service.py`
