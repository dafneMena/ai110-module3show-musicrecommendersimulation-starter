# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **MoodMatch 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
A ranked top-5 list of songs from a fixed catalog, each with a plain-language reason for why it fits.
- What assumptions does it make about the user  
That the user can state their taste as a genre, mood, and target energy level (plus optionally an acoustic preference), and that these traits alone capture what they want.
- Is this for real users or classroom exploration  
Classroom exploration — the catalog is small and hand-labeled, meant for learning how weighted scoring works, not for production use.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
Genre, mood, energy, and acousticness.
- What user preferences are considered  
Favorite genre, favorite mood, target energy level, and (optionally) whether the user likes acoustic sound.
- How does the model turn those into a score  
Each preference gets a "how well does this song fit?" score from 0 to 1, then those are combined into one weighted average — genre and mood matter most, energy and acoustic fit matter a bit less.
- What changes did you make from the starter logic  
Made energy and acousticness "how close" scores instead of strict yes/no matches, and if a user skips a preference, the other weights stretch to fill the gap so the score is still fair.


---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
18 songs.
- What genres or moods are represented  
15 genres - pop, lofi, rock, ambient, jazz, synthwave, indie pop, folk, metal, r&b, latin, blues, edm, country, classical 

14 moods - happy, chill, intense, relaxed, moody, focused, nostalgic, angry, romantic, playful, sad, euphoric, wistful, serene.
- Did you add or remove data  
No — used the provided CSV as is.
- Are there parts of musical taste missing in the dataset  
Yes there is no hip-hop/rap, and most genres have only one song, so there's little variety within a genre and no way to test finer sub-genre or artist preferences.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
Users whose genre, mood, and energy preference are all consistent with each other, like High-Energy Pop or Chill Lofi.
- Any patterns you think your scoring captures correctly  
Treating energy as a "how close" fit rather than a strict match, so a song doesn't get zeroed out just for being slightly off-target.
- Cases where the recommendations matched your intuition  
Chill Lofi's and Deep Intense Rock's top picks were exactly the songs I'd have picked by hand, near perfect genre, mood, and energy fit.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
Tempo, valence, and danceability are loaded from the CSV but never used in scoring.
- Genres or moods that are underrepresented  
Most genres (metal, classical, country, blues, latin, jazz, folk, edm) have only one song each, so a fan of those gets just one real match.
- Cases where the system overfits to one preference  
Genre+mood are exact-match booleans worth 0.60 combined weight, so they can override a badly-fitting energy score (seen in the Sad but Wired test).
- Ways the scoring might unintentionally favor some users  
Genre/mood matching is case- and spelling-exact, so a user typing "Pop" instead of "pop" scores zero on that trait with no warning.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
**High-Energy Pop**, **Chill Lofi**, and **Deep Intense Rock**, plus one adversarial profile, **Sad but Wired** 
- What you looked for in the recommendations  
Whether the #1 result was a genre+mood match, and whether score gaps between ranks made sense.
- What surprised you  
Sad but Wired (sad mood + 0.95 energy) still ranked the low-energy blues/sad song first at 0.81, since genre+mood weight (0.60) outweighs the energy mismatch.
- Any simple tests or comparisons you ran  
Compared normal vs. adversarial profiles: normal ones score near perfect at #1, the adversarial one scores lower but still wins decisively, showing the model averages preferences rather than flagging conflicts.

