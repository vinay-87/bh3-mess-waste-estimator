"""
BH3 Mess Food Waste Analyzer — IIIT Allahabad
================================================
Reads daily mess data (item, prepared qty, leftover qty, attendance)
and spits out waste patterns + actionable suggestions for the cook.

Usage:
    python mess_waste_analyzer.py                     # full analysis
    python mess_waste_analyzer.py Friday dinner        # suggest prep for a specific meal
"""

import pandas as pd
import sys

# ---- cost assumption (avg raw material cost per kg) ----
COST_PER_KG = 45  # rough average across rice/dal/sabzi in bulk


def load_data(filepath="data.csv"):
    """Load csv, compute derived columns, basic validation."""
    df = pd.read_csv(filepath)

    # basic checks
    required = ["date", "meal", "day", "item", "qty_prepared_kg", "qty_leftover_kg", "students_present"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"ERROR: missing columns in csv: {missing}")
        sys.exit(1)

    if len(df) < 20:
        print(f"WARNING: only {len(df)} rows — patterns may be unreliable")

    df["consumed_kg"] = df["qty_prepared_kg"] - df["qty_leftover_kg"]
    df["waste_pct"] = (df["qty_leftover_kg"] / df["qty_prepared_kg"] * 100).round(1)
    return df


def print_header(title):
    print("\n" + "=" * 62)
    print(f"  {title}")
    print("=" * 62)


def overall_summary(df):
    total_prep = df["qty_prepared_kg"].sum()
    total_left = df["qty_leftover_kg"].sum()
    total_eaten = total_prep - total_left
    waste_rate = total_left / total_prep * 100

    print_header("OVERALL SUMMARY")
    print(f"  Data period       : {df['date'].min()} → {df['date'].max()}")
    print(f"  Total entries     : {len(df)}")
    print(f"  Food prepared     : {total_prep:.1f} kg")
    print(f"  Food consumed     : {total_eaten:.1f} kg")
    print(f"  Food wasted       : {total_left:.1f} kg")
    print(f"  Waste rate        : {waste_rate:.1f}%")
    print(f"  Est. weekly cost of waste : Rs {total_left * COST_PER_KG:.0f}")


def item_analysis(df):
    """Which items waste the most?"""
    print_header("WASTE BY ITEM")

    stats = (
        df.groupby("item")
        .agg(
            times=("item", "count"),
            avg_prep=("qty_prepared_kg", "mean"),
            avg_left=("qty_leftover_kg", "mean"),
            avg_waste=("waste_pct", "mean"),
        )
        .round(1)
        .sort_values("avg_waste", ascending=False)
    )

    print(f"\n  {'Item':<26}{'Times':>6}{'Avg Prep':>10}{'Avg Left':>10}{'Waste%':>8}")
    print("  " + "-" * 60)
    for item, r in stats.iterrows():
        flag = " !!!" if r["avg_waste"] > 35 else ""
        print(
            f"  {item:<26}{int(r['times']):>6}{r['avg_prep']:>10}{r['avg_left']:>10}{r['avg_waste']:>8}{flag}"
        )
    return stats


def day_analysis(df):
    """Which days waste the most?"""
    print_header("WASTE BY DAY OF WEEK")

    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    stats = (
        df.groupby("day")
        .agg(
            avg_waste=("waste_pct", "mean"),
            avg_students=("students_present", "mean"),
            total_left=("qty_leftover_kg", "sum"),
        )
        .round(1)
    )
    stats = stats.reindex([d for d in day_order if d in stats.index])

    print(f"\n  {'Day':<14}{'Avg Waste%':>11}{'Avg Students':>14}{'Total Left kg':>15}")
    print("  " + "-" * 54)
    for day, r in stats.iterrows():
        flag = " !!!" if r["avg_waste"] > 25 else ""
        print(
            f"  {day:<14}{r['avg_waste']:>11}{r['avg_students']:>14.0f}{r['total_left']:>15}{flag}"
        )


def meal_analysis(df):
    """Breakfast vs lunch vs dinner."""
    print_header("WASTE BY MEAL TYPE")

    stats = (
        df.groupby("meal")
        .agg(
            entries=("meal", "count"),
            avg_waste=("waste_pct", "mean"),
            avg_students=("students_present", "mean"),
        )
        .round(1)
    )

    print(f"\n  {'Meal':<14}{'Entries':>8}{'Avg Waste%':>12}{'Avg Students':>14}")
    print("  " + "-" * 48)
    for meal, r in stats.iterrows():
        print(f"  {meal:<14}{int(r['entries']):>8}{r['avg_waste']:>12}{r['avg_students']:>14.0f}")


def find_worst_combos(df, top_n=5):
    """Specific day+meal+item combos with highest absolute waste."""
    print_header(f"TOP {top_n} WORST WASTE INSTANCES")

    worst = df.nlargest(top_n, "qty_leftover_kg")[
        ["date", "day", "meal", "item", "qty_prepared_kg", "qty_leftover_kg", "waste_pct"]
    ]
    print(f"\n  {'Date':<13}{'Day':<11}{'Meal':<10}{'Item':<22}{'Prep':>6}{'Left':>6}{'W%':>6}")
    print("  " + "-" * 72)
    for _, r in worst.iterrows():
        print(
            f"  {r['date']:<13}{r['day']:<11}{r['meal']:<10}{r['item']:<22}"
            f"{r['qty_prepared_kg']:>6}{r['qty_leftover_kg']:>6}{r['waste_pct']:>6}"
        )


