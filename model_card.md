# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The most significant weakness in this system is its heavy reliance on exact genre matching. Genre accounts for 2.0 out of a maximum score of 4.80 — over 40% of the total — and it is awarded as an all-or-nothing bonus with no partial credit for similar genres. This means a user who enjoys indie pop will never be recommended a pop or soul song, even if those songs match their energy, mood, and tempo almost perfectly. The effect was visible in the "Conflicting Vibes" experiment: a classical song ranked first for a user who wanted high energy and low acousticness, simply because the genre label matched, while sonically closer songs were buried. In practice, this creates a filter bubble where the system constantly reinforces what the user already said they like, rather than surfacing music they might genuinely enjoy.

---

## 7. Evaluation  

I tested six different user profiles. Three of them were "normal" — High-Energy Pop, Chill Lofi, and Intense Rock — where the genre and mood I asked for were actually in the catalog. Those mostly made sense. The other three were edge cases I used to break things: one had totally contradicting preferences (classical music but extreme energy), one asked for a genre that doesn't exist in the catalog (reggae), and one just set everything to the middle.

The normal profiles worked pretty much how I expected. The lofi profile in particular gave really confident results — the top two songs were almost identical in score, which makes sense since the catalog has three lofi songs that all fit well.

What surprised me the most was the Conflicting Vibes profile. The user wanted classical music but also wanted really high energy (0.95) and low acousticness — basically the opposite of what classical songs sound like. I expected the system to pick something high-energy, but instead it gave Morning Sonata the top spot just because the genre matched. That felt wrong, and it helped me see how much the genre bonus can overpower everything else.

The reggae/missing genre profile was also interesting. When there's no genre match at all, the top 5 results were all super close in score — like 1.46 to 1.59. That basically means the system has no idea what to recommend and is just guessing based on energy values.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
