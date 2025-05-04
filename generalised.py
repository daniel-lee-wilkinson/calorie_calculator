import streamlit as st

def calorie_target(
    weight,
    target_weight,
    rate_per_week,
    steps=0,
    zwift_minutes=0,
    jog_km=0,
    gym_minutes=0,
    bike_commute_km=0
):
    # Estimate BMR using Mifflin-St Jeor (simplified for this case)
    bmr = 22 * weight  # Approximate resting energy
    maintenance = bmr * 1.45  # Lightly to moderately active multiplier

    # Calculate target deficit
    weekly_deficit = 7700 * rate_per_week  # 1 kg fat ~7700 kcal
    daily_deficit = weekly_deficit / 7

    # Activity burns
    step_burn = 0.04 * steps
    zwift_burn = 8 * zwift_minutes
    jog_burn = 65 * jog_km
    gym_burn = 6 * gym_minutes
    commute_burn = 25 * (bike_commute_km / 2)

    activity_burn = step_burn + zwift_burn + jog_burn + gym_burn + commute_burn

    # Suggested intake = maintenance - deficit + 50% of activity calories
    suggested_intake = maintenance - daily_deficit + (activity_burn * 0.5)

    return round(suggested_intake), round(bmr), {
        "Maintenance": round(maintenance),
        "Daily Deficit": round(daily_deficit),
        "Step Burn": round(step_burn),
        "Zwift Burn": round(zwift_burn),
        "Jog Burn": round(jog_burn),
        "Gym Burn": round(gym_burn),
        "Bike Commute Burn": round(commute_burn),
        "Total Activity Burn": round(activity_burn),
        "Net Calorie Target": round(suggested_intake)
    }

st.title("Personalized Calorie Target Calculator")

weight = st.number_input("Current weight (kg)", min_value=40.0, max_value=150.0, value=65.0, step=0.5)
target_weight = st.number_input("Target weight (kg)", min_value=40.0, max_value=150.0, value=62.0, step=0.5)
rate_per_week = st.slider("Desired weight loss per week (kg)", min_value=0.1, max_value=1.0, value=0.25, step=0.05)

steps = st.number_input("Steps walked today", min_value=0, value=10000, step=500)
zwift_minutes = st.number_input("Minutes of Zwift", min_value=0, value=0, step=5)
jog_km = st.number_input("Kilometers jogged (at ~11 km/h)", min_value=0.0, value=0.0, step=0.5)
gym_minutes = st.number_input("Minutes of strength training", min_value=0, value=0, step=5)
bike_commute_km = st.number_input("Total bike commute distance (km)", min_value=0.0, value=0.0, step=1.0)

if st.button("Calculate Target"):
    target, bmr, breakdown = calorie_target(
        weight=weight,
        target_weight=target_weight,
        rate_per_week=rate_per_week,
        steps=steps,
        zwift_minutes=zwift_minutes,
        jog_km=jog_km,
        gym_minutes=gym_minutes,
        bike_commute_km=bike_commute_km
    )

    st.subheader(f"Suggested Calorie Target: {target} kcal")
    if target < bmr:
        st.warning(f"⚠️ Your target ({target} kcal) is below your estimated BMR ({bmr} kcal). Consider reducing your weight loss rate.")
        if st.button("Reduce weight loss rate to safe level"):
            rate_per_week = round(((bmr - (0.5 * breakdown["Total Activity Burn"])) - (bmr * 1.45)) * -7 / 7700, 2)
            st.info(f"Rate adjusted to {rate_per_week} kg/week. Recalculate to update.")

    st.write("Breakdown:")
    st.json(breakdown)
