import requests
from dataclasses import dataclass


@dataclass
class UserData:
    first_name: str
    last_name: str
    email: str
    city: str
    country: str

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name}\nEmail: {self.email}\nLocation: {self.city}, {self.country}\n"


class APIClient:
    def __init__(self):
        self.base_url = "https://randomuser.me/api/"

    def get_data_from_api(self, results=10):
        url = f"{self.base_url}?results={results}"
        response = requests.get(url)
        if response.ok:
            return response.json()["results"]
        else:
            print("Error: Failed to fetch data from the API.")
            return []

    def create_user_instance(self, user_data):
        return UserData(
            first_name=user_data["name"]["first"],
            last_name=user_data["name"]["last"],
            email=user_data["email"],
            city=user_data["location"]["city"],
            country=user_data["location"]["country"],
        )

    def run(self, results=10):
        api_data = self.get_data_from_api(results)
        user_instances = [self.create_user_instance(user_data) for user_data in api_data]
        for user in user_instances:
            print(user)


if __name__ == "__main__":
    api_client = APIClient()
    api_client.run()
