# pyrefly: ignore [missing-import]
from playwright.sync_api import sync_playwright
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set
from datetime import datetime
from config import WEBSITE_URL, MAX_CRAWL_PAGES, REQUEST_TIMEOUT
from services.website_cache import save_website_cache, reload_website_cache

class WebsiteCrawler:
    def __init__(self, start_url: str, max_pages: int, timeout: int):
        self.start_url = start_url
        self.domain = urlparse(start_url).netloc
        self.max_pages = max_pages
        self.timeout = timeout
        self.visited: Set[str] = set()
        self.pages: List[Dict] = []
        self.failed_pages: List[str] = []

    def is_valid_url(self, url: str) -> bool:
        parsed = urlparse(url)
        # Check domain
        if parsed.netloc != self.domain:
            return False
        # Prevent fragments and query params that might duplicate content loosely
        return True

    def normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    def extract_content(self, html: str) -> str:
        """
        Extensible interface for content extraction.
        Currently uses BeautifulSoup, but can be updated for JS later.
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove scripts and styles
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text(separator=' ')
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        return '\n'.join(chunk for chunk in chunks if chunk)

    def extract_title(self, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        return soup.title.string if soup.title else ""

    def extract_links(self, html: str, base_url: str) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            norm_url = self.normalize_url(full_url)
            if self.is_valid_url(norm_url):
                links.append(norm_url)
        return links

    def crawl(self) -> Dict:
        urls_to_visit = [self.normalize_url(self.start_url)]
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            page.set_default_timeout(self.timeout * 1000)
            
            while urls_to_visit and len(self.pages) < self.max_pages:
                current_url = urls_to_visit.pop(0)
                
                if current_url in self.visited:
                    continue
                    
                self.visited.add(current_url)
                
                try:
                    print(f"Crawling ({len(self.pages) + 1}/{self.max_pages}): {current_url}")
                    page.goto(current_url, wait_until="domcontentloaded")
                    html_content = page.content()
                    
                    try:
                        text_content = page.evaluate("document.body.innerText")
                    except Exception:
                        text_content = self.extract_content(html_content)
                    
                    title = self.extract_title(html_content)
                    
                    if text_content:
                        self.pages.append({
                            "url": current_url,
                            "title": title,
                            "text": text_content
                        })
                    else:
                        self.failed_pages.append(current_url)
                        
                    new_links = self.extract_links(html_content, current_url)
                    for link in new_links:
                        if link not in self.visited and link not in urls_to_visit:
                            urls_to_visit.append(link)
                            
                except Exception as e:
                    print(f"Failed to crawl {current_url}: {e}")
                    self.failed_pages.append(current_url)
            
            browser.close()

        # Save to cache
        last_refreshed_str = datetime.now().isoformat()
        save_website_cache(self.pages, last_refreshed_str)
        reload_website_cache()
        
        return {
            "success": True,
            "pages_crawled": len(self.pages),
            "pages_failed": len(self.failed_pages),
            "failed_urls": self.failed_pages,
            "last_refreshed": last_refreshed_str
        }

def start_crawl():
    crawler = WebsiteCrawler(WEBSITE_URL, MAX_CRAWL_PAGES, REQUEST_TIMEOUT)
    return crawler.crawl()
# pyrefly: ignore [parse-error]
