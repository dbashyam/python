import os

# Define folder structure
folders = [
    "phonepe_pulse_analyzer/data/raw_repo",
    "phonepe_pulse_analyzer/db",
    "phonepe_pulse_analyzer/scripts",
    "phonepe_pulse_analyzer/notebooks",
    "phonepe_pulse_analyzer/reports"
]

# Define files with starter content
files = {
    "phonepe_pulse_analyzer/scripts/clone_repo.py": "# Clones the PhonePe Pulse GitHub repository\n",
    "phonepe_pulse_analyzer/scripts/db_schema.py": "# Creates SQLite tables\n",
    "phonepe_pulse_analyzer/scripts/load_data.py": "# Loads PhonePe JSON data into DB\n",
    "phonepe_pulse_analyzer/scripts/analyze.py": "# Analysis queries and logic\n",
    "phonepe_pulse_analyzer/scripts/visualize.py": "# Visualization code (charts/maps)\n",
    "phonepe_pulse_analyzer/main.py": "# Pipeline entry point\n",
    "phonepe_pulse_analyzer/requirements.txt": "# Dependencies go here\n",
    "phonepe_pulse_analyzer/README.md": "# Project description\n",
    "phonepe_pulse_analyzer/.gitignore": "*.db\n__pycache__/\n.ipynb_checkpoints/\n",
    "phonepe_pulse_analyzer/notebooks/exploratory_analysis.ipynb": "",  # Will be created empty
    "phonepe_pulse_analyzer/reports/summary_report.pdf": "",  # Placeholder
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for path, content in files.items():
    with open(path, "w") as f:
        f.write(content)

print("✅ Project folder structure and files created successfully!")
