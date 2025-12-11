import re
import spacy

class PIIMasker:
    def __init__(self):
        print("🧠 Loading PII Masker models...")
        self.nlp = spacy.load("en_core_web_sm")
        
        # Regex patterns
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        # IMPROVED PHONE REGEX:
        # Handles 10 digits (123-456-7890) AND 7 digits (555-0199)
        # The part "(?:\d{3}[-.]?)?" means "The area code is optional"
        self.phone_pattern = r'\b(?:\d{3}[-.]?)?\d{3}[-.]?\d{4}\b'

    def mask_email(self, text):
        return re.sub(self.email_pattern, "[EMAIL]", text)

    def mask_phone(self, text):
        return re.sub(self.phone_pattern, "[PHONE]", text)

    def mask_entities(self, text):
        doc = self.nlp(text)
        new_text = text
        for ent in reversed(doc.ents):
            if ent.label_ == "PERSON":
                new_text = new_text[:ent.start_char] + "[PERSON]" + new_text[ent.end_char:]
            elif ent.label_ == "ORG":
                new_text = new_text[:ent.start_char] + "[ORG]" + new_text[ent.end_char:]
        return new_text

    def mask_all(self, text):
        text = self.mask_email(text)
        text = self.mask_phone(text)
        text = self.mask_entities(text)
        return text