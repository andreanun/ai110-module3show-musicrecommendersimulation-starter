"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile — categorical and numerical fields tell a consistent story
    user_prefs = {
        "genre":        "pop",   # preferred genre for exact-match scoring
        "mood":         "happy", # preferred mood for exact-match scoring
        "energy":       0.85,    # target energy level (0.0 = very calm, 1.0 = very intense)
        "acousticness": 0.10,    # target acoustic feel (0.0 = electronic, 1.0 = fully acoustic)
        "tempo_bpm":    125,     # target tempo in beats per minute
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
