import frappe
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from metrack.config import config
from frappe import json

API_KEYS = config["ai"]["ai_key"]
API_ENDPOINTS = config["ai"]["api_endpoints"]
MODEL_PARAMS = config["ai"]["model_params"]


class ModelManager:
    def __init__(self, text):
        self.text = text
        self.chain = self.get_google_gemini_chain()

    def get_google_gemini_chain(self):
        prompt = self.create_prompt()
        llm = self.create_llm()
        return prompt | llm

    def create_prompt(self):
        return ChatPromptTemplate.from_template(
            """
            You are an expert at creating challenging true/false questions. Generate questions from the input text in JSON format:

            [
            {{"statement": "statement text", "true/false": true/false, "explanation": "justification"}}
            ]

            - **Absolutely do not quote the input text directly in your statements or explanations.** Rephrase the information.
            - Generate 50 true and 50 false statements.
            - Statements should be cunningly, deceptive, concise, independent, and cover key facts.
            - Provide brief explanations justifying the truth value.

            Text: {input_text}
            """
        )


    def create_llm(self):
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=API_KEYS["google_gemini"],
        )

    def run_chain(self):
        result = None
        try:
            result = self.chain.invoke({"input_text": self.text})
            json_string = self.extract_json(result)
            if json_string:
                return self.parse_json(json_string)
        except (json.JSONDecodeError, AttributeError) as e:
            frappe.log_error(f"Error processing LLM output: {e}. Raw output: {result}")
        except Exception as e:
            frappe.log_error(f"Unexpected error in run_chain: {e}. Raw output: {result}")
        return None

    def extract_json(self, result):
        if hasattr(result, "content"):
            json_string = result.content
        elif isinstance(result, str):
            json_string = result
        else:
            frappe.log_error(
                f"Unexpected result type: {type(result)}. Raw output: {result}"
            )
            return None
        json_string = json_string.strip()
        if json_string.startswith("```json"):
            json_string = json_string[7:]
        if json_string.endswith("```"):
            json_string = json_string[:-3]

        return json_string.strip()

    def parse_json(self, json_string):
        try:
            json_output = json.loads(json_string)
            if isinstance(json_output, list):
                return json_output
        except json.JSONDecodeError:
            frappe.log_error(f"Failed to parse JSON: {json_string}")
        frappe.log_error("LLM output is not a JSON array.")
        return None


@frappe.whitelist(allow_guest=True)
def get_upsc_questions(text):
    try:
        text = """
        Akbar sent his very able finance minister Todar Mal to build imperial demesne in Kangra and adjoining areas of Chamba.
        In this process, Chamba lost Rihlu, Chari, and Gharoh areas. 
        Raja Pratap Singh Verman was the contemporary of Mughal Emperor Akbar. He was loyal to the Mughals.
        When Raja Surajmal of Nurpur took refugee in the Chamba against protecting himself from the Mughal Army, Raja of Chamba was asked to surrender him or face the wrath of the Mughal Army. However, before anything could happen Raja Surajmal felt ill and died.
        Battle of Dhalog (near Dhalousie) was fought between Raja Janardhan of Chamba and Raja Jagat Singh of Nurpur in which Raja Jagat Singh emerged victorious. Mughals sided Raja Jagat Singh.

        After some time, Raja Jagat Singh revolted against Mughals.
        Emperor Shah Jahah sent a large army under the command of Murad Baksh in 1641 A.D. to suppress the rebellion.
        Prithvi Singh son of Janardhan rushed to Raja of Mandi and Suket to seek their help for the restoration of the Chamba throne.
        Raja Jagat Singh fought bravely but could not withstand the Mughal’s Army.
        Chamba was restored to Prithvi Singh.
        Raja Chatar Singh succeeded his father Prithvi Singh.
        Raja Chatar Singh was the contemporary of Mughal Emperor Aurangzeb. He refused to obey the Royal orders regarding the demolition of Hindu Temples in the native state. Upon this, he had to fight against Mughals.
        """
        manager = ModelManager(text)
        questions = manager.run_chain()
        if questions:
            return questions
        else:
            frappe.throw(
                "Failed to generate UPSC questions. Check server logs for details."
            )
    except Exception as e:
        frappe.throw(f"Error processing request: {str(e)}")