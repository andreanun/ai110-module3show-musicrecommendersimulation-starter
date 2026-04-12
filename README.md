# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify or YouTube learn from massive amounts of listening history and user behavior to predict what you will enjoy next. They combine content features (what a song sounds like) with collaborative signals (what similar listeners liked). This simulation focuses on the content side: it scores each song based on how closely it matches a user's stated preferences, then returns the top matches. Rather than learning from data over time, it applies a fixed weighted formula — transparent, inspectable, and easy to reason about.

### Song Features

Each `Song` object stores the following attributes used in scoring:

| Feature | Type | Description |
|---|---|---|
| `genre` | string | Musical category (pop, lofi, rock, etc.) |
| `mood` | string | Emotional tone (happy, chill, intense, etc.) |
| `energy` | float 0–1 | How energetic or driving the track feels |
| `acousticness` | float 0–1 | How acoustic vs. electronic the track is |
| `tempo_bpm` | float | Beats per minute (normalized before scoring) |

### UserProfile Features

Each `UserProfile` stores the user's taste preferences:

| Field | Type | Description |
|---|---|---|
| `favorite_genre` | string | Preferred genre for exact-match scoring |
| `favorite_mood` | string | Preferred mood for exact-match scoring |
| `target_energy` | float 0–1 | Desired energy level (scored by closeness) |
| `likes_acoustic` | bool | Whether the user prefers acoustic sound |

### Algorithm Recipe

Each song is scored using a weighted formula. The loop visits every song in the catalog, computes the five terms below, sums them, then sorts all results descending and returns the top `k`.

```
score = 2.0 × genre_match                              # exact match → 1 or 0
      + 1.0 × mood_match                               # exact match → 1 or 0
      + 1.0 × (1 − |song.energy − user.energy|)        # closeness, 0–1 scale
      + 0.5 × (1 − |song.acousticness − user.acousticness|)  # closeness, 0–1 scale
      + 0.3 × (1 − |tempo_norm(song) − tempo_norm(user)|)    # normalized first
```

**Score range:** 0.0 (no overlap at all) → 4.8 (perfect match on every feature)

**Term-by-term reasoning:**

| Term | Weight | Why this weight |
|---|---|---|
| genre | 2.0 | Dominant signal — genre controls instrumentation and production style |
| mood | 1.0 | What the listener wants right now; half the weight of genre |
| energy | 1.0 | High-resolution continuous signal; rewards closeness not magnitude |
| acousticness | 0.5 | Useful tiebreaker but wide catalog spread can distort rankings |
| tempo | 0.3 | Fine-grained tiebreaker; must be normalized before differencing |

Tempo is normalized to 0–1 using the catalog min and max at runtime:
```
tempo_norm = (bpm − min_bpm) / (max_bpm − min_bpm)
```

Songs are ranked by total score and the top `k` are returned with an explanation.

---

### Known Biases and Limitations

**Genre dominance.** At weight 2.0, genre is worth as much as a perfect mood match plus a perfect energy match combined. A high-energy rock song will lose to a low-energy pop song every time for a pop-preferring user, even if the rock song matches the user's energy and mood exactly. This may cause the system to miss great cross-genre fits.

**Exact-match brittleness.** Genre and mood are string comparisons. "indie pop" and "pop" score 0 for genre match even though they are sonically close. A user who likes "chill" songs will not benefit from "relaxed" or "peaceful" songs that feel nearly identical.

**Catalog size amplifies both problems.** With only 18 songs, genre dominance is especially visible — there may be only one or two songs per genre, so a genre mismatch immediately drops a song to the bottom of the list regardless of how well it fits numerically.

**No personalization over time.** The system applies the same fixed weights to every user. It cannot learn that one user cares deeply about genre while another only cares about energy. Real recommenders adapt weights per user from listening history.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this made me realize that a recommender isn't really "smart" — it just turns preferences into numbers and picks the highest one. Every song gets a score based on how close it is to what you said you want, and the math doesn't know anything beyond that. The interesting part is how much the design choices matter. Deciding that genre is worth 2 points and tempo is worth 0.3 points is a judgment call, not a fact. Those weights shape every recommendation the system makes, and changing them even slightly can flip the results completely — which we saw during the weight shift experiment.

The bias side was more surprising. I went in thinking bias meant something obvious like "the system ignores certain users." But the real issue was subtler: the system treats genre as an all-or-nothing signal, so users whose genre isn't well represented in the catalog get noticeably worse recommendations, even if their other preferences are perfectly matchable. A reggae fan and a lofi fan could have identical energy and mood preferences, but the lofi fan gets three strong candidates and the reggae fan gets five nearly identical results that basically mean "we have no idea." That kind of unevenness is easy to miss when you're just looking at the formula — you have to actually run it on different users to see it.


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

