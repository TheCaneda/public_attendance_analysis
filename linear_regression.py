import pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import seaborn as sns

# Updated function to read, filter data, calculate match outcomes, and total points
def read_and_calculate_actual_points(file_paths):
    yearly_data = []
    for file_path in file_paths:
        try:
            year = file_path[-8:-4]  # Extract year from filename
            df = pd.read_csv(file_path, sep=';', usecols=['Público', 'Cidade', 'Resultado'])
            df['Público'] = pd.to_numeric(df['Público'], errors='coerce')  # Convert to numeric, ignore 'x'
            df = df.dropna(subset=['Público', 'Resultado'])  # Drop rows with NaNs

            # Calculate match outcomes and points
            def calculate_points(result):
                home_goals, away_goals = map(int, result.split(':'))
                if home_goals > away_goals:
                    return 3  # win
                elif home_goals == away_goals:
                    return 1  # draw
                else:
                    return 0  # loss

            def calculate_away_points(result):
                home_goals, away_goals = map(int, result.split(':'))
                if home_goals < away_goals:
                    return 3  # away win
                elif home_goals == away_goals:
                    return 1  # draw
                else:
                    return 0  # home win, away loss

            # Exclude rows where 'Resultado' is not in the expected format
            df = df[df['Resultado'].str.contains(':', na=False)]
            
            pontos = []

            for ind, row in df.iterrows():
                if row['Cidade'] == 'C':
                    pontos.append(calculate_points(row['Resultado']))
                else:
                    pontos.append(calculate_away_points(row['Resultado']))

            df['Points'] = pontos
            average_attendance = df['Público'].mean()
            total_points = df['Points'].sum()
            yearly_data.append((year, average_attendance, total_points))
        except Exception as e:
            print(f"Could not process file {file_path}: {e}")
    
    return pd.DataFrame(yearly_data, columns=['Year', 'Average_Attendance', 'Total_Points'])

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

# Load and process the data for both teams
inter_yearly_data = read_and_calculate_actual_points(inter_files)
gremio_yearly_data = read_and_calculate_actual_points(gremio_files)

# EDA: Plot average attendance and total points for each team per season
plt.figure(figsize=(14, 6))

# Plot for Internacional
plt.subplot(1, 2, 1)
sns.scatterplot(data=inter_yearly_data, x='Average_Attendance', y='Total_Points', color='red', label='Internacional')
plt.title('Internacional: Attendance vs. Points')
plt.xlabel('Average Attendance')
plt.ylabel('Total Points')

# Plot for Grêmio
plt.subplot(1, 2, 2)
sns.scatterplot(data=gremio_yearly_data, x='Average_Attendance', y='Total_Points', color='blue', label='Grêmio')
plt.title('Grêmio: Attendance vs. Points')
plt.xlabel('Average Attendance')
plt.ylabel('Total Points')

plt.tight_layout()
plt.show()
plt.savefig('attendance_vs_points.png')

from sklearn.linear_model import LinearRegression
import numpy as np

# Check for NaN values in both datasets
print("Internacional dataset NaN values:")
print(inter_yearly_data.isnull().sum())

print("\nGrêmio dataset NaN values:")
print(gremio_yearly_data.isnull().sum())

# Remove rows with NaN values
inter_yearly_data_clean = inter_yearly_data.dropna()
gremio_yearly_data_clean = gremio_yearly_data.dropna()

# Prepare the cleaned data for linear regression
X_inter_clean = inter_yearly_data_clean[['Average_Attendance']].values.reshape(-1, 1)
y_inter_clean = inter_yearly_data_clean['Total_Points'].values

X_gremio_clean = gremio_yearly_data_clean[['Average_Attendance']].values.reshape(-1, 1)
y_gremio_clean = gremio_yearly_data_clean['Total_Points'].values

# Perform linear regression with the cleaned data
reg_inter_clean = LinearRegression().fit(X_inter_clean, y_inter_clean)
reg_gremio_clean = LinearRegression().fit(X_gremio_clean, y_gremio_clean)

# Extracting coefficients and intercepts for the regression lines with cleaned data
inter_clean_slope, inter_clean_intercept = reg_inter_clean.coef_[0], reg_inter_clean.intercept_
gremio_clean_slope, gremio_clean_intercept = reg_gremio_clean.coef_[0], reg_gremio_clean.intercept_

# Output the coefficients and intercepts for both teams with cleaned data
inter_clean_slope, inter_clean_intercept, gremio_clean_slope, gremio_clean_intercept

# Print the results
print(f"Internacional Regression Line: y = {inter_clean_slope:.2f}x + {inter_clean_intercept:.2f}")
print(f"Grêmio Regression Line: y = {gremio_clean_slope:.2f}x + {gremio_clean_intercept:.2f}")

# Plotting regression lines along with the scatter plots
plt.figure(figsize=(14, 6))

# Internacional
plt.subplot(1, 2, 1)
sns.scatterplot(data=inter_yearly_data, x='Average_Attendance', y='Total_Points', color='red', label='Internacional')
plt.plot(X_inter_clean, inter_clean_slope*X_inter_clean + inter_clean_intercept, color='black', label='Regression Line')
plt.title('Internacional: Attendance vs. Points')
plt.xlabel('Average Attendance')
plt.ylabel('Total Points')
plt.legend()
plt.savefig('inter_regression.png')

# Grêmio
plt.subplot(1, 2, 2)
sns.scatterplot(data=gremio_yearly_data, x='Average_Attendance', y='Total_Points', color='blue', label='Grêmio')
plt.plot(X_gremio_clean, gremio_clean_slope*X_gremio_clean + gremio_clean_intercept, color='black', label='Regression Line')
plt.title('Grêmio: Attendance vs. Points')
plt.xlabel('Average Attendance')
plt.ylabel('Total Points')
plt.legend()
plt.savefig('gremio_regression.png')

plt.tight_layout()
plt.show()
plt.savefig('attendance_vs_points_with_regression.png')
