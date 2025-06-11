import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    gearless = pd.read_csv("gearless_motors_final.csv")
    geared = pd.read_csv("geared_motors_final.csv")
    return gearless, geared

def calculate_capacity(passengers, avg_weight=68):
    return passengers * avg_weight

def calculate_travel(floors, height_per_floor=3):
    return (floors + 1) * height_per_floor

def filter_motors(df, capacity, speed, travel, roping):
    df = df[(df["Capacity_KG"] >= capacity) & (df["Speed_mps"] >= speed)]
    if "Max_Travel_m" in df.columns:
        df = df[df["Max_Travel_m"] >= travel]
    if roping != "Any":
        df = df[df["Roping"] == roping]
    return df

def main():
    st.title("Montanari Motor Selector Bot")
    st.markdown("Get recommended motors based on your building specifications.")

    motor_type = st.selectbox("Motor Type", ["Both", "Gearless", "Geared"])
    roping = st.selectbox("Roping Type", ["Any", "1:1", "2:1"])
    floors = st.number_input("Enter number of floors (e.g., 5 for G+5)", min_value=1, step=1)
    passengers = st.number_input("Enter number of passengers", min_value=1, step=1)
    speed = st.selectbox("Desired speed (mps)", options=[0.5, 0.63, 0.67, 0.81, 1.0], index=4)

    if st.button("Recommend Motors"):
        gearless_df, geared_df = load_data()
        required_capacity = calculate_capacity(passengers)
        travel_height = calculate_travel(floors)

        if motor_type in ["Both", "Gearless"]:
            g_filtered = filter_motors(gearless_df, required_capacity, speed, travel_height, roping)
            st.subheader("Gearless Motor Options")
            if not g_filtered.empty:
                st.dataframe(g_filtered)
            else:
                st.warning("No suitable gearless motors found.")

        if motor_type in ["Both", "Geared"]:
            gr_filtered = filter_motors(geared_df, required_capacity, speed, travel_height, roping)
            st.subheader("Geared Motor Options")
            if not gr_filtered.empty:
                st.dataframe(gr_filtered)
            else:
                st.warning("No suitable geared motors found.")

if __name__ == "__main__":
    main()
