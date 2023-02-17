# Build poetrybot.
build:
    @poetry build

# Remove build artifacts.
clean:
    @rm -rf dist/

# Run tests.
test:
    @poetry run pytest

# poetry run ...
run +ARGS:
    @poetry run {{ARGS}}

# Set version in both package and pyproject.toml.
set-version version:
    @echo 'Setting version to {{version}}…'
    @sed -i 's/version = ".*"/version = "{{version}}"/' pyproject.toml
    @sed -i 's/__version__ = ".*"/__version__ = "{{version}}"/' src/poetrybot/__init__.py