def generate_recommendations(df):
    """The main output: actionable suggestions for Ramesh bhaiya."""
    print_header("RECOMMENDATIONS FOR THE COOK")

    # --- high waste items ---
    item_waste = df.groupby("item")["waste_pct"].mean()
    bad_items = item_waste[item_waste > 35].sort_values(ascending=False)
    if not bad_items.empty:
        print("\n  RED — Items with >35% average waste:")
        for item, pct in bad_items.items():
            avg_prep = df.loc[df["item"] == item, "qty_prepared_kg"].mean()
            avg_eaten = df.loc[df["item"] == item, "consumed_kg"].mean()
            suggested = round(avg_eaten * 1.12, 1)      # 12% buffer over actual consumption
            print(f"    • {item}: ~{pct:.0f}% wasted")
            print(f"      Currently preparing {avg_prep:.0f} kg → suggest {suggested} kg (save {avg_prep - suggested:.1f} kg)")

    # --- Friday dinner ---
    fri_d = df[(df["day"] == "Friday") & (df["meal"] == "dinner")]
    weekday_d = df[df["day"].isin(["Monday", "Tuesday", "Wednesday", "Thursday"]) & (df["meal"] == "dinner")]
    if not fri_d.empty and not weekday_d.empty:
        fri_students = fri_d["students_present"].mean()
        wd_students = weekday_d["students_present"].mean()
        drop = (1 - fri_students / wd_students) * 100
        print(f"\n  RED — Friday dinner attendance crash:")
        print(f"    Weekday dinner avg: {wd_students:.0f} students")
        print(f"    Friday dinner avg : {fri_students:.0f} students")
        print(f"    → Cut ALL Friday dinner prep by ~{drop:.0f}%")

    # --- weekend breakfast ---
    wknd_b = df[df["day"].isin(["Saturday", "Sunday"]) & (df["meal"] == "breakfast")]
    if not wknd_b.empty:
        wb_waste = wknd_b["waste_pct"].mean()
        print(f"\n  RED — Weekend breakfast: {wb_waste:.0f}% average waste")
        print(f"    → Students are sleeping in. Cut breakfast prep by 40%.")

    # --- best day ---
    day_waste = df.groupby("day")["waste_pct"].mean()
    best_day = day_waste.idxmin()
    print(f"\n  GREEN — Best day: {best_day} ({day_waste[best_day]:.0f}% waste)")
    # find what items were served on best day
    best_items = df[df["day"] == best_day]["item"].unique()
    print(f"    Menu that day: {', '.join(best_items)}")
    print(f"    → Consider repeating popular items on high-waste days")

    # --- money ---
    weekly_waste_kg = df["qty_leftover_kg"].sum()
    saveable = weekly_waste_kg * 0.45   # realistic: can cut ~45% of waste
    print(f"\n  SAVINGS POTENTIAL:")
    print(f"    Current weekly waste : {weekly_waste_kg:.1f} kg ≈ Rs {weekly_waste_kg * COST_PER_KG:.0f}")
    print(f"    If we cut waste by 45%: save ~{saveable:.0f} kg/week ≈ Rs {saveable * COST_PER_KG:.0f}/week")
    print(f"    That's roughly Rs {saveable * COST_PER_KG * 4:.0f}/month back into the mess budget")


def suggest_quantities(df, target_day, target_meal="lunch"):
    """Given a day and meal, suggest how much to prepare."""
    print_header(f"SUGGESTED PREP: {target_day.upper()} {target_meal.upper()}")

    # day-level attendance factor
    day_avg = df.groupby("day")["students_present"].mean()
    overall_avg = df["students_present"].mean()
    factor = day_avg.get(target_day, overall_avg) / overall_avg

    # get items typically served at this meal
    meal_items = df[df["meal"] == target_meal].groupby("item").agg(
        avg_eaten=("consumed_kg", "mean"),
        avg_prep=("qty_prepared_kg", "mean"),
    ).round(1)

    if meal_items.empty:
        print(f"\n  No data for {target_meal}.")
        return

    print(f"\n  Attendance factor for {target_day}: {factor:.2f}x")
    print(f"\n  {'Item':<26}{'Usual Prep':>11}{'Suggested':>11}")
    print("  " + "-" * 48)
    for item, r in meal_items.iterrows():
        suggested = round(r["avg_eaten"] * factor * 1.12, 1)
        diff = r["avg_prep"] - suggested
        arrow = f"  (↓{diff:.1f} kg)" if diff > 0.5 else ""
        print(f"  {item:<26}{r['avg_prep']:>11}{suggested:>11}{arrow}")


def main():
    df = load_data()

    overall_summary(df)
    item_analysis(df)
    day_analysis(df)
    meal_analysis(df)
    find_worst_combos(df)
    generate_recommendations(df)

    # if user passes a day and meal, give specific suggestions
    if len(sys.argv) >= 2:
        target_day = sys.argv[1].capitalize()
        target_meal = sys.argv[2].lower() if len(sys.argv) >= 3 else "lunch"
        suggest_quantities(df, target_day, target_meal)
    else:
        # default: suggest for Saturday lunch (tomorrow from Friday)
        suggest_quantities(df, "Saturday", "lunch")

    print("\n" + "=" * 62)
    print("  Usage: python mess_waste_analyzer.py [day] [meal]")
    print("  Example: python mess_waste_analyzer.py Friday dinner")
    print("=" * 62 + "\n")


if __name__ == "__main__":
    main()
