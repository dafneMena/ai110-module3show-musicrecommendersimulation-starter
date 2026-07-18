# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

This version, **MoodMatch 1.0**:

- Scores each of the 18 catalog songs against a user's genre, mood, target energy, and (optionally) acoustic preference
- Returns the top 5 matches, each with a plain-language reason
- Was tested against three consistent profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock)
- Was also tested against one deliberately contradictory profile (Sad but Wired) to see how it handles conflicting preferences instead of clean ones

---

## How The System Works

Real-world recommenders blend two approaches:

 **collaborative filtering**, which predicts taste from what similar users liked, and **content-based filtering**, which predicts taste from an item's own attributes. This simulation is a **content-based** recommender — it has no other users to learn from, so it matches each song's attributes directly against one user's stated taste profile. It also mirrors the two-stage structure production systems use: a **scoring rule** that rates one song against the user profile, and a separate **ranking rule** that sorts and truncates the full scored list to the top `k`.

**`Song` features used:** `genre`, `mood`, `energy`, `acousticness`. These four were chosen because they had the widest, least-redundant spread across the sample catalog — `tempo_bpm` and `danceability` were dropped from scoring since they closely tracked `energy` in this dataset and would have added weight without adding new information.

**`UserProfile` stores:** `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic` — a direct, one to one mirror of the `Song` features above, so every scored attribute has a matching preference to compare against.

**Scoring:** `score_song` computes a weighted average of four 0–1 components: exact matches on `genre` (0.35) and `mood` (0.25) score 1.0 or 0.0; `energy` (0.25) scores `1 - abs(song.energy - target_energy)`, so a near miss still scores highly; and `acousticness` (0.15) scores `song.acousticness`, scaling with how strongly the song leans that way rather than a hard threshold. Genre and mood carry the most weight as the strongest signal in a small catalog; energy and acousticness are smoother secondary and tie-breaking signals. Missing preferences are dropped and the remaining weights renormalize. `score_song` also returns a reason per component, which `explain_recommendation` and `recommend_songs` join into the "Because: ..." text.

**Choosing recommendations:** `recommend_songs` calls `score_song` on every song, then sorts by score descending and returns the top `k`. Ties are broken by catalog order.

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

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
User profile: genre=pop, mood=happy, energy=0.8

Top recommendations:

+------+------------------+-------+-----------------------------------------------+
| Rank | Song             | Score | Reason                                        |
+------+------------------+-------+-----------------------------------------------+
| 1    | Sunrise City     | 0.99  | Genre matches your favorite (pop); Mood       |
|      |                  |       | matches your favorite (happy); Energy (0.82)  |
|      |                  |       | is close to your target (0.80)                |
+------+------------------+-------+-----------------------------------------------+
| 2    | Gym Hero         | 0.67  | Genre matches your favorite (pop); Mood       |
|      |                  |       | (intense) differs from your favorite (happy); |
|      |                  |       | Energy (0.93) is close to your target (0.80)  |
+------+------------------+-------+-----------------------------------------------+
| 3    | Rooftop Lights   | 0.58  | Genre (indie pop) differs from your favorite  |
|      |                  |       | (pop); Mood matches your favorite (happy);    |
|      |                  |       | Energy (0.76) is close to your target (0.80)  |
+------+------------------+-------+-----------------------------------------------+
| 4    | Carnival Sundown | 0.29  | Genre (latin) differs from your favorite      |
|      |                  |       | (pop); Mood (playful) differs from your       |
|      |                  |       | favorite (happy); Energy (0.80) is close to   |
|      |                  |       | your target (0.80)                            |
+------+------------------+-------+-----------------------------------------------+
| 5    | Night Drive Loop | 0.28  | Genre (synthwave) differs from your favorite  |
|      |                  |       | (pop); Mood (moody) differs from your         |
|      |                  |       | favorite (happy); Energy (0.75) is close to   |
|      |                  |       | your target (0.80)                            |
+------+------------------+-------+-----------------------------------------------+

```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

We didn't run these experiments, but based on the scoring formula, here's what we'd expect:

- **Genre weight (2.0 → 0.5):** only the ratio matters (weights renormalize), so lower genre weight lets mood matter more — confirmed by a quick test where Rooftop Lights (mood match) overtook Gym Hero (genre match) for #2.
- **Adding tempo or valence:** tempo is 95% correlated with energy here, so it'd mostly double-count that signal; valence (~28% correlated) would be more independent but likely just echoes mood.
- **Different user types:** consistent profiles (e.g. Chill Lofi) get a clear near-perfect #1; contradictory ones (e.g. Sad but Wired) still get a confident #1, but it's a compromise — genre+mood wins over a poor energy fit since the model averages rather than detects conflict.

---

## Limitations and Risks

Summarize some limitations of your recommender.

- Only works on a tiny, 18-song hand-labeled catalog
- Doesn't understand lyrics, language, or artist reputation — only genre/mood/energy/acousticness tags
- Can over-favor genre+mood matches even when energy is a bad fit, since it averages rather than detects contradictions
- Genre/mood matching is exact-string and case-sensitive, so typos or synonyms silently score as a total mismatch

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

Building this made it clear that a "recommendation" is just a weighted average wearing a friendly explanation — the model doesn't understand taste, it converts genre/mood/energy/acoustic matches into 0-1 scores and blends them by fixed weights, so whichever traits carry the most weight (here, genre and mood) end up deciding the winner almost regardless of the rest. That mechanical simplicity is also where bias creeps in: exact-string genre/mood matching silently punishes typos or synonyms, genres with only one song in the catalog get recommended by default rather than by genuine merit, and a self-contradictory profile still gets a confident top pick because the system averages preferences instead of flagging that they conflict — so it can look "fair" while quietly baking in whatever the weights and the catalog's blind spots happen to favor.



