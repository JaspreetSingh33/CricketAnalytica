from cricdata import CricinfoClient

client = CricinfoClient()

REGIONS = {
    "Africa",
    "Americas",
    "Asia",
    "Europe",
    "Oceania"
}


def get_player_data(player_name):

    # =============================
    # SEARCH PLAYER
    # =============================

    results = client.search_players(player_name)

    if not results:
        print("Player not found.")
        return None

    player = results[0]
    player_id = player["id"]
    bio = client.player_bio(player_id)

    # Player's country/team
    home_country = player["teamRelationships"][0]["displayName"]

    # =============================
    # GET ODI BATTING DATA
    # =============================

    stats = client.player_career_stats(
        player_id,
        fmt="odi",
        stat_type="batting"
    )

    summary = stats["summary"]
    breakdowns = stats["breakdowns"]

    # =============================
    # OVERALL
    # =============================

    overall = {
        "matches": int(summary["Mat"]),
        "innings": int(summary["Inns"]),
        "not_outs": int(summary["NO"]),
        "runs": int(summary["Runs"]),
        "average": float(summary["Ave"]),
        "balls_faced": int(summary["BF"]),
        "strike_rate": float(summary["SR"]),
        "hundreds": int(summary["100"]),
        "fifties": int(summary["50"]),
        "highest_score": summary["HS"],
        "fours": int(summary["4s"]),
        "sixes": int(summary["6s"])
    }

    # =============================
    # HOME
    # =============================

    home = None

    # =============================
    # OVERSEAS TOTALS
    # =============================

    overseas_matches = 0
    overseas_innings = 0
    overseas_not_outs = 0
    overseas_runs = 0
    overseas_balls = 0
    overseas_hundreds = 0
    overseas_fifties = 0
    overseas_fours = 0
    overseas_sixes = 0

    overseas_highest_score = None

    # =============================
    # PROCESS BREAKDOWNS
    # =============================

    for item in breakdowns:

        grouping = item.get("Grouping", "")

        # We only want "in <country>"
        if not grouping.startswith("in "):
            continue

        country = grouping[3:]

        # Ignore regions such as Asia, Africa, Europe
        if country in REGIONS:
            continue

        # Ignore entries without batting data
        if item.get("Runs") in [None, "-", ""]:
            continue

        if item.get("Inns") in [None, "-", ""]:
            continue

        matches = int(item["Mat"])
        innings = int(item["Inns"])
        not_outs = int(item["NO"])
        runs = int(item["Runs"])
        balls = int(item["BF"])
        hundreds = int(item["100"])
        fifties = int(item["50"])
        fours = int(item["4s"])
        sixes = int(item["6s"])
        highest = item["HS"]

        # =============================
        # HOME COUNTRY
        # =============================

        if country == home_country:

            dismissals = innings - not_outs

            if dismissals > 0:
                average = runs / dismissals
            else:
                average = 0

            if balls > 0:
                strike_rate = (runs / balls) * 100
            else:
                strike_rate = 0

            home = {
                "matches": matches,
                "innings": innings,
                "not_outs": not_outs,
                "runs": runs,
                "average": round(average, 2),
                "balls_faced": balls,
                "strike_rate": round(strike_rate, 2),
                "hundreds": hundreds,
                "fifties": fifties,
                "highest_score": highest,
                "fours": fours,
                "sixes": sixes
            }

        # =============================
        # OVERSEAS
        # =============================

        else:

            overseas_matches += matches
            overseas_innings += innings
            overseas_not_outs += not_outs
            overseas_runs += runs
            overseas_balls += balls
            overseas_hundreds += hundreds
            overseas_fifties += fifties
            overseas_fours += fours
            overseas_sixes += sixes

            # Find highest overseas score
            if highest not in ["-", None, ""]:

                score = highest.replace("*", "")

                try:

                    score_value = int(score)

                    if (
                        overseas_highest_score is None
                        or score_value > overseas_highest_score[0]
                    ):
                        overseas_highest_score = (
                            score_value,
                            highest
                        )

                except ValueError:
                    pass

    # =============================
    # OVERSEAS AVERAGE
    # =============================

    overseas_dismissals = (
        overseas_innings - overseas_not_outs
    )

    if overseas_dismissals > 0:
        overseas_average = (
            overseas_runs / overseas_dismissals
        )
    else:
        overseas_average = 0

    # =============================
    # OVERSEAS STRIKE RATE
    # =============================

    if overseas_balls > 0:
        overseas_strike_rate = (
            overseas_runs / overseas_balls
        ) * 100
    else:
        overseas_strike_rate = 0

    # =============================
    # OVERSEAS OBJECT
    # =============================

    overseas = {
        "matches": overseas_matches,
        "innings": overseas_innings,
        "not_outs": overseas_not_outs,
        "runs": overseas_runs,
        "average": round(overseas_average, 2),
        "balls_faced": overseas_balls,
        "strike_rate": round(overseas_strike_rate, 2),
        "hundreds": overseas_hundreds,
        "fifties": overseas_fifties,
        "highest_score": (
            overseas_highest_score[1]
            if overseas_highest_score
            else "-"
        ),
        "fours": overseas_fours,
        "sixes": overseas_sixes
    }

    # =============================
    # FINAL DATA
    # =============================

    return {
    "name": player["displayName"],
    "country": home_country,
    "espn_id": player_id,
    "image": bio["headshot"]["href"],
    "overall": overall,
    "home": home,
    "overseas": overseas
}


# ==========================================
# PRINT FUNCTION
# ==========================================

def print_stats(title, data):

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    if data is None:
        print("No data available.")
        return

    print(f"Matches       : {data['matches']}")
    print(f"Innings       : {data['innings']}")
    print(f"Not Outs      : {data['not_outs']}")
    print(f"Runs          : {data['runs']}")
    print(f"Average       : {data['average']}")
    print(f"Balls Faced   : {data['balls_faced']}")
    print(f"Strike Rate   : {data['strike_rate']}")
    print(f"Hundreds      : {data['hundreds']}")
    print(f"Fifties       : {data['fifties']}")
    print(f"Highest Score : {data['highest_score']}")
    print(f"Fours         : {data['fours']}")
    print(f"Sixes         : {data['sixes']}")


# ==========================================
# TEST PLAYER
# ==========================================

player1_name = input("Enter first player name: ")
player2_name = input("Enter second player name: ")

player1 = get_player_data(player1_name)
player2 = get_player_data(player2_name)

if player1:

    print("\nPLAYER 1")
    print("Name :", player1["name"])
    print("Image:", player1["image"])

    print_stats(
        f"{player1['name'].upper()} - OVERALL ODI",
        player1["overall"]
    )

    print_stats(
        f"{player1['name'].upper()} - HOME ODI",
        player1["home"]
    )

    print_stats(
        f"{player1['name'].upper()} - OVERSEAS ODI",
        player1["overseas"]
    )

if player2:

    print("\nPLAYER 2")
    print("Name :", player2["name"])
    print("Image:", player2["image"])

    print_stats(
        f"{player2['name'].upper()} - OVERALL ODI",
        player2["overall"]
    )

    print_stats(
        f"{player2['name'].upper()} - HOME ODI",
        player2["home"]
    )

    print_stats(
        f"{player2['name'].upper()} - OVERSEAS ODI",
        player2["overseas"]
    )