# epumpz

## Ollama install quickstart

If you want to run:

```bash
ollama run r1-1776:70b
```

install Ollama first.

### Linux/macOS (official installer)

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Then start the service and verify:

```bash
ollama serve
# in another shell
ollama --version
```

### Pull and run the model

```bash
ollama run r1-1776:70b
```

This command downloads the model on first run, then opens an interactive chat.

## Troubleshooting

- `command not found: ollama`: Ollama is not installed or not on `PATH`.
- `403` during download/install: your environment likely blocks outbound package downloads; retry on a network that allows access to `ollama.com` and GitHub releases.
- Out-of-memory errors with 70B models: use a smaller model or run with more RAM/VRAM.
