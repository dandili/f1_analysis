
# F1 Telemetry Visualization Toolkit

Analyze and visualize telemetry data from Formula 1 races using Python.

![Telemetry Visualization Sample]([https://github.com/dandili/f1_analysis/blob/master/images/2022%20Dutch%20GP%20-%20Verstappen%20Fastest%20Lap.png?raw=true](https://raw.githubusercontent.com/dandili/f1_analysis/master/images/2022%20Dutch%20Grand%20Prix%20-%20Fastest%20Qualifying%20Laps%20-%20Verstappen%20vs%20Leclerc.png?token=GHSAT0AAAAAACGR3KZZGK5JKE36CH4AW5T2ZHDOVPA))  

## Features

- **Fetch Telemetry Data**: Easily obtain telemetry data for specific drivers and sessions using the `fastf1` library.
- **Compare Fastest Laps**: Analyze and compare the fastest laps between two drivers.
- **Speed Distribution on Track**: Visualize how a driver's speed varies throughout different parts of the track.
- **Speed Traces**: Plot speed traces to understand and compare driver performance throughout a lap.
- **Race Strategies**: Analyze and visualize race strategies based on tire stints.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or later
- The following Python libraries: `fastf1`, `matplotlib`, `numpy`

### Installation

1. Clone the repository:

```
git clone https://github.com/your_github_username/f1_telemetry_toolkit.git
```

2. Navigate to the project directory:

```
cd f1_telemetry_toolkit
```

3. Install the required Python libraries:

```
pip install -r requirements.txt
```

## Usage

Detailed instructions for each module can be found within the respective Python files.

```python
from plot_laptimes_distribution import plot_laptimes_distribution

# Example usage
plot_laptimes_distribution(year=2022, race="Dutch")
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

## Ackowledgements

* FastF1 for the API.
* Brrrake(https://www.instagram.com/brrrake) for the inspiration from their race data analysis Youtube videos.

