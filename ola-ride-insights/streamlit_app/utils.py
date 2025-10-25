def load_data(file_path):
    import pandas as pd
    """Load data from a CSV file."""
    return pd.read_csv(file_path)

def preprocess_data(df):
    """Preprocess the DataFrame by handling missing values and converting data types."""
    # Example preprocessing steps
    df.fillna(method='ffill', inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    return df

def get_unique_values(df, column_name):
    """Return unique values from a specified column in the DataFrame."""
    return df[column_name].unique()

def filter_data_by_condition(df, condition):
    """Filter the DataFrame based on a given condition."""
    return df.query(condition)

def calculate_average(df, column_name):
    """Calculate the average of a specified column in the DataFrame."""
    return df[column_name].mean()