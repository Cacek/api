import requests


def get_data_from_api():
    url = "https://randomuser.me/api/?results=10" #Przykladowe API
    response = requests.get(url)
    api_data = response.json()
    return api_data["results"]


def display_data(api_data):
    for user in api_data:
        print("First Name:", user["name"]["first"])
        print("Last Name:", user["name"]["last"])
        print("Email:", user["email"])
        print("City:", user["location"]["city"])
        print("Country:", user["location"]["country"])
        print(20 * "-")


def main():
    api_data = get_data_from_api()
    display_data(api_data)


if __name__ == "__main__":
    main()
