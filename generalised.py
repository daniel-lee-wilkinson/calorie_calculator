import streamlit as st
import pandas as pd
import altair as alt
from math import ceil

st.set_page_config(
    page_title="🎯 Calorie Target Calculator",
    page_icon="🏃‍♂️",
    layout="centered",
)

# ------------------- Global Style Tweaks -------------------
st.markdown(
    """
    <style>
    body {background: #f9fafb;}
    .stNumberInput > div > div {border-radius:0.75rem;}
    .stButton>button {background-color:#2563eb;color:white;border-radius:0.5rem;}
    pre {background:#f3f4f6;padding:1rem;border-radius:0.75rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------- Core calculation -------------------

def calorie_target(
    weight: float,
    target_weight: float,
    rate_per_week: float,
    steps: int = 0,
    zwift_minutes: int = 0,
    jog_km: float = 0.0,
    jog_kph: float = 11.0,
    gym_minutes: int = 0,
    bike_commute_km: float = 0.0,
):
    """Return suggested intake, BMR and breakdown dict."""

    bmr = 22 * weight
    maintenance = bmr * 1.45

    weekly_deficit = 7700 * rate_per_week
    daily_deficit = weekly_deficit / 7

    # Activity burns
    step_burn = 0.04 * steps
    zwift_burn = 8 * zwift_minutes
    jog_burn = jog_km * 65 * (jog_kph / 11.0)
    gym_burn = 6 * gym_minutes
    commute_burn = 25 * (bike_commute_km / 2)

    activity_burn = step_burn + zwift_burn + jog_burn + gym_burn + commute_burn

    suggested_intake = maintenance - daily_deficit + (activity_burn * 0.5)

    return (
        ceil(suggested_intake),
        round(bmr),
        {
            "Maintenance": round(maintenance),
            "Daily Deficit": round(daily_deficit),
            "Step Burn": round(step_burn),
            "Zwift Burn": round(zwift_burn),
            "Jog Burn": round(jog_burn),
            "Gym Burn": round(gym_burn),
            "Bike Commute Burn": round(commute_burn),
            "Total Activity Burn": round(activity_burn),
            "Net Calorie Target": ceil(suggested_intake),
        },
    )

# ------------------- Sidebar Inputs -------------------
with st.sidebar:
    st.header("📝 Enter your details")
    weight = st.number_input("Current weight (kg)", min_value=40.0, max_value=150.0, value=65.0, step=0.5)
    target_weight = st.number_input("Target weight (kg)", min_value=40.0, max_value=150.0, value=62.0, step=0.5)
    rate_per_week = st.slider("Desired weight loss per week (kg)", 0.1, 1.0, 0.25, 0.05)

    st.divider()
    st.subheader("🏃‍♀️ Today's Activity")
    steps = st.number_input("Steps walked", min_value=0, value=10000, step=500)
    zwift_minutes = st.number_input("Zwift cycling (mins)", min_value=0, value=0, step=5)
    jog_km = st.number_input("Jog distance (km)", min_value=0.0, value=0.0, step=0.5)
    jog_kph = st.number_input("Avg jog speed (km/h)", min_value=6.0, max_value=16.0, value=11.0, step=0.5)
    gym_minutes = st.number_input("Strength‑training (mins)", min_value=0, value=0, step=5)
    bike_commute_km = st.number_input("Bike commute (km)", min_value=0.0, value=0.0, step=1.0)

    calculate = st.button("💡 Calculate target", type="primary")

# ------------------- Results -------------------
if calculate:
    target, bmr, breakdown = calorie_target(
        weight,
        target_weight,
        rate_per_week,
        steps,
        zwift_minutes,
        jog_km,
        jog_kph,
        gym_minutes,
        bike_commute_km,
    )

    # ⭐ Emphasised target intake
    st.markdown(
        f"<div style='font-size:2.4rem;font-weight:800;color:#dc2626;'>🎯 Target intake: {target} kcal</div>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("🔥 BMR", f"{bmr} kcal")
    col2.metric("📉 Daily deficit", f"{breakdown['Daily Deficit']} kcal")
    col3.metric("🚴‍♂️ Total activity", f"{breakdown['Total Activity Burn']} kcal")

    if target < bmr:
        st.warning(
            f"⚠️ Your target ({target} kcal) is below your estimated BMR ({bmr} kcal)."
        )

    st.divider()
    st.subheader("📊 Activity burn breakdown (by activity)")

    # DataFrame excluding Total Activity
    burns_df = pd.DataFrame(
        {
            "Activity": [k.replace(" Burn", "") for k in breakdown if k.endswith("Burn") and k != "Total Activity Burn"],
            "kcal": [v for k, v in breakdown.items() if k.endswith("Burn") and k != "Total Activity Burn"],
        }
    ).sort_values("kcal", ascending=False)

    chart = (
        alt.Chart(burns_df)
        .mark_bar()
        .encode(
            x=alt.X("kcal:Q", title="Calories (kcal)"),
            y=alt.Y("Activity:N", sort="-x", title="Activity"),
            tooltip=["Activity", "kcal"],
        )
        .properties(height=300)
    )
    st.altair_chart(chart, use_container_width=True)

    with st.expander("🔍 Full breakdown"):
        st.json(breakdown)

# ------------------- Footer -------------------
st.caption("Made with ❤️ using Streamlit | Calculations are estimates and should not be taken as medical advice.")
