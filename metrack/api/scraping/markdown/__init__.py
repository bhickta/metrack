import requests
from bs4 import BeautifulSoup
import markdownify
from readabilipy import simple_json_from_html_string
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_fixed
import frappe
from urllib.parse import urlparse

class Scraper:
    def __init__(self, base_url: str):
        self.base_url = base_url.strip()
        self.session = requests.Session()
        self.ua = UserAgent()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2), reraise=True)
    def fetch_page(self):
        headers = {
            "User-Agent": self.ua.random,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.google.com/",
            "Cache-Control": "no-cache"
        }
        self.session.headers.update(headers)
        response = self.session.get(self.base_url, timeout=10)
        response.raise_for_status()
        return response.text

    def clean_html(self, html):
        content = simple_json_from_html_string(html, use_readability=True)
        return content.get('content', '')

    def parse_content(self, html):
        cleaned_html = self.clean_html(html)
        return BeautifulSoup(cleaned_html, "html.parser")

    def extract_page_name(self):
        parsed_url = urlparse(self.base_url)
        page_name = parsed_url.path.strip("/").split("/")[-1]
        return page_name.replace("-", " ").title()  # Convert to title case and replace hyphens with spaces

    def extract_markdown(self, html):
        content_soup = self.parse_content(html)
        markdown_content = markdownify.markdownify(str(content_soup), heading_style="ATX").strip()
        return "\n".join(line for line in markdown_content.splitlines() if line.strip())

def get_article_content(url):
    scraper = Scraper(base_url=url)
    try:
        html = scraper.fetch_page()
        title = scraper.extract_page_name()  # Using page name from URL as title
        markdown = scraper.extract_markdown(html)
        return frappe._dict({'title': title, 'markdown': markdown})
    except requests.exceptions.RequestException as e:
        frappe.log_error(f"Error fetching URL: {e}")
    except Exception as e:
        frappe.log_error(f"An error occurred: {e}")
    return None

def fetch_article_data(url: str):
    result = get_article_content(url)
    if result:
        return result
    return None