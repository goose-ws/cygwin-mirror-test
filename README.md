# Cygwin Mirror Tester

A lightweight, containerized utility to find the fastest Cygwin mirrors for your location. It fetches the official mirror list, tests latency concurrently, and outputs a ranked table of the best candidates.

## Usage

### Quick Start (Recommended)
You can run the latest version immediately:

```bash
docker run --rm ghcr.io/goose-ws/cygwin-mirror-test:latest

```

### Advanced Options

You can pass arguments directly to the container to adjust concurrency or timeouts:

```bash
# Run with 50 threads for faster results
docker run --rm ghcr.io/goose-ws/cygwin-mirror-test:latest --workers 50

# Set a stricter timeout (e.g., 0.5 seconds)
docker run --rm ghcr.io/goose-ws/cygwin-mirror-test:latest --timeout 0.5

```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.