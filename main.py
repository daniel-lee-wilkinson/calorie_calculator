import streamlit as st

def calorie_target(
    steps=0,
    zwift_minutes=0,
    jog_km=0,
    gym_minutes=0,
    bike_commute_km=0,
    base_intake=1500,
    eatback_factor=0.5
):
    step_burn = 0.04 * steps
    zwift_burn = 8 * zwift_minutes
    jog_burn = 65 * jog_km
    gym_burn = 6 * gym_minutes
    commute_burn = 25 * (bike_commute_km / 2)

    total_burn = step_burn + zwift_burn + jog_burn + gym_burn + commute_burn
    adjusted_intake = base_intake + (total_burn * eatback_factor)

    return round(adjusted_intake), {
        "Step Burn": round(step_burn),
        "Zwift Burn": round(zwift_burn),
        "Jog Burn": round(jog_burn),
        "Gym Burn": round(gym_burn),
        "Bike Commute Burn": round(commute_burn),
        "Total Burn": round(total_burn),
        "Net Calorie Target": round(adjusted_intake)
    }

st.title("Daily Calorie Target Calculator")

steps = st.number_input("Steps walked today", min_value=0, value=10000, step=500)
zwift_minutes = st.number_input("Minutes of Zwift", min_value=0, value=0, step=5)
jog_km = st.number_input("Kilometers jogged (at ~11 km/h)", min_value=0.0, value=0.0, step=0.5)
gym_minutes = st.number_input("Minutes of strength training", min_value=0, value=0, step=5)
bike_commute_km = st.number_input("Total bike commute distance (km)", min_value=0.0, value=0.0, step=1.0)

base_intake = st.slider("Base calorie target (rest day)", min_value=1300, max_value=1700, value=1500, step=50)
eatback_factor = st.slider("% of activity calories to eat back", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

if st.button("Calculate Target"):
    target, breakdown = calorie_target(
        steps=steps,
        zwift_minutes=zwift_minutes,
        jog_km=jog_km,
        gym_minutes=gym_minutes,
        bike_commute_km=bike_commute_km,
        base_intake=base_intake,
        eatback_factor=eatback_factor
    )

    st.subheader(f"Suggested Calorie Target: {target} kcal")
    st.write("Breakdown:")
    st.json(breakdown)
