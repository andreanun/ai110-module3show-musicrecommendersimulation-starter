# Reflection: Profile Pair Comparisons

---

## Pair 1: High-Energy Pop vs. Chill Lofi Session

These two profiles are basically opposites. Pop wants high energy (0.90), fast tempo, and low acousticness. Lofi wants low energy (0.38), slow tempo, and high acousticness.

The results flipped almost completely — no song appeared in the top 3 of both profiles. That makes sense because they're asking for totally different things.

One thing I noticed: the lofi user's top two songs (Library Rain 4.73, Midnight Coding 4.70) were much closer in score than the pop user's top two (Sunrise City 4.62, Gym Hero 3.76). That gap exists because the catalog has three lofi songs that all fit well, but only two pop songs. So lofi users get better, more competitive recommendations just because their genre has more songs — not because the system is smarter for them.

Something worth explaining about the pop results: "Gym Hero" shows up at #2 even though the user asked for "happy" mood and Gym Hero is tagged "intense." The system doesn't know that gym music and happy dance pop feel different to a real person. It just sees that Gym Hero is a pop song with 0.93 energy — very close to the target 0.90 — and gives it a high score. The genre match (+2.0) plus near-perfect energy (+0.97) gets it to 3.76, which beats every non-pop song. The math checks out, but the recommendation might feel off.

---

## Pair 2: Intense Rock vs. Conflicting Vibes

Both profiles wanted high energy (0.92 and 0.95) and low acousticness. The only real difference was the genre and mood: rock/intense vs. classical/peaceful.

The rock profile worked great. Storm Runner scored 4.77 out of 4.80 — nearly perfect. Every feature lined up: rock genre, intense mood, high energy, low acousticness. That's the system at its best.

The classical profile was a mess. Even though the user wanted extreme energy and low acousticness — which are the opposite of classical music — Morning Sonata still came out on top at 3.35. It's a quiet piano piece. It won because "classical" genre gave it +2.0 and "peaceful" mood gave it +1.0. That's 3.0 points before the system even looked at energy. The energy and acousticness scores were terrible, but they couldn't overcome the label bonus.

This comparison shows the biggest design flaw clearly. When genre and energy contradict each other, genre always wins. The numeric features don't have enough weight to override it.

---

## Pair 3: Missing Genre (Reggae) vs. Dead Center (Ambient/Focused)

Both of these were supposed to be hard edge cases, but they played out very differently.

The reggae profile got no genre bonus at all — reggae isn't in the catalog. The top 5 scores were all between 1.46 and 1.59. That's a really small range. The songs are basically ranked by which ones had energy closest to 0.65. There's no real logic to the ordering — it's almost random.

The ambient/focused profile did better than I expected. "Ambient" is actually in the catalog (Spacewalk Thoughts), so it got the genre bonus even though the user set everything to the midpoint. That gave it a clear #1 at 3.26. Then Focus Flow came in at #2 with a mood match ("focused"). So the Dead Center profile ended up with more meaningful results than the Missing Genre profile, even though both were supposed to stress-test the system.

The lesson: the quality of recommendations completely depends on whether your genre is in the catalog. If it is, you get a strong #1 with a big lead. If it isn't, the system just lines up songs by energy and calls it a recommendation.
