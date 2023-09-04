import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.collections import LineCollection
import fastf1.plotting
import fastf1 as ff1
import numpy as np

# Enable some matplotlib patches for plotting timedelta values and load
# FastF1's default color scheme
fastf1.plotting.setup_mpl(misc_mpl_mods=False)

# Load a session and its telemetry data
session = fastf1.get_session(2023, 'Italian', 'q')
session.load()

driver1 = "VER"
driver2 = "SAI"

driver1_lap = session.laps.pick_driver(driver1).pick_fastest()
driver2_lap = session.laps.pick_driver(driver2).pick_fastest()

driver1_tel = driver1_lap.get_car_data().add_distance()
driver2_tel = driver2_lap.get_car_data().add_distance()

# Fetching throttle, brake, and DRS data for VER
driver1_throttle = driver1_tel['Throttle']
driver1_brake = driver1_tel['Brake']
driver1_drs = driver1_tel['DRS']

# Fetching throttle, brake, and DRS data for LEC
driver2_throttle = driver2_tel['Throttle']
driver2_brake = driver2_tel['Brake']
driver2_drs = driver2_tel['DRS']

driver1_color = fastf1.plotting.team_color(driver1_lap['Team'])
driver2_color = fastf1.plotting.team_color(driver2_lap['Team'])

# Assuming that the telemetry data is regularly spaced, we'll interpolate both drivers' data to a common distance array
common_distance = np.linspace(driver1_tel['Distance'].min(), driver1_tel['Distance'].max(), len(driver1_tel['Distance']))

# Interpolating the time data for both drivers
driver1_time_interp = np.interp(common_distance, driver1_tel['Distance'], driver1_tel['Time'].dt.total_seconds())
driver2_time_interp = np.interp(common_distance, driver2_tel['Distance'], driver2_tel['Time'].dt.total_seconds())

# Calculating time delta
time_delta = driver1_time_interp - driver2_time_interp

##############################################################################
# After this, we can actually plot the data.

fig, ax = plt.subplots(5, 1, sharex=True, figsize=(12, 18))  # 5 subplots for Speed, Throttle, Brake, DRS, and Time Delta
plt.suptitle(f"Fastest Lap Comparison \n "
             f"{session.event['EventName']} {session.event.year} - Fastest Qualifying Laps \n "
             f"{driver1_lap['Driver']} vs {driver2_lap['Driver']}")

# Plotting speed data
ax[0].plot(driver1_tel['Distance'], driver1_tel['Speed'], color=driver1_color, label=driver1_lap['Driver'])
ax[0].plot(driver2_tel['Distance'], driver2_tel['Speed'], color=driver2_color, label=driver2_lap['Driver'])
ax[0].set_ylabel('Speed in km/h')
ax[0].yaxis.grid(which='major', color='gray', linewidth=0.3)
ax[0].minorticks_on()
ax[0].legend()

# Plotting throttle data
ax[1].plot(driver1_tel['Distance'], driver1_throttle, color=driver1_color, label=driver1_lap['Driver'])
ax[1].plot(driver2_tel['Distance'], driver2_throttle, color=driver2_color, label=driver2_lap['Driver'])
ax[1].set_ylabel('Throttle %')
ax[1].legend()

# Plotting brake data
ax[2].plot(driver1_tel['Distance'], driver1_brake, color=driver1_color, label=driver1_lap['Driver'])
ax[2].plot(driver2_tel['Distance'], driver2_brake, color=driver2_color, label=driver2_lap['Driver'])
ax[2].set_ylabel('Brake %')
ax[2].legend()

# Plotting DRS data
ax[3].plot(driver1_tel['Distance'], driver1_drs, color=driver1_color, label=driver1_lap['Driver'])
ax[3].plot(driver2_tel['Distance'], driver2_drs, color=driver2_color, label=driver2_lap['Driver'])
ax[3].set_ylabel('DRS Activation')
ax[3].legend()

# Plotting the time delta
colors = np.where(time_delta < 0, driver1_color, driver2_color)  # Color based on which driver is ahead
ax[4].fill_between(common_distance, time_delta, where=time_delta>=0, color=driver1_color, label=f"{driver1_lap['Driver']} Ahead", interpolate=True)
ax[4].fill_between(common_distance, time_delta, where=time_delta<0, color=driver2_color, label=f"{driver2_lap['Driver']} Ahead", interpolate=True)
ax[4].set_ylabel('Time Delta (s)')
ax[4].legend()
ax[4].axhline(0, color='white', linestyle='--', linewidth=0.5)  # Line at zero for reference
ax[4].yaxis.grid(which='major', color='gray', linewidth=0.3)
ax[4].yaxis.grid(which='minor', color='gray', linestyle=':', linewidth=0.1)
ax[4].minorticks_on()

plt.tight_layout()
plt.show()

fig2, ax = plt.subplots(sharex=True, sharey=True, figsize=(12, 6.75))
fig2.suptitle(f'{session.event["EventName"]} - {session.event.year} - Speed', size=24, y=0.97)

# Adjust margins and turn of axis
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.12)
ax.axis('off')


colormap = mpl.cm.plasma
x = driver1_lap.telemetry['X']              # values for x-axis
y = driver1_lap.telemetry['Y']              # values for y-axis
color = driver1_lap.telemetry['Speed']      # value to base color gradient on

# Plotting the speed heatmap on the last subplot
ax_speed = ax
ax_speed.axis('off')
ax_speed.plot(driver1_lap.telemetry['X'], driver1_lap.telemetry['Y'], color='black', linestyle='-', linewidth=16, zorder=0)

points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

norm = plt.Normalize(color.min(), color.max())
lc = LineCollection(segments, cmap=colormap, norm=norm, linestyle='-', linewidth=5)
lc.set_array(color)
line = ax_speed.add_collection(lc)

# Color bar legend for the speed heatmap
cbaxes = fig.add_axes([0.25, 0.05, 0.5, 0.05])
normlegend = mpl.colors.Normalize(vmin=color.min(), vmax=color.max())
legend = mpl.colorbar.ColorbarBase(cbaxes, norm=normlegend, cmap=colormap, orientation="horizontal")
plt.tight_layout()

plt.show()
