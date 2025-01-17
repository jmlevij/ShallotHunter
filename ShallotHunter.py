import requests
import base64
import hashlib
from nacl.signing import SigningKey
from nacl.encoding import RawEncoder
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import threading

# Configure Tor to route traffic through the Tor network
def get_tor_session():
    session = requests.session()
    session.proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050',
    }
    return session

# Generate an Onion v3 address
def generate_onion_v3_address():
    # Generate a random 32-byte Ed25519 private key
    signing_key = SigningKey.generate()
    
    # Extract the public key from the signing key
    public_key = signing_key.verify_key.encode(RawEncoder)

    # Compute the checksum
    onion_prefix = b".onion checksum"
    checksum = hashlib.sha3_256(onion_prefix + public_key + b"\x03").digest()[:2]

    # Create the Onion address
    onion_address = base64.b32encode(public_key + checksum + b"\x03").decode('utf-8').lower()
    return onion_address

# Fetch new .onion URLs from a known dark web index or generated address
def fetch_onion_site(onion_url):
    session = get_tor_session()
    try:
        response = session.get(f"http://{onion_url}.onion", timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching data from {onion_url}.onion: {e}")
        return None

# Extract .onion URLs from the page content
def extract_onion_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = set()
    for a_tag in soup.find_all('a', href=True):
        if ".onion" in a_tag['href']:
            links.add(a_tag['href'])
    return links

# Thread-safe counter
total_success = threading.Lock()
success_count = 0

def verify_known_url():
    known_onion_url = "juhanurmihxlp77nkq76byazcldy2hlmovfu2epvl5ankdibsot4csyd"  # Ahmia's onion URL
    print(f"[*] Verifying known Onion URL: {known_onion_url}.onion...")
    html_content = fetch_onion_site(known_onion_url)
    if html_content:
        print(f"[+] Successfully accessed known URL: {known_onion_url}.onion")
        return True
    else:
        print(f"[-] Failed to access known URL: {known_onion_url}.onion")
        return False

def worker(attempt_number):
    global success_count
    try:
        print(f"[*] Attempt {attempt_number}/100: Generating Onion v3 address...")
        onion_address = generate_onion_v3_address()
        print(f"[+] Generated Onion v3 address: {onion_address}.onion")

        print(f"[*] Attempting to fetch content from {onion_address}.onion...")
        html_content = fetch_onion_site(onion_address)
        if html_content:
            with total_success:
                success_count += 1
            print(f"[+] Successfully accessed {onion_address}.onion")
            print("[*] Extracting links...")
            onion_links = extract_onion_links(html_content)
            print(f"[*] Found {len(onion_links)} links:")
            for link in onion_links:
                print(link)
        else:
            print(f"[-] Failed to access {onion_address}.onion")
    except Exception as e:
        print(f"[!] An error occurred in attempt {attempt_number}: {e}")

# Main logic
def main():
    # Test connectivity to TOR. If there is no connectivity, stop the script.
    print("[*] Verifying access to the Tor network using a known URL...")
    verify_known_url()
    if not verify_known_url(): 
        return

    print("[*] Starting the process to generate and test 1000 Onion v3 addresses with multithreading...")
    max_threads = 10  # Limit the number of concurrent threads

    with ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(worker, i + 1) for i in range(1000)]

        # Wait for all threads to complete
        for future in futures:
            future.result()

    print(f"[*] Process completed. Total successful accesses: {success_count}/1000")

if __name__ == "__main__":
    main()
