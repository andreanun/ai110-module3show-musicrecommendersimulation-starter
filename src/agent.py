import os
import pathlib
from typing import List

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

from recommender import Song, UserProfile, Recommender, load_songs

load_dotenv()

DEFAULT_CATALOG = pathlib.Path(__file__).parent.parent / "data" / "songs.csv"

_PARSE_SYSTEM = """You are a music preference analyst. Convert natural language music requests into structured preferences.

Available genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, r&b, classical, folk, electronic, country, metal, soul
Available moods: happy, chill, intense, peaceful, focused, melancholic, groovy, romantic, energetic

Rules:
- target_energy: float 0.0 (very calm) to 1.0 (very high energy)
- likes_acoustic: true for organic/acoustic sounds, false for electronic/produced
- Pick the closest matching genre and mood from the lists above"""


class ParsedProfile(BaseModel):
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def parse_user_input(client: anthropic.Anthropic, user_input: str) -> UserProfile:
    """Step 1 — Use Claude to convert natural language into a structured UserProfile."""
    response = client.messages.parse(
        model="claude-opus-4-7",
        max_tokens=256,
        system=_PARSE_SYSTEM,
        messages=[{
            "role": "user",
            "content": f"Convert to structured music preferences: {user_input}",
        }],
        output_format=ParsedProfile,
    )
    p = response.parsed_output
    return UserProfile(
        favorite_genre=p.favorite_genre,
        favorite_mood=p.favorite_mood,
        target_energy=max(0.0, min(1.0, p.target_energy)),
        likes_acoustic=p.likes_acoustic,
    )


def generate_explanation(
    client: anthropic.Anthropic,
    user_input: str,
    profile: UserProfile,
    recommendations: List[Song],
) -> str:
    """Step 3 — Use Claude to explain recommendations in natural language (streamed)."""
    songs_block = "\n".join(
        f"  {i+1}. {s.title} by {s.artist} "
        f"(genre: {s.genre}, mood: {s.mood}, energy: {s.energy:.0%})"
        for i, s in enumerate(recommendations)
    )
    prompt = (
        f'User asked: "{user_input}"\n\n'
        f"Interpreted as: genre={profile.favorite_genre}, mood={profile.favorite_mood}, "
        f"energy={profile.target_energy:.0%}, acoustic={profile.likes_acoustic}\n\n"
        f"Top recommendations:\n{songs_block}\n\n"
        "In 2-3 sentences, explain conversationally why these songs fit the request. "
        "Be specific about the connection between the request and the picks."
    )

    parts: List[str] = []
    with client.messages.stream(
        model="claude-opus-4-7",
        max_tokens=512,
        thinking={"type": "adaptive"},
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for chunk in stream.text_stream:
            print(chunk, end="", flush=True)
            parts.append(chunk)
    print()
    return "".join(parts)


def run_agent(user_input: str, catalog_path: str | None = None) -> None:
    """Three-step agentic workflow with observable intermediate steps.

    Step 1: Claude parses natural language → UserProfile (structured output)
    Step 2: Rule-based recommender scores and ranks songs
    Step 3: Claude generates a natural language explanation (streamed)
    """
    client = anthropic.Anthropic()
    path = catalog_path or str(DEFAULT_CATALOG)

    print(f"\n{'='*60}")
    print(f"  Request: {user_input}")
    print(f"{'='*60}")

    # Step 1 — parse
    print("\n[Step 1/3]  Parsing request with Claude...")
    profile = parse_user_input(client, user_input)
    print(f"            genre    → {profile.favorite_genre}")
    print(f"            mood     → {profile.favorite_mood}")
    print(f"            energy   → {profile.target_energy:.0%}")
    print(f"            acoustic → {profile.likes_acoustic}")

    # Step 2 — score
    print("\n[Step 2/3]  Scoring catalog...")
    song_dicts = load_songs(path)
    songs = [Song(**s) for s in song_dicts]
    recommender = Recommender(songs)
    recommendations = recommender.recommend(profile, k=5)
    print(f"            {len(songs)} songs scored, top {len(recommendations)} selected.")

    # Step 3 — explain
    print("\n[Step 3/3]  Generating explanation (streaming):")
    print("            " + "─" * 46)
    print("            ", end="", flush=True)
    explanation = generate_explanation(client, user_input, profile, recommendations)
    print("            " + "─" * 46)

    # Final output
    print("\n  Recommendations:")
    for i, song in enumerate(recommendations, 1):
        score_str = recommender.explain_recommendation(profile, song)
        print(f"\n  #{i}  {song.title} — {song.artist}")
        print(f"       {score_str}")

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else \
        "I want something chill to study to late at night"
    run_agent(query)
