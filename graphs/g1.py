import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [10, 12, 8, 15, 13]

plt.figure(figsize=(8, 5))
plt.plot(x, y, marker='o', linestyle='-', color='blue', label='Data Line')

for i in range(len(x)):
    label = f"({x[i]}, {y[i]})"
    plt.text(x[i], y[i] + 0.5, label, ha='center', fontsize=9)

plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.title('Line Chart with (x, y) Labels')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()  # <--- This MUST be included
