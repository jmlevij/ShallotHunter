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
   git clone https://github.com/your-username/ShallotHunter.git
   cd ShallotHunter

2. Install the required Python packages:
   pip install -r requirements.txt

3. Start the Tor service:
   sudo service tor start

   <img width="1273" alt="ShallotHunter" src="https://github.com/user-attachments/assets/73d17d8b-7eb4-4162-98c8-67d9932bf07b" />


   
