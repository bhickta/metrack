# Copyright (c) 2024, nishantbhickta and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SubjectiveQuestion(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF
        from metrack.metrack.doctype.subjective_question_topic.subjective_question_topic import SubjectiveQuestionTopic

        exam: DF.Link | None
        naming_series: DF.Literal["Q-.#."]
        source: DF.Data | None
        subjective_question_topic: DF.Table[SubjectiveQuestionTopic]
        title: DF.Text
        url: DF.SmallText | None
        year: DF.Data | None
    # end: auto-generated types
    pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_init(self)

    def post_init(self, *args, **kwargs):
        pass

    def validate(self):
        pass