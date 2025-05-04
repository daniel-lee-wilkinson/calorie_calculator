# 🎯 Calorie Target Calculator

A Streamlit web app that helps you estimate a *daily calorie target* for gradual weight loss, taking into account both your basal needs and the calories you burn through common activities (steps, Zwift, outdoor cycling, jogging, gym work, etc.).

---
## 🤔 Why this app?
Until now I have relied on **Garmin → MyFitnessPal** to log workouts and calories, but noticed my **calorie‑burn numbers were consistently inflated**. Eating every “earned” calorie back stalled my weight‑loss progress. This app gives me a **conservative, transparent target** by:
1. **Starting from BMR + activity factor**
2. **Discounting exercise calories** (only 50 % are added back) to protect the deficit.
3. Letting me **tweak multipliers** so I can dial down any source I know is over‑optimistic.

Now I can plan the day’s food around *planned* or *actual* sport without accidentally wiping out the deficit.

---
## ✨ Features

| Feature | Details |
|---------|---------|
| **Personalised inputs** | Current & target weight, desired weight‑loss rate, and today’s activities |
| **Instant feedback** | Key numbers (Target Intake, BMR, Daily Deficit, Activity Burn) shown as colourful live metrics |
| **Activity breakdown** | Horizontal bar‑chart plus JSON breakdown of each burn component |
| **Safety guard** | Warns if your target intake drops below your estimated BMR |
| **Acronym helper** | Clickable expander explains BMR, kcal, deficit, etc. |
| **Clean UI** | Pastel theme, rounded widgets, single‑page layout with sidebar inputs |

---
## 🚀 Quick start

### 1. Clone & install
```bash
# clone the repo
git clone https://github.com/your‑username/calorie‑target‑calc.git
cd calorie‑target‑calc

# (optional) create a virtualenv
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# install deps
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py          # or whatever the filename is
```
Visit the local URL shown in your terminal (usually `http://localhost:8501`).

---
## 🖱️ How to use
1. Enter **current weight**, **target weight**, and **desired weekly loss** in the sidebar.  
2. Log today’s **steps**, **Zwift minutes**, **outdoor ride minutes** (and choose Easy/Moderate/Hard), **jog distance & speed**, and **gym time**.  
3. Click **“💡 Calculate target”**.  
4. Review your *Target intake* (bold red number) along with BMR, daily deficit, and activity burn.  
5. Expand the charts and acronym helper as needed.

> **Tip:** A sustainable weight‑loss rate is ~0.25–0.75 kg/week. If the app warns your target is below BMR, consider reducing the rate.
---

![](target_calorie_calculator.gif)

---
## 🔬 Calculation logic (Mifflin‑St Jeor, simplified)

* **BMR** ≈ `22 × weight (kg)`  
* **Maintenance** = `BMR × 1.45` (light–moderate activity factor)  
* **Deficit needed** = `rate_per_week × 7700 kcal` per week  
* **Daily deficit** = `weekly_deficit / 7`  

### Activity calorie formulas

| Activity | Formula |
|----------|---------|
| Steps | `0.04 × steps` |
| Zwift cycling | `8 × minutes` |
| Outdoor cycling | `minutes × factor (5,7,10)` picked by effort |
| Jogging | `km × 65 × (speed/11 km/h)` |
| Strength training | `6 × minutes` |

**Suggested intake** = `maintenance − daily_deficit + 0.5 × activity_burn`  
(The 50 % factor assumes you “eat back” half of exercise calories.)

---
## 📦 Dependencies
* Python ≥ 3.9  
* Streamlit  
* pandas  
* altair & vega‑datasets (for charts)  

Install via `pip install -r requirements.txt`.

---
## 🛠️ Customising
* **Change activity multipliers** in `calorie_target()` to better match your devices.  
* **Add new activities** by extending the inputs and formulas.  
* **Theming** — edit the CSS block near the top or tweak `st.set_page_config()`.  

---
## ⚠️ Disclaimer
This tool provides *estimates* only. Always consult a healthcare professional before making significant changes to diet or exercise.
