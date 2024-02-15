import pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns

# Helper function to read and filter data
def read_and_filter_data(file_paths):
    attendance_data = []
    for file_path in file_paths:
        try:
            df = pd.read_csv(file_path, sep=';', usecols=['Público', 'Cidade'])
            df = df[df['Cidade'] == 'C']  # Only home games
            df = df[df['Público'] != 'x']  # Exclude 'x' (COVID-19 affected games)
            df['Público'] = pd.to_numeric(df['Público'], errors='coerce')  # Convert to numeric, making 'x' NaN
            df = df.dropna(subset=['Público'])  # Drop rows with NaNs in 'Público'
            attendance_data.append(df['Público'])
        except Exception as e:
            print(f"Could not process file {file_path}: {e}")
    
    return pd.concat(attendance_data)

# Define the paths to the files for both teams
inter_files = [
    './data/inter/campeonato gaúcho/2011.csv',
    './data/inter/campeonato gaúcho/2016.csv',
    './data/inter/campeonato gaúcho/2017.csv',
    './data/inter/campeonato gaúcho/2018.csv',
    './data/inter/campeonato gaúcho/2019.csv',
    './data/inter/campeonato gaúcho/2020.csv'
]

gremio_files = [
    './data/gremio/campeonato gaúcho/2011.csv',
    './data/gremio/campeonato gaúcho/2016.csv',
    './data/gremio/campeonato gaúcho/2017.csv',
    './data/gremio/campeonato gaúcho/2018.csv',
    './data/gremio/campeonato gaúcho/2019.csv',
    './data/gremio/campeonato gaúcho/2020.csv'
]

# Read and filter the data for both teams
inter_attendance = read_and_filter_data(inter_files)
gremio_attendance = read_and_filter_data(gremio_files)

# Perform EDA - plot the distribution of attendance
plt.figure(figsize=(14, 7))

plt.subplot(1, 2, 1)
sns.histplot(inter_attendance, kde=True, color='blue')
plt.title('Attendance Distribution for Internacional')

plt.subplot(1, 2, 2)
sns.histplot(gremio_attendance, kde=True, color='black')
plt.title('Attendance Distribution for Grêmio')

plt.tight_layout()
plt.savefig('attendance_distribution.png')
plt.show()

# Perform the Mann-Whitney U Test on the filtered attendance data
u_statistic, p_value = mannwhitneyu(inter_attendance, gremio_attendance, alternative='two-sided')

# Output the results of the Mann-Whitney U Test
print(f'U statistic: {u_statistic}, p-value: {p_value}')
