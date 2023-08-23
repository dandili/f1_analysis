import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class RaceData:
    def __init__(self, sprint_file, results_file, drivers_file):
        self.sprint_results = pd.read_csv(sprint_file)
        self.results = pd.read_csv(results_file)
        self.drivers = pd.read_csv(drivers_file)

    def merge_data(self):
        # Merging sprint_results with results on raceId and driverId
        merged_results = self.sprint_results.merge(self.results, on=['raceId', 'driverId'],
                                                   suffixes=('_sprint', '_main'))
        return merged_results

    def get_driver_name(self, driver_id):
        driver = self.drivers[self.drivers['driverId'] == driver_id].iloc[0]
        return f"{driver['forename']} {driver['surname']}"


class SprintImpactAnalysis(RaceData):
    def __init__(self, sprint_file, results_file, drivers_file):
        super().__init__(sprint_file, results_file, drivers_file)
        self.merged_results = self.merge_data()

    def calculate_position_difference(self):
        self.merged_results['position_difference'] = abs(
            self.merged_results['position_sprint'] - self.merged_results['position_main'])
        return self.merged_results[['raceId', 'driverId', 'position_sprint', 'position_main', 'position_difference']]

    def analyze_position_change(self):
        # Calculate position change for each race
        self.merged_results['position_change'] = self.merged_results['position_sprint'] - self.merged_results[
            'position_main']

        # Calculate average position change for each driver
        avg_position_change = self.merged_results.groupby('driverId')['position_change'].mean().reset_index()
        avg_position_change['driver_name'] = avg_position_change['driverId'].apply(self.get_driver_name)

        # Visualization
        plt.figure(figsize=(14, 10))
        sns.barplot(data=avg_position_change, y='driver_name', x='position_change', palette="coolwarm_r")
        plt.title('Average Position Change from Sprint to Main Race')
        plt.xlabel('Average Position Change')
        plt.ylabel('Driver Name')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, axis='x')
        plt.show()


if __name__ == "__main__":
    analyzer = SprintImpactAnalysis('kaggle-archive/sprint_results.csv', 'kaggle-archive/results.csv', 'kaggle-archive/drivers.csv')
    analyzer.analyze_position_change()
