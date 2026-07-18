"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import textwrap

try:
    from tabulate import tabulate
    HAS_TABULATE = True
except ModuleNotFoundError:
    HAS_TABULATE = False

try:
    from recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    from src.recommender import load_songs, recommend_songs


USER_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
    # Edge case: conflicting preferences (sad mood + near-max energy target)
    "Sad but Wired": {"genre": "blues", "mood": "sad", "energy": 0.95},
}


def print_recommendations(profile_name: str, user_prefs: dict, songs: list) -> None:
    print(f"\n=== {profile_name} ===")
    if user_prefs:
        profile_str = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
        print(f"User profile: {profile_str}")
    else:
        print("User profile: (empty — no preferences given)")

    recommendations = recommend_songs(user_prefs, songs, k=5)
    print("\nTop recommendations:\n")

    headers = ["Rank", "Song", "Score", "Reason"]
    rows = []
    for i, rec in enumerate(recommendations, start=1):
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        wrapped_reason = "\n".join(textwrap.wrap(explanation, width=45)) or ""
        rows.append([i, song["title"], f"{score:.2f}", wrapped_reason])

    if HAS_TABULATE:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
    else:
        col_widths = [
            max(len(str(headers[i])), *(len(line) for row in rows for line in str(row[i]).split("\n")))
            for i in range(len(headers))
        ]
        border = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

        def fmt_row(cells):
            split_cells = [str(c).split("\n") for c in cells]
            height = max(len(c) for c in split_cells)
            lines = []
            for line_i in range(height):
                parts = [
                    f" {(cell[line_i] if line_i < len(cell) else '').ljust(col_widths[i])} "
                    for i, cell in enumerate(split_cells)
                ]
                lines.append("|" + "|".join(parts) + "|")
            return "\n".join(lines)

        print(border)
        print(fmt_row(headers))
        print(border)
        for row in rows:
            print(fmt_row(row))
            print(border)


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in USER_PROFILES.items():
        print_recommendations(profile_name, user_prefs, songs)


if __name__ == "__main__":
    main()
