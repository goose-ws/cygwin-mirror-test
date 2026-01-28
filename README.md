# Cygwin Mirror Tester

A lightweight, containerized utility to find the fastest Cygwin mirrors for your location. It fetches the official mirror list, tests latency concurrently, and outputs a ranked table of the best candidates.

Output looks like:

<img width="564" height="461" alt="image" src="https://github.com/user-attachments/assets/1dcf7dc2-9630-4855-8124-296d726fa60f" />

## Usage

### Manual / Shell Usage (No Docker)

If you prefer to run the script directly on your host machine, you only need Python 3 installed. The script uses only the standard library, so no `pip install` is required.

**Requirements:**

* Python 3.6+

**Run:**

```bash
# Grab the script
wget "https://raw.githubusercontent.com/goose-ws/cygwin-mirror-test/refs/heads/main/cygwin_mirror_test.py"
chmod +x cygwin_mirror_test.py

# Run the script
python3 cygwin_mirror_test.py

# Optional arguments
python3 cygwin_mirror_test.py --workers 50 --timeout 1.0

```

### Docker
You can run the latest version immediately:

```bash
docker run --rm ghcr.io/goose-ws/cygwin-mirror-test:latest

```

### Advanced Options (Docker)

You can pass arguments directly to the container to adjust concurrency or timeouts:

```bash
# Run with 50 threads for faster results
docker run --rm ghcr.io/goose-ws/cygwin-mirror-test:latest --workers 50

# Set a stricter timeout (e.g., 0.5 seconds)
docker run --rm ghcr.io/goose-ws/cygwin-mirror-test:latest --timeout 0.5

```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.