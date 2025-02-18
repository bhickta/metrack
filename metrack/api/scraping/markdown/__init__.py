import requests
from bs4 import BeautifulSoup
import markdownify
from readability import Document
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_fixed

class Scraper:
    def __init__(self, **kwargs):
        self.base_url = kwargs.get('base_url', '').strip()
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
        """Clean the HTML by extracting the main content like Firefox's read mode."""
        doc = Document(html)
        content = doc.summary()  # Extract the readable content from the page
        return content

    def parse_content(self, html):
        """Parse the cleaned content into BeautifulSoup for further processing."""
        cleaned_html = self.clean_html(html)
        content_soup = BeautifulSoup(cleaned_html, "html.parser")
        return content_soup

    def extract_markdown(self):
        try:
            html = self.fetch_page()
            content_soup = self.parse_content(html)
            markdown_content = markdownify.markdownify(str(content_soup), heading_style="ATX").strip()
            return "\n".join(line for line in markdown_content.splitlines() if line.strip())
        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    url = "https://www.insightsonindia.com/ancient-indian-history/post-gupta-age/chalukyas/"  # Replace with your URL
    scraper = Scraper(base_url=url)
    markdown = scraper.extract_markdown()

    if markdown:
        print(markdown)
    else:
        print("Failed to extract content.")
