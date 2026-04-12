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
    print(f"Loaded songs: {len(songs)}")

    # Taste profile — categorical and numerical fields tell a consistent story
    user_prefs = {
        "genre":        "pop",   # preferred genre for exact-match scoring
        "mood":         "happy", # preferred mood for exact-match scoring
        "energy":       0.85,    # target energy level (0.0 = very calm, 1.0 = very intense)
        "acousticness": 0.10,    # target acoustic feel (0.0 = electronic, 1.0 = fully acoustic)
        "tempo_bpm":    125,     # target tempo in beats per minute
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    divider = "=" * 54
    thin    = "-" * 54
    profile_line = (
        f"  genre={user_prefs['genre']} | mood={user_prefs['mood']} | "
        f"energy={user_prefs['energy']} | tempo={user_prefs['tempo_bpm']} bpm"
    )
    print(f"\n{divider}")
    print(f"  Top {len(recommendations)} Recommendations")
    print(profile_line)
    print(divider)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n #{rank}  {song['title']}  —  {song['artist']}")
        print(f"      Score : {score:.2f} / 4.80")
        for reason in explanation.split(" | "):
            print(f"      • {reason}")

    print(f"\n{thin}\n")


if __name__ == "__main__":
    main()
