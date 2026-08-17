from cricdata import CricinfoClient
from google import genai
import json


# ==========================================
# CLIENTS
# ==========================================

cric_client = CricinfoClient()
gemini_client = genai.Client()


# ==========================================
# REGIONS TO IGNORE
# ==========================================

REGIONS = {
    "Africa",
    "Americas",
    "Asia",
    "Europe",
    "Oceania"
}


# ==========================================
# GET PLAYER DATA
# ==========================================

def get_player_data(player_name):

    results = cric_client.search_players(player_name)

    if not results:
        print(f"Player not found: {player_name}")
        return None

    player = results[0]
    player_id = player["id"]

    # Player information
    bio = cric_client.player_bio(player_id)

    home_country = player["teamRelationships"][0]["displayName"]

    # ODI batting statistics
    stats = cric_client.player_career_stats(
        player_id,
        fmt="odi",
        stat_type="batting"
    )

    summary = stats["summary"]
    breakdowns = stats["breakdowns"]

    # ==========================================
    # OVERALL
    # ==========================================

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

    # ==========================================
    # HOME
    # ==========================================

    home = None

    # ==========================================
    # OVERSEAS TOTALS
    # ==========================================

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

    # ==========================================
    # PROCESS BREAKDOWNS
    # ==========================================

    for item in breakdowns:

        grouping = item.get("Grouping", "")

        if not grouping.startswith("in "):
            continue

        country = grouping[3:]

        if country in REGIONS:
            continue

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

        # ==========================================
        # HOME
        # ==========================================

        if country == home_country:

            dismissals = innings - not_outs

            average = (
                runs / dismissals
                if dismissals > 0
                else 0
            )

            strike_rate = (
                (runs / balls) * 100
                if balls > 0
                else 0
            )

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

        # ==========================================
        # OVERSEAS
        # ==========================================

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

    # ==========================================
    # OVERSEAS CALCULATIONS
    # ==========================================

    overseas_dismissals = (
        overseas_innings - overseas_not_outs
    )

    overseas_average = (
        overseas_runs / overseas_dismissals
        if overseas_dismissals > 0
        else 0
    )

    overseas_strike_rate = (
        (overseas_runs / overseas_balls) * 100
        if overseas_balls > 0
        else 0
    )

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

    # ==========================================
    # FINAL PLAYER DATA
    # ==========================================

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
# GEMINI ANALYSIS
# ==========================================

def compare_players(player1, player2):

    player1_json = json.dumps(
        player1,
        indent=2
    )

    player2_json = json.dumps(
        player2,
        indent=2
    )

    prompt = f"""
You are a cricket statistics analyst.

Compare these two ODI cricket players using ONLY the statistics provided below.

PLAYER 1:
{player1_json}

PLAYER 2:
{player2_json}

Give the comparison in this format:

1. Overall comparison
2. Home performance comparison
3. Overseas performance comparison
4. Strengths of Player 1
5. Strengths of Player 2

For strengths:
- Compare each player against the other player.
- Also identify improvements/declines from home to overseas separately.
- Do NOT call something a "strength" merely because a player's own overseas
  numbers are better than their home numbers.
- A strength should be meaningful relative to the comparison or clearly
  supported by the player's statistics.
6. Who has the better overall ODI batting record?
7. Final verdict

Important:
- Use the actual numbers.
- Do not invent statistics.
- Do not use information that is not provided.
- Mention when the sample size is very different.
- Do not judge bowling ability because the provided data is batting data.
"""

    response = gemini_client.interactions.create(
        model="gemini-3.5-flash",
        input=prompt
    )

    return response.output_text


# ==========================================
# MAIN
# ==========================================

player1_name = input("Enter first player name: ")
player2_name = input("Enter second player name: ")

player1 = get_player_data(player1_name)
player2 = get_player_data(player2_name)

if player1 and player2:

    print("\n" + "=" * 70)
    print("GEMINI PLAYER COMPARISON")
    print("=" * 70)

    analysis = compare_players(
        player1,
        player2
    )

    print("\n")
    print(analysis)