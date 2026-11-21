# Research — BH3 Mess Food Waste at IIIT Allahabad

## The Problem (5 lines)

BH3 mess at IIITA is run by KMK Global Limited and feeds around 200 students every day — breakfast, lunch, dinner. The issue is that they cook the exact same quantities every single day no matter how many people actually show up to eat. Friday nights half the hostel leaves for the weekend but the cook still makes 20 kg rice, and whenever something like kaddu sabzi or soyabean is on the menu it comes back almost untouched. I've literally watched full containers of leftover sabzi getting dumped after dinner multiple times. The cook knows all this — he's been here for years — but the weekly menu is fixed by the mess committee and KMK procures materials on a weekly contract so nobody adjusts anything. We're just burning through the mess fund on food nobody eats.

## 2 Existing Solutions and Why They Don't Fit

### 1. Enterprise food waste platforms (Winnow, Leanpath)
These are professional kitchen waste tracking systems — smart scales under bins, cameras on serving lines, AI dashboards. They cost thousands of dollars and are designed for hotel chains and airline caterers. Our mess is run by a contractor (KMK Global) with a head cook who doesn't use a smartphone. The entire kitchen operates on verbal instructions and mental estimation. We don't need a smart scale, we need a simple printed sheet that says "Thursday dinner: make 13 kg aloo-pattagobhi not 20, it'll come back anyway."

### 2. FSSAI Save Food Share Food / Too Good To Go apps
These focus on redistributing surplus food after it's already been cooked — connecting leftover food with NGOs or discounted buyers. That solves the disposal problem, not the prevention problem. Our cook doesn't need help giving away leftovers, he needs to know how much to cook in the first place. And honestly asking a 50+ year old mess worker in Prayagraj to download an app and list surplus food daily is not going to happen.

## 2 Sources I Actually Read

### Source 1: UNEP Food Waste Index Report 2024
Link: https://www.unep.org/resources/publication/food-waste-index-report-2024
- Says India wastes around 78 million tonnes of food per year. Institutional kitchens like hostels and canteens are specifically called out as major contributors because they cook for a fixed headcount not actual demand. This is exactly what BH3 does — 200 students on paper, 105 at Friday dinner in reality.
- The report has this finding that just measuring and tracking waste for one week reduces it by 15-25% without any other changes. The act of making waste visible changes behavior. Our mess has literally zero tracking — nobody has ever counted what gets thrown away.
- Made me realise that even my basic script outputting numbers on a screen would be new information for the mess committee. The bar is that low.

### Source 2: "Food waste and its management in educational institutions" — Bharathiar University study
Link: https://www.researchgate.net/publication/341287005
- Surveyed food waste across college hostels in South India and found 25-40% of prepared food gets wasted in hostels with fixed menus and no feedback loop. Main cause wasn't bad cooking — it was mismatch between what's prepared and actual attendance combined with unpopular menu items that keep getting repeated.
- Found that unpopular items had 3x the waste rate of popular ones, but cooks kept preparing same quantity because "that's what the menu says." This is literally what happens in BH3 — kaddu and soyabean waste 40%+ but the cook makes full quantity because it's on the weekly menu card from KMK.
- Their recommendation was simple: track waste for one week, share with the mess committee, adjust quantities. No ML, no app, no hardware. Just awareness. That's basically what I'm building.
