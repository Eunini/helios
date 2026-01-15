# Contributing to Helios

Thank you for your interest in contributing to Helios! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on code quality and user experience
- Report issues responsibly

## Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/yourusername/helios.git
cd helios
```

### 2. Setup Development Environment

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**

```bash
cd frontend
npm install
```

### 3. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or for fixes
git checkout -b fix/your-fix-name
```

## Development Workflow

### Code Style

**Backend (Python)**

- Use Black for formatting
- Use Ruff for linting
- Type hints required
- Docstrings for all functions

```bash
# Format
black .

# Lint
ruff check .

# Fix automatically
ruff check . --fix
```

**Frontend (TypeScript/React)**

- Use ESLint
- Use Prettier
- No `any` types
- Prop types required

```bash
# Check
npm run lint

# Format
npm run format
```

### Testing

**Backend:**

```bash
cd backend
pytest                    # Run all tests
pytest tests/test_agents.py  # Run specific test
pytest --cov=.           # With coverage
```

**Frontend:**

```bash
cd frontend
npm run test              # Run tests (when implemented)
```

### Code Review Checklist

Before submitting PR, verify:

- [ ] Code is formatted (Black/Prettier)
- [ ] Linting passes (Ruff/ESLint)
- [ ] Tests pass
- [ ] Test coverage maintained
- [ ] Types are correct (TypeScript/Pydantic)
- [ ] No console.log/print statements (except logging)
- [ ] Documentation updated
- [ ] Commit messages are clear

## Pull Request Process

### 1. Prepare Your Changes

```bash
# Ensure branch is up to date
git fetch origin
git rebase origin/main

# Run tests
pytest  # Backend
npm run test  # Frontend

# Format code
black .  # Backend
npm run format  # Frontend
```

### 2. Commit Messages

Format:

```
type(scope): brief description

Longer description if needed.
- Bullet points for changes
- Reference issues: Closes #123

Co-authored-by: Name <email>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

Example:

```
feat(agents): add context window management

- Implement sliding window for token limit
- Add token counting utility
- Update PlannerAgent to use new window
- Add tests for window behavior

Closes #45
```

### 3. Create Pull Request

```bash
git push origin feature/your-feature-name
```

Create PR on GitHub with:

- Clear title (use conventional commits format)
- Description of changes
- Screenshots for UI changes
- Reference related issues

### 4. Respond to Review

- Address feedback promptly
- Push new commits (don't force push)
- Request re-review when ready

## Areas to Contribute

### Backend

- [ ] Agent implementations (prompt engineering, context management)
- [ ] Database optimizations and migrations
- [ ] API endpoints enhancements
- [ ] Test coverage expansion
- [ ] Documentation

### Frontend

- [ ] Complete stub pages (Inventory, Customers, Staff, Insights)
- [ ] Add charts and visualizations
- [ ] Implement dark mode
- [ ] Mobile responsiveness
- [ ] Performance optimizations

### DevOps

- [ ] Kubernetes deployment files
- [ ] Monitoring and alerting setup
- [ ] Database backup automation
- [ ] Performance benchmarks

### Documentation

- [ ] API documentation
- [ ] Deployment guides
- [ ] Architecture diagrams
- [ ] Tutorial videos
- [ ] Blog posts

## Commit Guidelines

Good commit message:

```
feat(inventory): add low stock alerts

- Implement threshold checking in InventoryService
- Add alert notification to CommunicationsAgent
- Update product schema with alert_threshold field
- Add tests for threshold logic

This allows businesses to receive notifications
when inventory falls below critical levels.

Closes #234
```

Bad commit message:

```
fixed stuff
update code
```

## Testing Guidelines

### Backend Tests

```python
def test_agent_functionality():
    """Test that agent executes task correctly."""
    agent = SomeAgent()
    result = agent.execute("task description")
    assert result.status == "success"
    assert result.data is not None
```

### Frontend Tests (when implemented)

```typescript
describe("ChatInterface", () => {
  it("should submit message on button click", () => {
    // Test implementation
  });
});
```

## Documentation

### Python Docstrings

```python
def create_product(name: str, price: float) -> Product:
    """Create a new product with given details.

    Args:
        name: Product name
        price: Product price in Naira

    Returns:
        Created Product object

    Raises:
        ValueError: If price is negative

    Example:
        >>> product = create_product("Coke", 100)
        >>> product.name
        'Coke'
    """
```

### TypeScript Comments

```typescript
/**
 * Formats currency value for display.
 * @param amount - Numeric amount in Naira
 * @returns Formatted string with ₦ symbol
 * @example
 * formatCurrency(5000) // "₦5,000.00"
 */
export function formatCurrency(amount: number): string {
```

## Common Issues

### Python Import Errors

```bash
# Reinstall in development mode
pip install -e .

# Check PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:/path/to/backend"
```

### Node Module Issues

```bash
# Clean install
rm -rf node_modules package-lock.json
npm install
```

### Database Issues

```bash
# Reset database
rm backend/helios.db
python -c "from core import init_db; init_db()"
```

## Performance Guidelines

### Backend

- Avoid N+1 queries (use joins)
- Cache frequently accessed data
- Implement pagination for lists
- Use indexes on foreign keys

### Frontend

- Code split large components
- Lazy load images
- Minimize bundle size
- Use React.memo for expensive components

## Security Guidelines

- Never commit secrets or API keys
- Use environment variables for configuration
- Validate user input (Pydantic, TypeScript)
- Use parameterized queries (SQLAlchemy handles this)
- Follow OWASP guidelines

## Release Process

1. Update version in package.json/setup.py
2. Update CHANGELOG.md
3. Create git tag
4. Push to GitHub
5. GitHub Actions deploys automatically

## Questions?

- Check existing issues and discussions
- Read the main README.md
- Check API documentation
- Create a discussion thread

## Recognition

Contributors are recognized in:

- CONTRIBUTORS.md file
- GitHub contributors page
- Release notes

---

**Thank you for contributing to Helios!**

Questions? Create an issue or discussion.