User profile outputs: 
---
```
=== High-Energy Pop ===
User profile: genre=pop, mood=happy, energy=0.85

Top recommendations:
+------+------------------+-------+-----------------------------------------------+
| Rank | Song             | Score | Reason                                        |
+------+------------------+-------+-----------------------------------------------+
| 1    | Sunrise City     | 0.99  | Genre matches your favorite (pop); Mood       |
|      |                  |       | matches your favorite (happy); Energy (0.82)  |
|      |                  |       | is close to your target (0.85)                |
+------+------------------+-------+-----------------------------------------------+
| 2    | Gym Hero         | 0.68  | Genre matches your favorite (pop); Mood       |
|      |                  |       | (intense) differs from your favorite (happy); |
|      |                  |       | Energy (0.93) is close to your target (0.85)  |
+------+------------------+-------+-----------------------------------------------+
| 3    | Rooftop Lights   | 0.56  | Genre (indie pop) differs from your favorite  |
|      |                  |       | (pop); Mood matches your favorite (happy);    |
|      |                  |       | Energy (0.76) is close to your target (0.85)  |
+------+------------------+-------+-----------------------------------------------+
| 4    | Carnival Sundown | 0.28  | Genre (latin) differs from your favorite      |
|      |                  |       | (pop); Mood (playful) differs from your       |
|      |                  |       | favorite (happy); Energy (0.80) is close to   |
|      |                  |       | your target (0.85)                            |
+------+------------------+-------+-----------------------------------------------+
| 5    | Storm Runner     | 0.28  | Genre (rock) differs from your favorite       |
|      |                  |       | (pop); Mood (intense) differs from your       |
|      |                  |       | favorite (happy); Energy (0.91) is close to   |
|      |                  |       | your target (0.85)                            |
+------+------------------+-------+-----------------------------------------------+

=== Chill Lofi ===
User profile: genre=lofi, mood=chill, energy=0.35

Top recommendations:

+------+---------------------+-------+-----------------------------------------------+
| Rank | Song                | Score | Reason                                        |
+------+---------------------+-------+-----------------------------------------------+
| 1    | Library Rain        | 1.00  | Genre matches your favorite (lofi); Mood      |
|      |                     |       | matches your favorite (chill); Energy (0.35)  |
|      |                     |       | is close to your target (0.35)                |
+------+---------------------+-------+-----------------------------------------------+
| 2    | Midnight Coding     | 0.98  | Genre matches your favorite (lofi); Mood      |
|      |                     |       | matches your favorite (chill); Energy (0.42)  |
|      |                     |       | is close to your target (0.35)                |
+------+---------------------+-------+-----------------------------------------------+
| 3    | Focus Flow          | 0.69  | Genre matches your favorite (lofi); Mood      |
|      |                     |       | (focused) differs from your favorite (chill); |
|      |                     |       | Energy (0.40) is close to your target (0.35)  |
+------+---------------------+-------+-----------------------------------------------+
| 4    | Spacewalk Thoughts  | 0.57  | Genre (ambient) differs from your favorite    |
|      |                     |       | (lofi); Mood matches your favorite (chill);   |
|      |                     |       | Energy (0.28) is close to your target (0.35)  |
+------+---------------------+-------+-----------------------------------------------+
| 5    | Coffee Shop Stories | 0.29  | Genre (jazz) differs from your favorite       |
|      |                     |       | (lofi); Mood (relaxed) differs from your      |
|      |                     |       | favorite (chill); Energy (0.37) is close to   |
|      |                     |       | your target (0.35)                            |
+------+---------------------+-------+-----------------------------------------------+

=== Deep Intense Rock ===
User profile: genre=rock, mood=intense, energy=0.9

Top recommendations:

+------+-----------------+-------+-----------------------------------------------+
| Rank | Song            | Score | Reason                                        |
+------+-----------------+-------+-----------------------------------------------+
| 1    | Storm Runner    | 1.00  | Genre matches your favorite (rock); Mood      |
|      |                 |       | matches your favorite (intense); Energy       |
|      |                 |       | (0.91) is close to your target (0.90)         |
+------+-----------------+-------+-----------------------------------------------+
| 2    | Gym Hero        | 0.58  | Genre (pop) differs from your favorite        |
|      |                 |       | (rock); Mood matches your favorite (intense); |
|      |                 |       | Energy (0.93) is close to your target (0.90)  |
+------+-----------------+-------+-----------------------------------------------+
| 3    | Skyline Anthem  | 0.28  | Genre (edm) differs from your favorite        |
|      |                 |       | (rock); Mood (euphoric) differs from your     |
|      |                 |       | favorite (intense); Energy (0.95) is close to |
|      |                 |       | your target (0.90)                            |
+------+-----------------+-------+-----------------------------------------------+
| 4    | Crimson Warpath | 0.27  | Genre (metal) differs from your favorite      |
|      |                 |       | (rock); Mood (angry) differs from your        |
|      |                 |       | favorite (intense); Energy (0.97) is close to |
|      |                 |       | your target (0.90)                            |
+------+-----------------+-------+-----------------------------------------------+
| 5    | Sunrise City    | 0.27  | Genre (pop) differs from your favorite        |
|      |                 |       | (rock); Mood (happy) differs from your        |
|      |                 |       | favorite (intense); Energy (0.82) is close to |
|      |                 |       | your target (0.90)                            |
+------+-----------------+-------+-----------------------------------------------+

=== Sad but Wired ===
User profile: genre=blues, mood=sad, energy=0.95

Top recommendations:

+------+-----------------+-------+-----------------------------------------------+
| Rank | Song            | Score | Reason                                        |
+------+-----------------+-------+-----------------------------------------------+
| 1    | Empty Chair     | 0.81  | Genre matches your favorite (blues); Mood     |
|      |                 |       | matches your favorite (sad); Energy (0.30) is |
|      |                 |       | somewhat different from your target (0.95)    |
+------+-----------------+-------+-----------------------------------------------+
| 2    | Skyline Anthem  | 0.29  | Genre (edm) differs from your favorite        |
|      |                 |       | (blues); Mood (euphoric) differs from your    |
|      |                 |       | favorite (sad); Energy (0.95) is close to     |
|      |                 |       | your target (0.95)                            |
+------+-----------------+-------+-----------------------------------------------+
| 3    | Gym Hero        | 0.29  | Genre (pop) differs from your favorite        |
|      |                 |       | (blues); Mood (intense) differs from your     |
|      |                 |       | favorite (sad); Energy (0.93) is close to     |
|      |                 |       | your target (0.95)                            |
+------+-----------------+-------+-----------------------------------------------+
| 4    | Crimson Warpath | 0.29  | Genre (metal) differs from your favorite      |
|      |                 |       | (blues); Mood (angry) differs from your       |
|      |                 |       | favorite (sad); Energy (0.97) is close to     |
|      |                 |       | your target (0.95)                            |
+------+-----------------+-------+-----------------------------------------------+
| 5    | Storm Runner    | 0.28  | Genre (rock) differs from your favorite       |
|      |                 |       | (blues); Mood (intense) differs from your     |
|      |                 |       | favorite (sad); Energy (0.91) is close to     |
|      |                 |       | your target (0.95)                            |
+------+-----------------+-------+-----------------------------------------------+ 

```
---



## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
Use tempo, valence, and danceability, which are already loaded but currently unused, plus let users list a secondary genre or mood instead of just one.
- Better ways to explain recommendations  
Flag when a profile's own preferences conflict (e.g. sad mood + high energy) instead of silently averaging them away.
- Improving diversity among the top results  
Cap how many songs from the same artist can appear in one top-5 list.
- Handling more complex user tastes  
Allow a list of acceptable genres/moods instead of one exact string, so near-matches (e.g. "indie pop" for a "pop" fan) aren't scored as a complete miss.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
A recommender is really just a weighted average dressed up as understanding a user the weights, not some deeper logic, decide what matters most.
- Something unexpected or interesting you discovered  
Feeding it a self contradictory profile (sad mood + high energy) didn't break it or return low scores across the board it just picked the best available compromise and stated it confidently.
- How this changed the way you think about music recommendation apps  
A "great match" score doesn't mean the app understood your mood it might just mean two out of three traits matched and the third got averaged away.
