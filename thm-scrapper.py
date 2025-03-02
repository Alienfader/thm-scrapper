import sys
import time
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup, NavigableString
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# A list of phrases that we want to filter out from text nodes.
UNWANTED_PHRASES = [
    "learn", "compete", "for education", "for business", "pricing",
    "join for free", "log in"
]

def filter_text(text):
    """
    If the text is short and exactly matches an unwanted phrase, or
    if it contains known footer/ad content, return an empty string.
    Otherwise, return the original text.
    """
    t = text.strip()
    lower_t = t.lower()
    # If the text is very short (3 words or fewer) and exactly one of the unwanted phrases, skip it.
    if len(lower_t.split()) <= 3 and lower_t in UNWANTED_PHRASES:
        return ""
    # Remove text that contains typical footer/ad indicators.
    if "copyright tryhackme" in lower_t:
        return ""
    if "we use cookies" in lower_t:
        return ""
    # Otherwise, keep the text.
    return t

def get_existing_driver():
    """
    Attaches to an already-running Chrome instance on port 9222.
    Make sure you launched Chrome with remote debugging enabled using your logged-in profile.
    """
    options = Options()
    options.debugger_address = "127.0.0.1:9222"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def scrape_page(driver, url):
    """
    Navigates the attached driver to the given URL, waits for dynamic content to load,
    and returns the page source.
    """
    driver.get(url)
    time.sleep(3)  # Wait for dynamic content (including images) to load.
    return driver.page_source

def convert_element_to_markdown(element):
    """
    Recursively converts a BeautifulSoup element and its children to Markdown.
    It preserves text, images (checking both 'src' and 'data-src' for lazy-loaded images),
    code blocks, and headings.
    Applies filtering to text nodes to bypass common ad/footer content.
    """
    if isinstance(element, NavigableString):
        return filter_text(str(element))
    
    if element.name == 'img':
        # Use the 'src' attribute; if not available, try 'data-src' (for lazy-loaded images).
        src = element.get("src") or element.get("data-src", "")
        alt = element.get("alt", "Image")
        return f"\n\n![{alt}]({src})\n\n"
    
    if element.name == 'code' and element.parent.name != 'pre':
        return f"`{element.get_text(strip=True)}`"
    
    if element.name == 'pre':
        code = element.get_text(strip=True)
        return f"\n\n```\n{code}\n```\n\n"
    
    if element.name in ['h1','h2','h3','h4','h5','h6']:
        level = int(element.name[1])
        content = ''.join(convert_element_to_markdown(child) for child in element.children).strip()
        return f"\n\n{'#' * level} {content}\n\n"
    
    if element.name == 'p':
        parts = []
        for child in element.children:
            if isinstance(child, NavigableString):
                parts.append(filter_text(str(child)))
            else:
                parts.append(convert_element_to_markdown(child))
        content = ''.join(parts).strip()
        if content:
            return content + "\n\n"
        return ""
    
    content = ''.join(convert_element_to_markdown(child) for child in element.children)
    return content

def parse_ordered_content(html):
    """
    Parses the HTML and extracts the core room content.
    It removes common site-wide elements and then attempts to locate the container
    holding the room details (using a common class pattern). If not found, falls back to <main> or the full body.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove unwanted site-wide elements.
    for tag in soup(["header", "footer", "nav", "script", "style", "iframe"]):
        tag.decompose()
    
    main_content = soup.find(lambda tag: tag.name == "div" and tag.get("class") and 
                             any("Room__Main" in cls for cls in tag.get("class")))
    if not main_content:
        main_content = soup.find("main")
    if not main_content:
        main_content = soup.body
    
    markdown = convert_element_to_markdown(main_content)
    return markdown

def create_markdown(markdown_content, file_name, url=""):
    """
    Wraps the converted Markdown content with a header and writes it to a Markdown (.md) file.
    """
    full_markdown = (
        f"# Scraped Notes from {url}\n\n"
        "Below is the organized content extracted from the page:\n\n"
        "### **Core Content**\n\n"
        f"{markdown_content}\n"
    )
    
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(full_markdown)
    
    print(f"Markdown note saved as {file_name}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 newapproach.py <URL1> [URL2 ...]")
        sys.exit(1)
    
    urls = sys.argv[1:]
    print("Scraping content from the following URLs:")
    for url in urls:
        print("  -", url)
    
    driver = get_existing_driver()
    
    # (Assumes your attached Chrome session is already logged in.)
    print("Using your existing Chrome session (assumed logged in).")
    
    for url in urls:
        print(f"Scraping content from: {url}")
        html_content = scrape_page(driver, url)
        markdown_content = parse_ordered_content(html_content)
        
        parsed_url = urlparse(url)
        base_name = os.path.basename(parsed_url.path)
        if not base_name:
            base_name = "scraped_notes"
        file_name = f"{base_name}.md"
        
        create_markdown(markdown_content, file_name, url=url)
    
    driver.quit()

if __name__ == "__main__":
    main()
