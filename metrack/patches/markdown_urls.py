import frappe
from metrack.api.scraping.markdown import get_article_content

def execute():
    urls = frappe.get_all("Urls", filters={"markdown": ["is", "not set"], "title": ["not like", "%Wiki%"]}, pluck="name")
    
    count = 0
    for url in urls:
        try:
            doc = frappe.get_doc("Urls", url)
            markdown = get_article_content(doc.url)
            
            if markdown:
                doc.markdown = markdown.markdown
                doc.save()
                count += 1
                
                if count % 10 == 0:
                    frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Error processing URL {url}: {str(e)}")
    
    frappe.db.commit()