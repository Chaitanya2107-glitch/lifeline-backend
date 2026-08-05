import json


class AIResponseError(Exception):
    pass


def parse_ai_response(response: str) -> dict:
    response = response.strip()

    if response.startswith("```json"):
        response = response.replace("```json", "", 1)

    if response.startswith("```"):
        response = response.replace("```", "", 1)

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    try:
        return json.loads(response)

    except json.JSONDecodeError as e:
        raise AIResponseError(f"Invalid AI JSON: {e}")
