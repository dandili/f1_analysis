import fastf1
import fastf1.plotting
from matplotlib import pyplot as plt
import numpy as np

fastf1.plotting.setup_mpl(misc_mpl_mods=False)

# Load the race session
session = fastf1.get_session(2022, "Dutch", 'R')
session.load()
laps = session.laps

# Get the list of driver numbers
drivers = session.drivers

# Convert the driver numbers to three letter abbreviations
drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]

# Group laps by driver, stint, and compound to find stint length and average lap time
stints = laps[["Driver", "Stint", "Compound", "LapNumber", "LapTime"]]
stints = stints.groupby(["Driver", "Stint", "Compound"])
stints_agg = stints.agg({"LapNumber": "count", "LapTime": "mean"}).reset_index()

# Rename columns for clarity
stints_agg = stints_agg.rename(columns={"LapNumber": "StintLength", "LapTime": "AvgLapTime"})

# Plot the strategies for each driver
fig, ax = plt.subplots(figsize=(5, 10))

for driver in drivers:
    driver_stints = stints_agg.loc[stints_agg["Driver"] == driver]

    previous_stint_end = 0
    for idx, row in driver_stints.iterrows():
        # Draw horizontal bars representing each stint
        plt.barh(
            y=driver,
            width=row["StintLength"],
            left=previous_stint_end,
            color=fastf1.plotting.COMPOUND_COLORS[row["Compound"]],
            edgecolor="black",
            fill=True
        )

        # Display the average lap time in the middle of the stint
        stint_midpoint = previous_stint_end + row["StintLength"] / 2
        avg_lap_time_str = str(np.timedelta64(row["AvgLapTime"], 's').astype(str))
        plt.text(stint_midpoint, driver, avg_lap_time_str, ha='center', va='center', color='black', fontsize=8)

        previous_stint_end += row["StintLength"]

# Plot aesthetics
plt.title("2023 British Grand Prix Tyre Strategies")
plt.xlabel("Lap Number")
plt.grid(False)
ax.invert_yaxis()  # invert the y-axis so drivers that finish higher are closer to the top
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
plt.tight_layout()
plt.show()
