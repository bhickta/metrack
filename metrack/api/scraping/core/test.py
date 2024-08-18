import re

# The input text
text = """
Consider the following statements regarding Statutory Bail in India:
Statutory bail is a right that becomes available to an accused when the police fail to complete their investigation within a specified period.
The time limit for statutory bail is uniformly 60 days across all types of cases.
Statutory bail is enshrined in the Code of Criminal Procedure (CrPC).
How many of the above statements is/are correct?
a) Only one
b) Only two
c) All three
d) None
"""

# Define a regular expression pattern to match sentences starting with a), b), c), d) and extract the text
pattern = re.compile(r'[a-d]\)\s([^\n]+)')

# Find all matches
matches = pattern.findall(text)

