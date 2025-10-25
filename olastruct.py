import os

dirs = [
    'ola-ride-insights/data/raw',
    'ola-ride-insights/data/processed',
    'ola-ride-insights/notebooks',
    'ola-ride-insights/sql',
    'ola-ride-insights/powerbi',
    'ola-ride-insights/streamlit_app',
    'ola-ride-insights/reports'
]

files = [
    'ola-ride-insights/data/README.md',
    'ola-ride-insights/notebooks/01_data_exploration.ipynb',
    'ola-ride-insights/notebooks/02_data_cleaning.ipynb',
    'ola-ride-insights/notebooks/03_feature_engineering.ipynb',
    'ola-ride-insights/sql/01_successful_bookings.sql',
    'ola-ride-insights/sql/02_avg_distance_per_vehicle.sql',
    'ola-ride-insights/sql/03_cancelled_by_customer.sql',
    'ola-ride-insights/sql/04_top5_customers.sql',
    'ola-ride-insights/sql/05_cancelled_by_driver.sql',
    'ola-ride-insights/sql/06_prime_sedan_ratings.sql',
    'ola-ride-insights/sql/07_upi_payments.sql',
    'ola-ride-insights/sql/08_avg_rating_per_vehicle.sql',
    'ola-ride-insights/sql/09_total_booking_value.sql',
    'ola-ride-insights/sql/10_incomplete_rides.sql',
    'ola-ride-insights/powerbi/README.md',
    'ola-ride-insights/powerbi/ola_dashboard.pbix',
    'ola-ride-insights/streamlit_app/app.py',
    'ola-ride-insights/streamlit_app/utils.py',
    'ola-ride-insights/streamlit_app/requirements.txt',
    'ola-ride-insights/streamlit_app/README.md',
    'ola-ride-insights/reports/business_insights.md',
    'ola-ride-insights/reports/project_presentation.pptx',
    'ola-ride-insights/reports/findings_summary.pdf',
    'ola-ride-insights/.gitignore',
    'ola-ride-insights/README.md',
    'ola-ride-insights/LICENSE'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

for f in files:
    if not os.path.exists(f):
        with open(f, 'w') as fp:
            pass

# Write the .gitignore content
gitignore_content = '''
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook checkpoints
.ipynb_checkpoints

# PyInstaller
*.manifest
*.spec

# Installer logs
debug.log

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Data files
ola-ride-insights/data/raw/*
ola-ride-insights/data/processed/*
!ola-ride-insights/data/README.md

# Power BI files
ola-ride-insights/powerbi/*.pbix

# Reports
ola-ride-insights/reports/*.pdf
ola-ride-insights/reports/*.pptx

# Streamlit secrets
ola-ride-insights/streamlit_app/.streamlit/secrets.toml

# OS files
.DS_Store
Thumbs.db
'''

with open('ola-ride-insights/.gitignore', 'w') as f:
    f.write(gitignore_content)
