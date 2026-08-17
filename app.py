from flask import Flask, render_template, request
import time

from cricket_data import get_player_data
from gemini_analysis import compare_players


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():

    player1 = None
    player2 = None
    analysis = None
    error = None

    if request.method == "POST":

        player1_name = request.form.get("player1", "").strip()
        player2_name = request.form.get("player2", "").strip()

        if not player1_name or not player2_name:

            error = "Please enter both player names."

        else:

            # ==========================================
            # GET PLAYER DATA
            # ==========================================

            start = time.time()

            player1 = get_player_data(player1_name)

            print(
                "Player 1:",
                round(time.time() - start, 2),
                "seconds"
            )

            player2 = get_player_data(player2_name)

            print(
                "Player 2:",
                round(time.time() - start, 2),
                "seconds"
            )

            if not player1:

                error = f"Player not found: {player1_name}"

            elif not player2:

                error = f"Player not found: {player2_name}"

            else:

                # ==========================================
                # GEMINI ANALYSIS
                # ==========================================

                try:

                    analysis_start = time.time()

                    analysis = compare_players(
                        player1,
                        player2
                    )

                    print(
                        "Gemini:",
                        round(time.time() - analysis_start, 2),
                        "seconds"
                    )

                    print(
                        "TOTAL:",
                        round(time.time() - start, 2),
                        "seconds"
                    )

                except Exception as e:

                    print("Gemini error:", e)

                    analysis = (
                        "The statistical comparison is available above, "
                        "but AI analysis is temporarily unavailable. "
                        "Please try again later."
                    )

    return render_template(
        "index.html",
        player1=player1,
        player2=player2,
        analysis=analysis,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)