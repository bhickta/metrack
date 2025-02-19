import frappe
from metrack.api.scraping.markdown import get_article_content
from tqdm import tqdm
import time

def execute():
    urls = frappe.get_all("Urls", filters={"markdown": ["is", "not set"], "title": ["not like", "%Wiki%"]}, pluck="name")
    count = 0
    start_time = time.time()
    total_urls = len(urls)
    
    for i, url in enumerate(tqdm(urls, desc="Processing URLs")):
        try:
            doc = frappe.get_doc("Urls", url)
            markdown = get_article_content(doc.url)
            
            if markdown:
                doc.markdown = markdown.markdown
                doc.save()
                count += 1
                
                if count % 10 == 0:
                    frappe.db.commit()
            remaining = total_urls - (i + 1)
            print(f"Remaining URLs: {remaining}")
        except Exception as e:
            frappe.log_error(f"Error processing URL {url}: {str(e)}")
    
    frappe.db.commit()
    elapsed_time = time.time() - start_time
    print(f"Processed {count} URLs in {elapsed_time:.2f} seconds")