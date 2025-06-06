import matplotlib.pyplot as plt
import numpy as np

# Sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)
categories = ['A', 'B', 'C']
values = [10, 15, 7]

# Create a 3x3 subplot
fig, axs = plt.subplots(3, 3, figsize=(15, 12))

# Top-right corner (1,3) → Scatter plot
axs[0, 2].scatter(x, y, color='purple')
axs[0, 2].set_title('Scatter Chart')

# Middle center (2,2) → Bar chart
axs[1, 1].bar(categories, values, color='orange')
axs[1, 1].set_title('Bar Chart')

# Bottom-right (3,3) → Line chart
axs[2, 2].plot(x, y, color='green')
axs[2, 2].set_title('Line Chart')

# Fill the remaining charts with example plots
for row in range(3):
    for col in range(3):
        if (row, col) not in [(0, 2), (1, 1), (2, 2)]:
            axs[row, col].plot(np.random.rand(10), color='gray')
            axs[row, col].set_title(f'Chart {row+1},{col+1}')

plt.tight_layout()
plt.show()
