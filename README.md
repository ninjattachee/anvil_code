# Anvil Code

**Anvil Code** is a simple toy code agent powered by OpenRouter.

## Install

### From a checkout

```sh
uv tool install .
```

### From a built distribution

```sh
uv build
uv tool install dist/anvil_code-0.1.0-py3-none-any.whl
```

For development, run `uv sync` and then `uv run anvil-code "describe the change to make"`.

## Configure and run

Create a `.env` file (or export the environment variable) with your OpenRouter key:

```sh
OPENROUTER_API_KEY=your_key_here
```

Then run the installed command from the directory you want the agent to work in:

```sh
anvil-code "add tests for the calculator" --verbose
```

The agent scopes its file tools to the directory where `anvil-code` is invoked.

## Publish to PyPI

1. Confirm that `anvil-code` is available on PyPI, then update the version in `pyproject.toml`.
2. Build the wheel and source distribution with `uv build`.
3. Validate the artifacts with `uv run twine check dist/*`.
4. Upload using a PyPI API token: `uv publish`.

Once published, users can install it globally with `uv tool install anvil-code`.
