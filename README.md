# ShallotHunter

This Python script generates Onion v3 addresses and attempts to fetch content from them using the Tor network. It is designed for educational and research purposes to validate Onion service availability.

## Features
- Generates Onion v3 addresses.
- Validates access to a known `.onion` URL (e.g., Ahmia's onion service) to ensure Tor connectivity.
- Attempts to fetch content from generated addresses.
- Extracts and prints `.onion` links from any accessible pages.
- Multithreaded to handle multiple requests efficiently.

## Requirements
- Python 3.7 or later
- Tor service running on the local machine
- Libraries:
  - `requests[socks]`
  - `pynacl`
  - `beautifulsoup4`

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/onion-v3-validator.git
   cd onion-v3-validator
