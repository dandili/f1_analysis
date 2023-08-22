import fastf1 as ff1
import random
import pandas as pd

# Number of simulations
N_SIMULATIONS = 10000

# Initialize FastF1
ff1.Cache.enable_cache('cache')

# Load past performance data for the Dutch Grand Prix for 2021 and 2022
race_2021 = ff1.get_session(2021, "Dutch", 'R')
race_2021.load(laps=True, weather=True)
laps_2021 = race_2021.laps
weather_2021 = race_2021.weather_data

race_2022 = ff1.get_session(2022, "Dutch", 'R')
race_2022.load(laps=True, weather=True)
laps_2022 = race_2022.laps
weather_2022 = race_2022.weather_data

# Dictionary to store the number of wins for each driver
win_count = {}

# Run the simulation
for _ in range(N_SIMULATIONS):
    # Randomly select driver performance from 2021 or 2022
    if random.choice([True, False]):
        laps = laps_2021
        weather = weather_2021
    else:
        laps = laps_2022
        weather = weather_2022

    # Adjust lap time based on weather (hypothetical adjustments)
    if 'Rain' in weather:
        laps['AdjustedLapTime'] = laps['LapTime'] * 1.10
    else:
        laps['AdjustedLapTime'] = laps['LapTime']

    # Adjust lap time based on tyre compound (hypothetical adjustments)
    laps['AdjustedLapTime'] = laps.apply(lambda row: row['AdjustedLapTime'] * 0.98 if row['Compound'] == 'SOFT' else (
        row['AdjustedLapTime'] * 1.02 if row['Compound'] == 'MEDIUM' else row['AdjustedLapTime'] * 1.05), axis=1)

    # Simulate the race outcome based on the adjusted performance data
    winner = laps.groupby('Driver')['AdjustedLapTime'].mean().idxmin()

    # Update the win count
    win_count[winner] = win_count.get(winner, 0) + 1

# Print the results
for driver, wins in win_count.items():
    print(f"{driver}: {wins / N_SIMULATIONS * 100:.2f}% win probability")
