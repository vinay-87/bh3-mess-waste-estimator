# AI Chat: Data Structure

## Context
Quick chat about how to structure the CSV columns before going to collect data.

---

**Me:** What columns should I use for tracking mess food waste? Going to visit BH3 mess, talk to the cook, and also observe a couple of meals directly.

**AI:** Suggested:
- date (YYYY-MM-DD format)
- meal (breakfast/lunch/dinner)
- day (day of week — handy for pattern analysis since your menu repeats weekly)
- item (food item name)
- qty_prepared_kg
- qty_leftover_kg
- students_present (count or estimate)
- notes (free text for context — useful for flagging outliers)

**Me:** Should I track individual plates? Like how much each student takes and wastes?

**AI:** That would give much richer data but practically impossible in a mess with 200 students and no weighing station. Aggregate quantities (total prep vs total leftover) is what you can realistically get from the cook. You could do plate-level if you sat at the disposal counter and weighed each plate but that's a full-day job for one meal.

**Me:** Aggregate it is. The cook estimates quantities by looking at containers, he should be reasonably accurate after 6 years of doing this.

---

*Short chat. The notes column suggestion ended up being actually useful — I used it to add context like "literally nobody eats kaddu" and "chole bhature is king" which made the data more readable.*
