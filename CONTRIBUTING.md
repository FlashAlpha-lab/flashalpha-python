# Contributing

Thanks for your interest in contributing to the FlashAlpha Python SDK.

## Reporting Issues

Open an issue on [GitHub](https://github.com/FlashAlpha-lab/flashalpha-python/issues) with:
- Python version
- SDK version (`flashalpha.__version__`)
- Steps to reproduce
- Expected vs actual behavior

## Development Setup

```bash
git clone https://github.com/FlashAlpha-lab/flashalpha-python.git
cd flashalpha-python
pip install -e ".[dev]"
pytest tests/test_client.py -v
```

## Running Tests

Unit tests (no API key needed):
```bash
pytest tests/test_client.py -v
```

Integration tests (requires API key):
```bash
FLASHALPHA_API_KEY=your_key pytest tests/test_integration.py -m integration -v
```

## Pull Requests

1. Fork the repo
2. Create a branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a PR

## Code Style

- Type hints on all public methods
- Docstrings on all public methods
- Follow existing patterns in `client.py`
