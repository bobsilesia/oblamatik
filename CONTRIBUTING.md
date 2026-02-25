# Contributing to Oblamatik

We are glad you want to help develop the Oblamatik integration! Below are some guidelines to facilitate our collaboration.

## Bug Reporting

If you found a bug, please report it in the [Issues](https://github.com/bobsilesia/oblamatik/issues) tab using the prepared "Bug Report" template. Remember to attach logs and steps to reproduce the error.

## Proposing Changes (Pull Requests)

1. **Fork**: Fork the repository and create a new branch for your change (`git checkout -b feature/my-change`).
2. **Code Standards**: We adhere to strict code quality standards.
   - We use `ruff` for linting and formatting.
   - We use `mypy` for type checking.
   - Code must be fully asynchronous (`async`/`await`).
3. **Local Testing**: Before submitting changes, run:
   ```bash
   ruff format custom_components/oblamatik
   ruff check custom_components/oblamatik
   mypy custom_components/oblamatik
   ```
4. **Commit Changes**: Describe your changes in the commit message clearly and concisely.
5. **Pull Request**: Submit a PR to the main branch (`main`). Describe what your code changes and why.

## Development Environment

We recommend using `uv` or `venv` to manage dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install homeassistant ruff mypy
```

## Project Structure

- `custom_components/oblamatik/` - Main integration code.
- `.github/workflows/` - CI/CD configuration.

Thank you for your contribution!
