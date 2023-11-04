import requests


class LakeraGuard:
    def __init__(self, api_key):
        self.api_key = api_key

    def check_prompt_injection(self, user_input):
        response = requests.post(
            "https://api.lakera.ai/v1/prompt_injection",
            json={"input": user_input},
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        return response.json()["results"][0]["flagged"]

    def check_moderation(self, user_input):
        moderation_response = requests.post(
            "https://api.lakera.ai/v1/moderation",
            json={"input": user_input},
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        moderation_results = moderation_response.json()["results"][0]
        return moderation_results["categories"], any(
            moderation_results["categories"].values()
        )

    @staticmethod
    def get_error_messages(categories):
        error_messages = []
        if categories["hate"]:
            error_messages.append("Mensaje de odio")
        if categories["sexual"]:
            error_messages.append("Mensaje sexual")
        return " / ".join(error_messages)
