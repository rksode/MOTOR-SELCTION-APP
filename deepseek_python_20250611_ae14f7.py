import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    gearless = pd.read_csv("gearless_motors_final.csv")
    geared = pd.read_csv("geared_motors_final.csv")
    return gearless, geared

def calculate_load(passengers, avg_weight=68):
    return passengers * avg_weight

def calculate_travel(floors, height_per_floor=3):
    return (floors + 1) * height_per_floor

def filter_motors(df, capacity, speed, travel=None, roping="Any"):
    filtered = df[(df["Capacity_KG"] >= capacity) & (df["Speed_mps"] >= speed)]
    if "Travel_Upto_m" in df.columns and travel:
        filtered = filtered[filtered["Travel_Upto_m"] >= travel]
    if roping != "Any":
        filtered = filtered[filtered["Roping"] == roping]
    return filtered

def main():
    st.title("Montanari Motor Selector")
    st.markdown("Select motors based on building requirements.")

    # User Inputs
    motor_type = st.selectbox("Motor Type", ["Both", "Gearless", "Geared"])
    roping = st.selectbox("Roping Type", ["Any", "1:1", "2:1"])
    floors = st.number_input("Number of Floors (e.g., 5 for G+5)", min_value=1, step=1)
    passengers = st.number_input("Passenger Count", min_value=1, step=1)
    speed = st.selectbox("Speed (m/s)", options=[0.5, 0.63, 0.67, 0.81, 1.0], index=4)

    if st.button("Find Motors"):
        gearless_df, geared_df = load_data()
        load = calculate_load(passengers)
        travel = calculate_travel(floors)

        # Filter and display results
        if motor_type in ["Both", "Gearless"]:
            st.subheader("Gearless Motors")
            gearless_result = filter_motors(gearless_df, load, speed, roping=roping)
            st.dataframe(gearless_result if not gearless_result.empty else "No matches found.")

        if motor_type in ["Both", "Geared"]:
            st.subheader("Geared Motors")
            geared_result = filter_motors(geared_df, load, speed, travel, roping)
            st.dataframe(geared_result if not geared_result.empty else "No matches found.")

if __name__ == "__main__":
    main()