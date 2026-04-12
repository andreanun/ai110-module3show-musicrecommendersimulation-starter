"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


PROFILES = [
    # --- Standard profiles ---
    {
        "label":        "High-Energy Pop",
        "genre":        "pop",
        "mood":         "happy",
        "energy":       0.90,
        "acousticness": 0.05,
        "tempo_bpm":    130,
    },
    {
        "label":        "Chill Lofi Session",
        "genre":        "lofi",
        "mood":         "chill",
        "energy":       0.38,
        "acousticness": 0.80,
        "tempo_bpm":    76,
    },
    {
        "label":        "Intense Rock",
        "genre":        "rock",
        "mood":         "intense",
        "energy":       0.92,
        "acousticness": 0.08,
        "tempo_bpm":    155,
    },
    # --- Adversarial / edge-case profiles ---
    {
        "label":        "Conflicting Vibes (peaceful genre, extreme energy)",
        "genre":        "classical",
        "mood":         "peaceful",
        "energy":       0.95,   # classical/peaceful songs sit near 0.18 — direct contradiction
        "acousticness": 0.05,   # classical is highly acoustic — another contradiction
        "tempo_bpm":    145,
    },
    {
        "label":        "Missing Genre (reggae/groovy not in catalog)",
        "genre":        "reggae",
        "mood":         "groovy",
        "energy":       0.65,
        "acousticness": 0.45,
        "tempo_bpm":    105,
    },
    {
        "label":        "Dead Center (all features at midpoint)",
        "genre":        "ambient",
        "mood":         "focused",
        "energy":       0.50,   # average of the catalog — minimal differentiation signal
        "acousticness": 0.50,
        "tempo_bpm":    100,
    },
]


def print_recommendations(label: str, recommendations: list) -> None:
    divider = "=" * 58
    thin    = "-" * 58
    print(f"\n{divider}")
    print(f"  {label}")
    print(divider)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n #{rank}  {song['title']}  —  {song['artist']}")
        print(f"      Score : {score:.2f} / 4.80")
        for reason in explanation.split(" | "):
            print(f"      • {reason}")
    print(f"\n{thin}\n")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    for prefs in PROFILES:
        label = prefs["label"]
        recommendations = recommend_songs(prefs, songs, k=5)
        print_recommendations(label, recommendations)


if __name__ == "__main__":
    main()
