import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mplcursors

# Load the datasets
drivers = pd.read_csv('kaggle-archive/drivers.csv')
results = pd.read_csv('kaggle-archive/results.csv')
races = pd.read_csv('kaggle-archive/races.csv')
qualifying = pd.read_csv('kaggle-archive/qualifying.csv')
constructors = pd.read_csv('kaggle-archive/constructors.csv')

# Extract information for Max Verstappen's career overview
verstappen_data = drivers[(drivers['forename'] == 'Max') & (drivers['surname'] == 'Verstappen')]
verstappen_id = verstappen_data['driverId'].iloc[0]
verstappen_results = results[results['driverId'] == verstappen_id]

# Merge the results with the races and constructors dataframes to get race details and team names
verstappen_race_details = verstappen_results.merge(races, on='raceId').merge(constructors, on='constructorId')

# Sort the data chronologically
verstappen_race_details = verstappen_race_details.sort_values(['year', 'round'])

# Filter out positions 20 and above from Verstappen's race details
filtered_verstappen_results = verstappen_race_details[verstappen_race_details['positionOrder'] < 20]

# Define a color palette for the teams
team_colors_verstappen = {
    'Toro Rosso': '#00327D',  # Dark Blue
    'Red Bull': '#1E41FF'  # Light Blue
}

# Define the theta values (angles) for the radial bar chart
theta = np.linspace(0.0, 2 * np.pi, len(filtered_verstappen_results), endpoint=False)
radii = 20 - filtered_verstappen_results['positionOrder']
width = 2 * np.pi / len(filtered_verstappen_results)

# Set up the figure and axis for radial bar chart
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(20, 20))

# Create a legend proxy for the teams
team_patches = [plt.Line2D([0], [0], color=color, lw=4, label=team) for team, color in team_colors_verstappen.items()]

# Plot the radial bars
bars = ax.bar(theta, radii, width=width, bottom=0.0, align='center', linewidth=0)  # No outline for the bars

# Color the bars based on the team and modify opacity based on position
for bar, (team, pos) in zip(bars,
                            zip(filtered_verstappen_results['name_y'], filtered_verstappen_results['positionOrder'])):
    bar.set_facecolor(team_colors_verstappen[team])
    if pos > 3:
        bar.set_alpha(0.6)  # Slightly increased opacity for better visibility

# Highlight pole positions on the radial bar chart
verstappen_qualifying = qualifying[qualifying['driverId'] == verstappen_id]
pole_races_verstappen = verstappen_qualifying[verstappen_qualifying['position'] == 1]['raceId']
pole_positions_theta = theta[filtered_verstappen_results['raceId'].isin(pole_races_verstappen)]
ax.scatter(pole_positions_theta, 19.5 * np.ones_like(pole_positions_theta), color='blue', marker='*', s=150, zorder=5)

# Enhancing labels, title, and other aesthetics
ax.set_title("Max Verstappen's Race Finish Positions (Radial View)", va='bottom', fontsize=22, pad=20)
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)
ax.set_rlabel_position(90)
ax.set_rticks(np.arange(1, 21))  # Add more ticks
ax.set_yticklabels(
    ['20th', '19th', '18th', '17th', '16th', '15th', '14th', '13th', '12th', '11th', '10th', '9th', '8th', '7th', '6th',
     '5th', '4th', '3rd', '2nd', '1st'], fontsize=10)
ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.6)
ax.legend(handles=team_patches + [plt.Line2D([0], [0], color='blue', marker='*', linestyle='', label='P1')],
          loc=(0.85, 0.85), fontsize=12)
ax.set_xticks([])  # Remove the outer degrees axis

# Hover functionality
cursor = mplcursors.cursor(bars, hover=True)


# Custom hover function to display desired information
@cursor.connect("add")
def on_add(sel):
    index = sel.target.index
    race_info = filtered_verstappen_results.iloc[index]
    race_name = race_info["name_x"]
    race_year = race_info['year']
    qual_pos = verstappen_qualifying[verstappen_qualifying["raceId"] == race_info["raceId"]]["position"].values[0]
    finish_pos = race_info["positionOrder"]
    # avg_lap_time = race_info["milliseconds"] / race_info["laps"]
    # minutes, milliseconds = divmod(avg_lap_time, 60000)
    # seconds = milliseconds // 1000
    sel.annotation.set_text(
        f"{race_year} {race_name}\nQual Pos: {qual_pos}\nFinish: {finish_pos}\nAvg Lap Time: m s")


# Show the plot
plt.tight_layout()
plt.show()
