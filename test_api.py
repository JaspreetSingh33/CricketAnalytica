import requests

API_KEY = "1578c467-2450-4026-8ab7-393003f17f23"


# ----------------------------------------
# 1. Search for the player
# ----------------------------------------

search_url = "https://api.cricapi.com/v1/players"

search_params = {
    "apikey": API_KEY,
    "offset": 0,
    "search": "Babar Azam"
}

search_response = requests.get(search_url, params=search_params)
search_data = search_response.json()

player = search_data["data"][0]

player_id = player["id"]
player_name = player["name"]
player_country = player["country"]

print("Player:", player_name)
print("Country:", player_country)
print("ID:", player_id)


# ----------------------------------------
# 2. Get detailed player information
# ----------------------------------------

info_url = "https://api.cricapi.com/v1/players_info"

info_params = {
    "apikey": API_KEY,
    "id": player_id
}

info_response = requests.get(info_url, params=info_params)
info_data = info_response.json()

player_data = info_data["data"]


# ----------------------------------------
# 3. Basic player information
# ----------------------------------------

print("\n" + "=" * 50)
print("PLAYER INFORMATION")
print("=" * 50)

print("Name          :", player_data["name"])
print("Date of Birth :", player_data["dateOfBirth"][:10])
print("Role          :", player_data["role"])
print("Batting Style :", player_data["battingStyle"])
print("Bowling Style :", player_data["bowlingStyle"])
print("Place of Birth:", player_data["placeOfBirth"])
print("Country       :", player_data["country"])
print("Player Image  :", player_data["playerImg"])


# ----------------------------------------
# 4. Show ONLY ODI batting statistics
# ----------------------------------------

print("\n" + "=" * 50)
print("ODI BATTING STATISTICS")
print("=" * 50)

for stat in player_data["stats"]:

    if (
        stat["matchtype"].strip() == "odi"
        and stat["fn"].strip() == "batting"
    ):
        name = stat["stat"].strip()
        value = stat["value"].strip()

        print(f"{name:<5} : {value}")