import json

class FAQDatabase:
    def __init__(self):
        self.faq_file = 'faq_data.json'  

    def get_faq_data(self):
        try:
            with open(self.faq_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            faqs = []
            for category in data.get("categories", []):
                for subcategory in category.get("subcategories", []):
                    faqs.extend(subcategory.get("faqs", []))
            return faqs
        except FileNotFoundError:
            print(f"Error: FAQ data file not found: {self.faq_file}")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in file: {self.faq_file}")
            return []
