# Contributing to No-Harm-Local

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Ways to Contribute

- 🐛 **Bug Reports**: Report issues you encounter
- ✨ **Feature Requests**: Suggest new features or improvements
- 📝 **Documentation**: Improve docs, add examples
- 🔧 **Code**: Fix bugs, implement features
- 🧪 **Testing**: Add test cases, improve coverage

## Getting Started

### 1. Fork and Clone

```bash
git fork https://github.com/antoniopuertas/no-harm-local.git
git clone https://github.com/yourfork/no-harm-local.git
cd no-harm-local
```

### 2. Set Up Development Environment

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

## Development Guidelines

### Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and small

**Format code before committing:**

```bash
black src/ scripts/
flake8 src/ scripts/
mypy src/
```

### Testing

Add tests for new features:

```bash
pytest tests/
```

Aim for >80% code coverage:

```bash
pytest --cov=src tests/
```

### Documentation

- Update README.md if adding features
- Add docstrings to new functions
- Update relevant docs in `docs/`
- Include usage examples

## Pull Request Process

### 1. Before Submitting

- [ ] Code follows style guidelines
- [ ] Tests pass: `pytest tests/`
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Commit messages are clear

### 2. Commit Messages

Use conventional commits:

```
feat: add support for new dataset
fix: correct dimension score calculation
docs: update quickstart guide
test: add tests for jury scorer
```

### 3. Submit PR

- Provide clear description
- Reference related issues
- Include screenshots if UI changes
- Request review from maintainers

### 4. Review Process

- Maintainers will review within 1-2 weeks
- Address feedback
- Once approved, maintainers will merge

## Adding New Features

### Adding a New Dataset

1. Create loader in `src/data/dataset_loaders.py`
2. Add configuration in `config/jury_config.yaml`
3. Update `AVAILABLE_DATASETS` dict
4. Add tests in `tests/test_datasets.py`
5. Document in `docs/CUSTOM_DATASETS.md`

### Adding New Harm Dimensions

1. Update `harm_dimensions.py` registry
2. Update configuration
3. Update documentation
4. Add tests
5. Update report templates

### Adding New Jury Models

1. Test model with Ollama
2. Add to `config/jury_config.yaml`
3. Document model characteristics
4. Update setup script
5. Test full evaluation

## Code Review Checklist

- [ ] Code is well-documented
- [ ] Tests added and passing
- [ ] No breaking changes (or documented)
- [ ] Performance implications considered
- [ ] Security implications considered
- [ ] Accessible and inclusive

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on facts and technical merit
- Assume positive intent

## Questions?

- **Issues**: [GitHub Issues](https://github.com/antoniopuertas/no-harm-local/issues)
- **Discussions**: [GitHub Discussions](https://github.com/antoniopuertas/no-harm-local/discussions)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
