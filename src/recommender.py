import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs ranked by match score for the given user profile."""
        if not self.songs:
            return []
        user_prefs = {
            "genre":        user.favorite_genre,
            "mood":         user.favorite_mood,
            "energy":       user.target_energy,
            "acousticness": 1.0 if user.likes_acoustic else 0.0,
        }
        tempos = [s.tempo_bpm for s in self.songs]
        min_tempo, max_tempo = min(tempos), max(tempos)
        return sorted(
            self.songs,
            key=lambda s: score_song(
                user_prefs,
                {"genre": s.genre, "mood": s.mood, "energy": s.energy,
                 "tempo_bpm": s.tempo_bpm, "acousticness": s.acousticness},
                min_tempo, max_tempo,
            )[0],
            reverse=True,
        )[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable string explaining why a song was recommended."""
        user_prefs = {
            "genre":        user.favorite_genre,
            "mood":         user.favorite_mood,
            "energy":       user.target_energy,
            "acousticness": 1.0 if user.likes_acoustic else 0.0,
        }
        tempos = [s.tempo_bpm for s in self.songs]
        min_tempo, max_tempo = min(tempos), max(tempos)
        total, reasons = score_song(
            user_prefs,
            {"genre": song.genre, "mood": song.mood, "energy": song.energy,
             "tempo_bpm": song.tempo_bpm, "acousticness": song.acousticness},
            min_tempo, max_tempo,
        )
        return f"Score {total:.2f}: " + " | ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(
    user_prefs: Dict,
    song: Dict,
    min_tempo: float,
    max_tempo: float,
) -> Tuple[float, List[str]]:
    """Score one song against user_prefs and return (total_score, reasons_list)."""
    score = 0.0
    reasons = []

    # Genre exact match: +2.0
    if song["genre"] == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood exact match: +1.0
    if song["mood"] == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy closeness: weight 1.0, scale 0–1
    target_energy = user_prefs.get("energy", 0.5)
    energy_points = round(1.0 * (1.0 - abs(song["energy"] - target_energy)), 2)
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    # Acousticness closeness: weight 0.5, scale 0–1
    target_acoustic = user_prefs.get("acousticness", 0.5)
    acoustic_points = round(0.5 * (1.0 - abs(song["acousticness"] - target_acoustic)), 2)
    score += acoustic_points
    reasons.append(f"acousticness closeness (+{acoustic_points:.2f})")

    # Tempo closeness: weight 0.3, normalized to 0–1 first
    target_tempo = user_prefs.get("tempo_bpm")
    if target_tempo is not None and max_tempo > min_tempo:
        tempo_norm = (song["tempo_bpm"] - min_tempo) / (max_tempo - min_tempo)
        target_norm = (target_tempo - min_tempo) / (max_tempo - min_tempo)
        tempo_points = round(0.3 * (1.0 - abs(tempo_norm - target_norm)), 2)
        score += tempo_points
        reasons.append(f"tempo closeness (+{tempo_points:.2f})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song in the catalog and return the top k as (song, score, explanation) tuples."""
    if not songs:
        return []

    tempos = [s["tempo_bpm"] for s in songs]
    min_tempo, max_tempo = min(tempos), max(tempos)

    scored = sorted(
        [
            (song, score, " | ".join(reasons))
            for song in songs
            for score, reasons in [score_song(user_prefs, song, min_tempo, max_tempo)]
        ],
        key=lambda x: x[1],
        reverse=True,
    )
    return scored[:k]
