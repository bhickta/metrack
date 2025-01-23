# Copyright (c) 2024, nishantbhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import re


class SubjectiveQuestion(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF
        from metrack.metrack.doctype.subjective_question_theme.subjective_question_theme import SubjectiveQuestionTheme
        from metrack.metrack.doctype.urls.urls import Urls

        exam: DF.Link | None
        input_urls: DF.SmallText | None
        naming_series: DF.Literal["Q-.#."]
        source: DF.Data | None
        status: DF.Literal["Untouched", "Read", "Brainstormed", "Written"]
        subjective_question_topic: DF.Table[SubjectiveQuestionTheme]
        title: DF.Text
        url: DF.SmallText | None
        urls: DF.Table[Urls]
        year: DF.Data | None
    # end: auto-generated types
    pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_init(self)

    def post_init(self, *args, **kwargs):
        pass

    def validate(self):
        self.extract_urls()

    def onload(self):
        if self.status != "Read" and self.status not in ["Brainstormed", "Written"]:
            self.status = "Read"
            self.save(ignore_permissions=True)
            frappe.db.commit()

    def extract_urls(self):
        extracted_urls = []
        seen_urls = set()  # To track unique URLs
        if self.input_urls:
            lines = self.input_urls.strip().split("\n")
            for line in lines:
                match = re.match(r"\[(.*?)\]\((.*?)\)", line.strip())
                if match:
                    title, url = match.groups()
                    # Check if the URL is unique in both seen_urls and self.urls
                    if url not in seen_urls and url not in [u["url"] for u in self.urls]:
                        extracted_urls.append({"title": title, "url": url})
                        seen_urls.add(url)  # Mark URL as seen
        if extracted_urls:
            for url in extracted_urls:
                # Skip URLs containing "metrack" or "localhost"
                if "metrack" in url["url"] or "localhost" in url["url"]:
                    continue
                self.append("urls", url)
        # Clear input_urls after processing
        self.input_urls = None
        self.question_status = "Done"

    def onload(self):
        self.set_onload("done_today", frappe.db.count("Subjective Question", filters={"status": ["in", ["Brainstormed", "Written"]], "modified": (">=", frappe.utils.today())}))