import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Relative weights used by score_song. Any preference the caller omits
# (e.g. no likes_acoustic) is dropped and the remaining weights are
# renormalized, so partial preference dicts still produce a 0-1 score.
GENRE_WEIGHT = 0.35
MOOD_WEIGHT = 0.25
ENERGY_WEIGHT = 0.25
ACOUSTIC_WEIGHT = 0.15

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
        user_prefs = asdict(user)
        scored = [(song, score_song(user_prefs, asdict(song))[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(asdict(user), asdict(song))
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Each preference contributes a weighted, continuous 0-1 component
    (distance-based for energy/acousticness) rather than a single
    all-or-nothing match, so songs that partially fit are ranked above
    songs that don't fit at all. Missing preferences are skipped and the
    remaining weights are renormalized.
    """
    favorite_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    favorite_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target_energy = user_prefs.get("target_energy", user_prefs.get("energy"))
    likes_acoustic = user_prefs.get("likes_acoustic")

    song_genre = song.get("genre")
    song_mood = song.get("mood")
    song_energy = float(song.get("energy", 0.0))
    song_acousticness = float(song.get("acousticness", 0.0))

    components = []  # (weight, 0-1 fit score, human-readable reason)

    if favorite_genre is not None:
        match = song_genre == favorite_genre
        components.append((
            GENRE_WEIGHT,
            1.0 if match else 0.0,
            f"Genre matches your favorite ({song_genre})" if match
            else f"Genre ({song_genre}) differs from your favorite ({favorite_genre})",
        ))

    if favorite_mood is not None:
        match = song_mood == favorite_mood
        components.append((
            MOOD_WEIGHT,
            1.0 if match else 0.0,
            f"Mood matches your favorite ({song_mood})" if match
            else f"Mood ({song_mood}) differs from your favorite ({favorite_mood})",
        ))

    if target_energy is not None:
        target_energy = float(target_energy)
        closeness = max(0.0, min(1.0, 1.0 - abs(song_energy - target_energy)))
        components.append((
            ENERGY_WEIGHT,
            closeness,
            f"Energy ({song_energy:.2f}) is close to your target ({target_energy:.2f})" if closeness >= 0.8
            else f"Energy ({song_energy:.2f}) is somewhat different from your target ({target_energy:.2f})",
        ))

    if likes_acoustic is not None:
        acoustic_fit = song_acousticness if likes_acoustic else (1.0 - song_acousticness)
        components.append((
            ACOUSTIC_WEIGHT,
            acoustic_fit,
            f"Acousticness ({song_acousticness:.2f}) aligns with your preference for "
            f"{'acoustic' if likes_acoustic else 'non-acoustic/electronic'} sound",
        ))

    if not components:
        return 0.0, ["No preference data available to score against."]

    total_weight = sum(weight for weight, _, _ in components)
    score = sum(weight * fit for weight, fit, _ in components) / total_weight
    reasons = [reason for _, _, reason in components]

    return round(score, 4), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    scored.sort(key=lambda item: item[1], reverse=True)
    return scored[:k]
