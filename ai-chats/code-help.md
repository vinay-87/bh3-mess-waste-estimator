# AI Chat: Code Help

## Context
Used AI assistance for pandas syntax and the analysis script structure. I knew what analysis I wanted to run but needed help with groupby/agg patterns and terminal output formatting.

---

**Me:** I have a CSV with these columns: date, meal, day, item, qty_prepared_kg, qty_leftover_kg, students_present, notes. Want to find which items waste the most on average across the week.

**AI:** 
```python
df['waste_pct'] = (df['qty_leftover_kg'] / df['qty_prepared_kg'] * 100).round(1)
item_stats = df.groupby('item').agg(
    avg_waste=('waste_pct', 'mean'),
    times_served=('item', 'count'),
    avg_prep=('qty_prepared_kg', 'mean')
).sort_values('avg_waste', ascending=False)
```

**Me:** Need to group by day of week too but I want the days ordered Mon-Sun not alphabetical.

**AI:**
```python
day_order = ['Monday', 'Tuesday', ...]
stats = stats.reindex([d for d in day_order if d in stats.index])
```

**Me:** For recommendations: if an item wastes more than 35%, I want to suggest a new quantity based on actual consumption + a 12% safety buffer. Help with the logic?

**AI:** [Gave me the avg_consumed * 1.12 approach with the threshold filtering logic]

**Me:** Should I build a web dashboard with Flask? Charts would look good.

**AI:** You could use Flask + Chart.js for visualization... [went into dashboard architecture details]

**Me:** Actually nah. The cook doesn't have a computer. I need clean terminal output I can screenshot or print. Let me keep it simple.

**AI:** Fair point. Here's how to format aligned columns with f-strings...

---

**Me:** One more — I want a "suggest for tomorrow" mode where you pass a day and meal as command line args and it tells you how much to prep.

**AI:** [Gave the sys.argv handling and attendance-factor adjustment approach]

---

**Me:** It was pushing me toward linear regression at one point to "predict waste trends" which I had to shut down. 7 days of data is not enough for regression and the cook doesn't need a model, he needs a table.

---

*Basically used AI for pandas syntax and formatting. The decisions about what to analyze, what thresholds matter, what output format makes sense for the actual user (a cook) — those were mine.*
