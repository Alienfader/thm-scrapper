README.txt
TryHackMe Scraper Tool
======================

Created by: Alienfader

Overview
--------
The TryHackMe Scraper Tool is designed to extract and convert the core content from TryHackMe room pages (or similar web pages) into well-organized Markdown files. This tool attaches to an existing, already‑logged‑in Google Chrome session (using remote debugging) so that you do not need to log in each time. Once attached, the tool navigates to the specified URLs, waits for dynamic content (including images) to load, filters out unwanted site-wide elements (like ads, headers, footers, navigation, etc.), and converts the page's core content into Markdown format. The resulting Markdown file is then saved using the last segment of the URL (e.g. "jwtsecurity.md").

Features
--------
- **Remote Session Attachment:**  
  Attach to an existing Chrome session running with remote debugging enabled so you can leverage your current logged‑in state.
  
- **Dynamic Content Loading:**  
  Waits for dynamic content (including lazy‑loaded images) to load properly before scraping.
  
- **Content Extraction & Conversion:**  
  Uses BeautifulSoup to filter out unwanted site-wide elements and extracts the core content. Converts text, headings, code blocks, and images into Markdown while preserving the original order.
  
- **Easy Output:**  
  Saves the extracted and formatted content into a Markdown file named after the URL’s last segment.

Prerequisites
-------------
1. **Python 3.x** installed on your system.
2. (Optional) A Python virtual environment for isolating dependencies.
3. **Google Chrome** installed.
4. **Chrome must be launched with remote debugging enabled** using your logged‑in profile.

Launching Chrome with Remote Debugging on Linux
-------------------------------------------------
Before running the script, you must start Chrome with remote debugging enabled. For example, on Linux, open a terminal and run:

    google-chrome --remote-debugging-port=9222 --user-data-dir="/home/yourusername/.config/google-chrome/Default"

Replace `/home/yourusername/.config/google-chrome/Default` with the path to your desired Chrome profile. This profile must already be logged in to TryHackMe (or the target site).

Installation
------------
1. **Clone or Download the Repository:**  
   Place the tool’s source code in your desired directory.

2. **Set Up a Virtual Environment (Optional but Recommended):**

       python3 -m venv .venv
       source .venv/bin/activate

3. **Install Required Python Packages:**

       pip install selenium beautifulsoup4 webdriver-manager

Usage
-----
Run the tool by providing one or more URLs as command-line arguments. For example:

    python3 newapproach.py https://tryhackme.com/room/jwtsecurity https://tryhackme.com/room/sessionmanagement

The tool will:
- Attach to your running Chrome instance (launched with remote debugging).
- Check that you are logged in (using your active session).
- Navigate to each provided URL.
- Scrape the page's core content.
- Convert the content into Markdown.
- Save each output as a Markdown file (e.g., "jwtsecurity.md").

Output
------
The output Markdown file will include:
- A header indicating the source URL.
- The extracted core content in Markdown format (with headings, paragraphs, code blocks, and images in their original order).

Troubleshooting
---------------
- **Chrome Not Attaching:**  
  Ensure that you have closed any non‑debugging instances of Chrome and restarted it with the remote debugging flag. Also, verify the debugger address (default is "127.0.0.1:9222").
  
- **Missing Dependencies:**  
  If you see errors about missing modules (e.g., selenium or webdriver-manager), make sure you have installed them in your active Python environment.
  
- **Content Not Loading Properly:**  
  If images or other dynamic content are missing, try increasing the sleep duration after navigation to allow more time for content to load.

License & Disclaimer
--------------------
This tool is provided "as is" without any warranty. Use it responsibly and ensure you comply with TryHackMe's terms of service and all applicable laws. The creator, Alienfader, is not responsible for any misuse or unintended consequences of this tool.

Contact
-------
For any questions, feedback, or further assistance, please contact Alienfader.

Enjoy scraping and happy hacking!
