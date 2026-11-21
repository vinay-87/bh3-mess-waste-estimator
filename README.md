# BH3 Mess Food Waste Estimator

**A tool that analyzes food waste patterns in the BH3 hostel mess at IIIT Allahabad and suggests how much to actually cook each day.**

- **Place:** BH3 Mess, Boys Hostel 3, IIIT Allahabad (Prayagraj), Jhalwa Campus
- **Mess contractor:** KMK Global Limited
- **Person:** Suresh Yadav — head cook, 6 years at BH3
- **Date:** 15–21 November 2026
- **Author:** Vinay Kumar

## The Problem

BH3 mess cooks for 200 students every meal, but actual attendance ranges wildly — from 55 (Sunday breakfast, everyone sleeping) to 182 (Wednesday dinner, chana masala night). The weekly menu is fixed by KMK Global, the cook gets fixed raw materials from the store, and nobody adjusts quantities for predictable patterns. Friday dinners are ghost towns because students leave for the weekend, and items like kaddu sabzi, soyabean-aloo, and aloo-pattagobhi come back nearly untouched every single week. Result: ~142 kg of food wasted per week ≈ ₹6,381/week of the mess budget going straight into the bin.

The cook knows all of this. He's been here for 6 years. But nobody asks him.

## How to Run

**Requirements:** Python 3.8+, pandas

```bash
# install dependency
pip install pandas

# run full analysis (default: suggests Saturday lunch prep)
python mess_waste_analyzer.py

# suggest quantities for a specific day + meal
python mess_waste_analyzer.py Friday dinner
python mess_waste_analyzer.py Wednesday lunch
```

## What It Does

1. Reads `data.csv` — 45 entries of item-level prep/leftover data across 7 days, all from the actual BH3 weekly menu
2. Calculates waste percentages by item, day of week, and meal type
3. Identifies worst offenders — Kaddu Sabzi (45%), Aloo-Pattagobhi (45%), Soyabean-Aloo (42%)
4. Flags systemic patterns — Friday dinner has 37% attendance drop, weekend breakfast wastes 44%
5. Generates specific kg recommendations ("prepare 8.1 kg kaddu not 13 kg")
6. Estimates savings potential — ~₹11,500/month if waste is cut by 45%

## Real Output

```
==============================================================
  OVERALL SUMMARY
==============================================================
  Data period       : 2026-11-15 → 2026-11-21
  Total entries     : 45
  Food prepared     : 677.0 kg
  Food consumed     : 535.2 kg
  Food wasted       : 141.8 kg
  Waste rate        : 20.9%
  Est. weekly cost of waste : Rs 6381

==============================================================
  WASTE BY ITEM (top and bottom)
==============================================================
  Kaddu Sabzi              45% waste  !!!
  Aloo-Pattagobhi          45% waste  !!!
  Soyabean-Aloo            42% waste  !!!
  Poha                     40% waste  !!!
  Aloo Bhujiya             37% waste  !!!
  ...
  Chana Masala              6% waste
  Rajma                     6% waste
  Dal Makhni                4% waste
  Egg Curry                 4% waste
  Chole Bhature             3% waste  ← almost zero waste

==============================================================
  WASTE BY DAY OF WEEK
==============================================================
  Monday              16.3%  — 171 students avg
  Wednesday           16.0%  — 175 students avg
  Thursday            16.3%  — 164 students avg
  Tuesday             21.0%  — 160 students avg
  Sunday              23.5%  — 125 students avg
  Saturday            26.1%  — 127 students avg  !!!
  Friday              32.5%  — 117 students avg  !!!

==============================================================
  RECOMMENDATIONS FOR THE COOK
==============================================================
  RED — Kaddu Sabzi: ~45% wasted
    Currently preparing 13 kg → suggest 8.1 kg (save 4.9 kg)
  RED — Soyabean-Aloo: ~42% wasted
    Currently preparing 13 kg → suggest 8.4 kg (save 4.6 kg)

  RED — Friday dinner attendance crash:
    Weekday dinner avg: 166 students
    Friday dinner avg : 105 students
    → Cut ALL Friday dinner prep by ~37%

  RED — Weekend breakfast: 44% average waste
    → Students are sleeping in. Cut breakfast prep by 40%.

  GREEN — Best day: Wednesday (16% waste)
    → Chana masala + veg fried rice combo works. Repeat popular items.

  SAVINGS POTENTIAL:
    Current weekly waste : 141.8 kg ≈ Rs 6381
    If we cut waste by 45%: save ~64 kg/week ≈ Rs 2871/week
    That's roughly Rs 11486/month back into the mess budget
```

## What It Gets Wrong

Being honest about the limitations:

- **Only 7 days of data.** This covers one cycle of the weekly menu. Patterns might shift during exams (attendance drops), after holidays (everyone comes back), or seasonally. The numbers will get more reliable with more weeks.
- **Cook's memory isn't precise.** For days I wasn't physically present, the leftover quantities are Suresh bhaiya's estimates from memory. Some could be off by 1-2 kg.
- **Doesn't account for menu interactions.** When chole bhature is served, students eat less rice — but the tool treats each item independently. In reality, items affect each other.
- **Fixed ₹45/kg cost assumption.** Rice costs way less, chicken costs way more. The savings estimate is ballpark, not exact.
- **Can't handle one-off events.** Fests, exams, holidays — the tool doesn't know about these. Someone still needs to use common sense.
- **The "Daal" on Friday dinner shows as 43% waste** — but that's partly because only 105 students showed up. If Friday attendance was normal, daal waste would be moderate. The tool doesn't fully separate "item unpopularity" from "low attendance day."

The tool is a conversation starter for the mess committee, not a replacement for the cook's 6 years of experience.

## Screen Recording

→ [3-minute walkthrough](./screen_recording.mp4)

*(Running the script, explaining output, trying Friday dinner query, feeding a bad data row)*

## Project Structure

```
mess-waste-estimator/
├── research.md                # problem research + 2 sources
├── fieldwork.md               # visit notes, cook conversation, data method
├── data.csv                   # 45 entries — real BH3 menu items
├── mess_waste_analyzer.py     # the analysis tool
├── reflection.md              # what I learned (no AI)
├── README.md                  # you're reading this
├── photos/
│   ├── mess_dinner_rush_621pm.jpg       # dining hall during dinner
│   ├── leftover_sabzi_container_643pm.jpg  # leftover food container
│   └── bh3_weekly_menu.jpg              # official KMK menu card
├── ai-chats/                  # exported AI conversations
│   ├── README.md
│   ├── research-help.md
│   ├── code-help.md
│   └── data-structure.md
└── .gitignore
```
