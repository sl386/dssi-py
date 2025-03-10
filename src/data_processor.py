"""
This module contains the various procedures for processing data.
"""

import argparse
import numpy as np
import pandas as pd

def load_data(data_path):
    """
    Read dataset from given directory.
        Parameters:
            data_path (str): directory containing dataset in csv
        Returns:
            df: dataframe containing the input data
    """
    df = pd.read_csv(data_path)
    print("Columns in dataset:", df.columns)  # This will show the exact column names
    return df

def save_data(data_path, df):
    """
    Save data to directory.
        Parameters:
            data_path (str): Directory for saving dataset
            df: Dataframe containing data to save
        Returns:
            None: No returns required
    """
    df.to_csv(data_path.replace('.csv','_processed.csv'), index=False)
    return None

def log_txf(df, cols: list):
    """
    Perform log transformation on specified columns in dataset.
        Parameters:
            df: input dataframe
            cols (list): columns that need log transformation
        Returns:
            df: resultant dataframe containing newly transformed columns
    """
    for col in cols:
        if col in df.columns:  # Check if the column exists
            df['log_' + col] = np.log(df[col] + 1)
        else:
            print(f"Warning: Column '{col}' not found in the dataset!")
    return df


def remap_emp_length(x):
    """
    Re-categorize categories in "emp_length" categorical variable.
        Parameters:
            x (str): Input category
        Returns:
            New category in (str)
    """
    if x in ['< 1 year','1 year','2 years']:
        return 'less_than_3yr'
    if x in ['3 years','4 years','5 years']:
        return '3_to_5yr'
    if x in ['6 years','7 years','8 years','9 years']:
        return '6_to_9yr'
    return 'more_than_9yr'


def preprocess(df):
    """
    Orchestrate data pre-processing procedures for diabetes-related features.
        Parameters:
            df: Input dataframe to be pre-processed
        Returns:
            df: Resultant dataframe after pre-processing
    """
    # Apply log transformation to numerical columns that can have large ranges or outliers
    df = log_txf(df, ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI','Age'])

    # Optionally, you may want to normalize or scale numerical features for better model performance
    # Example: Min-max scaling for numeric features (this could be added as needed)
    # from sklearn.preprocessing import MinMaxScaler
    # scaler = MinMaxScaler()
    # df[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']] = scaler.fit_transform(df[['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']])

    return df

def run(data_path):
    """
    Main script to read and pre-process data.
        Parameters:
            data_path (str): Directory containing dataset in csv
        Returns:
            df: Dataframe containing the final pre-processed data
    """
    df = load_data(data_path)
    df = preprocess(df)
    save_data(data_path, df)
    return df

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--data_path", type=str)
    args = argparser.parse_args()
    run(args.data_path)