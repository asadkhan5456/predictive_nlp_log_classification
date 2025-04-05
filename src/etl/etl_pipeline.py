import os
import pandas as pd

def parse_bgl_log(file_path):
    """
    Parses the BGL log file and returns a DataFrame.
    
    Each line in the log file is assumed to have the following format:
        <alert_label> <log message>
    where the first token is the alert label.
    "-" indicates a non-alert message, while any other value indicates an alert.
    
    Returns a DataFrame with columns 'alert' and 'log_message'.
    """
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            # Remove leading/trailing whitespace
            line = line.strip()
            if not line:
                continue
            # Split the line into label and message; only split once
            tokens = line.split(maxsplit=1)
            if len(tokens) == 2:
                label, message = tokens
            else:
                label = tokens[0]
                message = ""
            data.append({'alert': label, 'log_message': message})
    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    # Determine the project root by moving up three directories from this file's location
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Define the path to the raw data folder and the BGL log file
    raw_dir = os.path.join(project_root, 'data', 'raw')
    log_file = os.path.join(raw_dir, 'bgl.log')
    
    # Parse the BGL log file
    df_bgl = parse_bgl_log(log_file)
    print("Parsed BGL log dataset shape:", df_bgl.shape)
    print(df_bgl.head())
    
    # Create the processed data directory if it doesn't exist
    processed_dir = os.path.join(project_root, 'data', 'processed')
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    
    # Save the parsed logs as CSV for further processing
    output_file = os.path.join(processed_dir, 'parsed_bgl_logs.csv')
    df_bgl.to_csv(output_file, index=False)
    print("Parsed BGL logs saved to:", output_file)
