import pandas as pd
import os
from datetime import datetime
import glob
from tkinter import messagebox
import tkinter as tk
import shutil

def convert_date_format(df, date_columns):
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
    return df

def process_learner_data(input_dir):
    # Get all CSV files matching the pattern
    csv_files = glob.glob(os.path.join(input_dir, 'user-filtering-exports_*.csv'))
    
    # Filter files by name length check
    csv_files = [f for f in csv_files if len(os.path.basename(f).split('.')[0]) > len('user-filtering-exports_')]
    
    if not csv_files:
        raise Exception("No matching CSV files found in the input directory")
    
    # Check if number of CSV files is not 2 or 3
    if len(csv_files) not in [2, 3]:
        # Create and hide the root window
        root = tk.Tk()
        root.withdraw()
        
        # Show info dialog with OK button
        messagebox.showinfo("Information", 
            f"Found {len(csv_files)} CSV files.\nPlease move the old CSV files to the backup folder.")
        return
    
    # Read and concatenate all CSV files
    dfs = []
    date_columns = ['Join Date', 'Invitation Date', 'Latest Program Activity Date']
    for i, file in enumerate(csv_files):
        df = pd.read_csv(file)
        df['Programs'] = str(i) # found on May 29, 2025, no Programs column can be selected for downloaded csv 
        df['Invitation Date'] = '' # 'Invitation Date' is no longer needed, so make a blank one
        df = convert_date_format(df, date_columns)
        dfs.append(df)
    
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Select required columns
    columns = ['Full Name*', 'Email*', 'Join Date', 'Invitation Date', 
              'Programs', 'Latest Program Activity Date']
    # columns = ['Full Name', 'Email', 'Join Date', 'Latest Program Activity Date']
    selected_df = combined_df[columns]
    
    # Process Join Dates
    join_date_df = selected_df.groupby(['Full Name*', 'Email*'])['Join Date'].agg(lambda x: x.tolist()).reset_index()
    invitation_date_df = selected_df.groupby(['Full Name*', 'Email*'])['Invitation Date'].agg(lambda x: x.tolist()).reset_index()
    
    # Print some debug info
    print("First few rows of join_date_df:")
    print(join_date_df.head())
    
    # Process Join Dates
    max_join_dates = max((len(x) if isinstance(x, list) else 0 for x in join_date_df['Join Date']), default=0)
    join_date_columns = []
    for i in range(max_join_dates):
        col_name = f'Join Date {i+1}'
        join_date_df[col_name] = join_date_df['Join Date'].apply(lambda x: x[i] if i < len(x) else None)
        join_date_columns.append(col_name)
    join_date_df.drop('Join Date', axis=1, inplace=True)

    # Convert and calculate Latest Join Date
    for col in join_date_columns:
        join_date_df[col] = pd.to_datetime(join_date_df[col], errors='coerce')
    join_date_df['Latest Join Date'] = join_date_df[join_date_columns].max(axis=1)
    join_date_df['Latest Join Date'] = join_date_df['Latest Join Date'].dt.strftime('%Y-%m-%d')
    join_date_df.drop(columns=join_date_columns, inplace=True)

    # Process Invitation Dates
    max_inv_dates = max((len(x) if isinstance(x, list) else 0 for x in invitation_date_df['Invitation Date']), default=0)
    inv_date_columns = []
    for i in range(max_inv_dates):
        col_name = f'Invitation Date {i+1}'
        invitation_date_df[col_name] = invitation_date_df['Invitation Date'].apply(lambda x: x[i] if i < len(x) else None)
        inv_date_columns.append(col_name)
    invitation_date_df.drop('Invitation Date', axis=1, inplace=True)

    # Convert and calculate Latest Invitation Date
    for col in inv_date_columns:
        invitation_date_df[col] = pd.to_datetime(invitation_date_df[col], errors='coerce')
    invitation_date_df['Latest Invitation Date'] = invitation_date_df[inv_date_columns].max(axis=1)
    invitation_date_df['Latest Invitation Date'] = invitation_date_df['Latest Invitation Date'].dt.strftime('%Y-%m-%d')
    invitation_date_df.drop(columns=inv_date_columns, inplace=True)

    # Merge join and invitation dates
    date_df = pd.merge(join_date_df, invitation_date_df, on=['Full Name*', 'Email*'], how='outer')

    # Pivot for Programs and Latest Program Activity Date
    program_df = selected_df.pivot_table(
        index=['Full Name*', 'Email*'],
        columns='Programs',
        values='Latest Program Activity Date',
        aggfunc='first'
    ).reset_index()

    # Merge all dataframes
    final_df = pd.merge(date_df, program_df, on=['Full Name*', 'Email*'], how='outer')

    # Convert all program date columns to datetime for comparison
    program_date_columns = [col for col in final_df.columns
                          if col not in ['Full Name*', 'Email*'] + 
                          [f'Join Date {i+1}' for i in range(max_join_dates)]]
    for col in program_date_columns:
        final_df[col] = pd.to_datetime(final_df[col], errors='coerce')

    # Calculate latest date across program columns
    final_df['Latest Activity Date'] = final_df[program_date_columns].max(axis=1)
    
    # Convert dates back to string format for CSV output
    for col in final_df.select_dtypes(include=['datetime64']).columns:
        final_df[col] = final_df[col].dt.strftime('%Y-%m-%d')

    # Sort by Latest Active Date descending
    final_df = final_df.sort_values('Latest Activity Date')

    # Save to CSV
    output_filename = f'coursera_learners_{datetime.now().strftime("%Y-%m-%d")}.csv'
    output_path = os.path.join(input_dir, output_filename)
    final_df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

    # Show completion dialog and ask about backup
    root = tk.Tk()
    root.withdraw()
    if messagebox.askyesno("Processing Complete", 
        "Move the downloaded csv files and the result to backup folder?"):
        # Create backup folder and date subfolder
        backup_dir = os.path.join(os.path.dirname(input_dir), 'backups')
        date_folder = datetime.now().strftime("%Y-%m-%d")
        backup_date_dir = os.path.join(backup_dir, date_folder)
        os.makedirs(backup_date_dir, exist_ok=True)
        
        # Move each input CSV file and the generated output file to backup
        files_to_move = csv_files + [output_path]
        for file in files_to_move:
            filename = os.path.basename(file)
            backup_path = os.path.join(backup_date_dir, filename)
            # Add timestamp if file already exists in backup
            if os.path.exists(backup_path):
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime("%H%M%S")
                backup_path = os.path.join(backup_date_dir, f"{name}_{timestamp}{ext}")
            shutil.move(file, backup_path)
        
        print(f"Moved {len(files_to_move)} files to backup folder: {backup_date_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', required=True, help='Input directory containing CSV files')
    args = parser.parse_args()
    
    process_learner_data(args.input_dir)