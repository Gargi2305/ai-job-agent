import json

def parse_json_response(text):
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)