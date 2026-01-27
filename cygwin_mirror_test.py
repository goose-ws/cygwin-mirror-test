#!/usr/bin/env python3
import urllib.request
import urllib.error
import time
import concurrent.futures
import argparse
import sys
import shutil

# --- Configuration ---
MIRROR_LIST_URL = "https://cygwin.com/mirrors.lst"
# A user agent is polite and prevents some servers from blocking the request
USER_AGENT = "CygwinMirrorTester/3.0"

def log(message):
    """Prints a timestamped log message."""
    timestamp = time.strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_mirror_list():
    """Fetches and parses the mirror list."""
    log(f"Contacting {MIRROR_LIST_URL}...")
    
    try:
        req = urllib.request.Request(
            MIRROR_LIST_URL, 
            headers={'User-Agent': USER_AGENT}
        )
        with urllib.request.urlopen(req) as response:
            data = response.read().decode('utf-8')
    except Exception as e:
        log(f"CRITICAL ERROR: Could not download mirror list. {e}")
        sys.exit(1)

    log("Parsing mirror list...")
    mirrors = []
    for line in data.splitlines():
        # Cygwin list format: URL;Region;Country;...
        parts = line.split(';')
        if not parts or line.strip().startswith('#'):
            continue
        
        url = parts[0]
        # Filter for http/https only
        if url.startswith(("http:", "https:")):
            mirrors.append(url)
            
    log(f"Successfully identified {len(mirrors)} valid HTTP/HTTPS mirrors.")
    return mirrors

def test_mirror(url, timeout):
    """
    Tests a single mirror's latency.
    Returns: (latency_in_seconds, url) or (None, url) on failure.
    """
    # We test availability of a specific small file to ensure the mirror isn't broken
    target_url = f"{url.rstrip('/')}/x86_64/setup.ini"
    start_time = time.time()
    
    try:
        req = urllib.request.Request(
            target_url, 
            method='HEAD', 
            headers={'User-Agent': USER_AGENT}
        )
        with urllib.request.urlopen(req, timeout=timeout) as _:
            pass
        
        elapsed = time.time() - start_time
        return (elapsed, url)
        
    except Exception:
        return (None, url)

def print_progress(done, total):
    """Draws a simple inline progress bar."""
    bar_len = 30
    percent = done / total
    filled = int(bar_len * percent)
    bar = "=" * filled + "-" * (bar_len - filled)
    
    sys.stdout.write(f"\rProgress: [{bar}] {int(percent * 100)}% ({done}/{total})")
    sys.stdout.flush()

def main():
    parser = argparse.ArgumentParser(description="Programmatic Cygwin Mirror Tester")
    parser.add_argument("--workers", type=int, default=20, help="Number of concurrent threads")
    parser.add_argument("--timeout", type=float, default=2.0, help="Socket timeout in seconds")
    args = parser.parse_args()

    # 1. Get List
    mirrors = get_mirror_list()

    # 2. Prepare for Testing
    log(f"Initializing {args.workers} worker threads with {args.timeout}s timeout.")
    log("Starting latency tests...")

    results = []
    total = len(mirrors)
    
    # 3. Execute concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_url = {executor.submit(test_mirror, url, args.timeout): url for url in mirrors}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_url)):
            elapsed, url = future.result()
            if elapsed:
                results.append((elapsed, url))
            
            # Update progress bar
            print_progress(i + 1, total)

    print("") # Newline to clear the progress bar
    log(f"Testing complete. {len(results)} mirrors responded out of {total}.")

    # 4. Sort and Display
    results.sort(key=lambda x: x[0])
    
    print("\n" + "="*80)
    print(f"{'RANK':<4} | {'LATENCY':<10} | {'MIRROR URL'}")
    print("="*80)
    
    for rank, (elapsed, url) in enumerate(results[:20], 1):
        # Green color for top 5, standard for rest
        color = "\033[92m" if rank <= 5 else "\033[0m"
        print(f"{color}{rank:<4} | {elapsed:.4f}s    | {url}\033[0m")
    
    print("="*80 + "\n")

if __name__ == "__main__":
    main()