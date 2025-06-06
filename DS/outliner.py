# START GENAI
import pandas as pd

# Create the DataFrame
data = {'Temperature': [25, 30, 22, 40, 32, 17, 12, 252, 19]}
df_temp = pd.DataFrame(data)

# Print the original data
print("Original Data:")
print(df_temp)

# Sort the data to calculate percentiles
sorted_temp = df_temp['Temperature'].sort_values().reset_index(drop=True)

# Debug: Print sorted data
print("\nSorted Data:")
print(sorted_temp)

# Calculate Q1 (25th percentile)
Q1_position = 0.25 * (len(sorted_temp) + 1)
Q1 = sorted_temp.iloc[int(Q1_position) - 1] + (Q1_position % 1) * (sorted_temp.iloc[int(Q1_position)] - sorted_temp.iloc[int(Q1_position) - 1])

# Debug: Print Q1 position and value
print("\nQ1 Position (using 0.25 * (n + 1)):", Q1_position)
print("Q1 (25th percentile):", Q1)

# Calculate Q3 (75th percentile)
Q3_position = 0.75 * (len(sorted_temp) + 1)
Q3 = sorted_temp.iloc[int(Q3_position) - 1] + (Q3_position % 1) * (sorted_temp.iloc[int(Q3_position)] - sorted_temp.iloc[int(Q3_position) - 1])

# Debug: Print Q3 position and value
print("\nQ3 Position (using 0.75 * (n + 1)):", Q3_position)
print("Q3 (75th percentile):", Q3)

# Calculate IQR
IQR = Q3 - Q1

# Debug: Print IQR
print("\nInterquartile Range (IQR):", IQR)

# Define bounds for outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Debug: Print bounds
print("\nLower Bound for Outliers:", lower_bound)
print("Upper Bound for Outliers:", upper_bound)

# Remove outliers
df_no_outliers = df_temp[(df_temp['Temperature'] >= lower_bound) & (df_temp['Temperature'] <= upper_bound)]

# Print the data without outliers
print("\nData without outliers:")
print(df_no_outliers)

# END GENAI