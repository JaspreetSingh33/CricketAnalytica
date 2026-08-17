from google import genai
from dotenv import load_dotenv
import json

load_dotenv()

gemini_client = genai.Client()

def compare_players(player1, player2):

    # Only send the statistics Gemini actually needs
    player1_data = {
        "name": player1["name"],
        "overall": player1["overall"],
        "home": player1["home"],
        "overseas": player1["overseas"]
    }

    player2_data = {
        "name": player2["name"],
        "overall": player2["overall"],
        "home": player2["home"],
        "overseas": player2["overseas"]
    }

    player1_json = json.dumps(
        player1_data,
        indent=2
    )

    player2_json = json.dumps(
        player2_data,
        indent=2
    )

    prompt = f"""
You are a cricket analyst.

You are comparing two ODI batting players.

PLAYER 1:
{player1_json}

PLAYER 2:
{player2_json}

Give the comparison in this exact format:

1. Overall comparison

- Explain the important statistical differences.
- Focus on runs, average, strike rate, hundreds, fifties and highest score.
- Mention sample-size differences only when meaningful.

2. Home performance comparison

- Compare their home ODI batting statistics.
- Focus on meaningful differences.

3. Overseas performance comparison

- Compare their overseas ODI batting statistics.
- Focus on meaningful differences.

4. Strengths of {player1["name"]}

- Mention only meaningful statistical strengths.

5. Strengths of {player2["name"]}

- Mention only meaningful statistical strengths.

6. Who has the better overall ODI batting record?

- Give a neutral statistical conclusion.
- Explain which statistics support the conclusion.

7. Final verdict

- Give a short balanced conclusion.
- Do not insult or diminish either player.

STATISTICAL RULES:

- Use only the statistics provided.
- Do not invent statistics.
- Do not make historical claims.
- Do not judge bowling ability.
- Do not infer batting position or playing style.
- Do not exaggerate small differences in sample size.
- Focus primarily on batting innings rather than matches when discussing sample size.
- Do not call something a strength merely because its value is non-zero.
- Do not use subjective labels such as "greatest", "world-class",
  "elite", or "historic".
- Do not use "adaptability" or "versatility" unless directly supported
  by the statistics.
- Keep the comparison respectful and neutral.

IMPORTANT:
Return ONLY the analysis.
Do not use an introductory sentence before section 1.
"""


    try:

        response = gemini_client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt
        )

        return response.output_text

    except Exception as e:

        print("Gemini error:", e)

        return (
            "The statistical comparison is available above, "
            "but AI analysis is temporarily unavailable. "
            "Please try again later."
        )