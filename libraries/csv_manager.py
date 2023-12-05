import pandas as pd


# Load data from given path to dataframe and return that dataframe
def load_data(filepath, sep='\t'):
    df = pd.read_csv(filepath, sep=sep, index_col=None)
    if len(df) > 1:
        df.set_index('Unnamed: 0', inplace=True)
    return df


# Store received data to given filepath with default separator TAB
def store_data(filepath, df, sep='\t'):
    try:
        # Save the DataFrame to a CSV file
        # df.to_csv(filepath, sep=sep, index=True, header=True)
        df.to_csv(filepath, sep=sep)
        print(f"Data has been successfully stored in {filepath}")
    except Exception as e:
        print(f"An error occurred while storing the data: {str(e)}")
