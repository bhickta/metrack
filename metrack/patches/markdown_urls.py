import frappe
from metrack.api.scraping.markdown import get_article_content

def execute():
    urls = frappe.get_all("Urls", filters={"markdown": ["is", "not set"], "title": ["not like", "%Wiki%"]}, pluck="name")
    for url in urls:
        doc = frappe.get_doc("Urls", url)
        markdown = get_article_content(doc.url)
        if markdown:
            doc.markdown = markdown.markdown
            doc.save()