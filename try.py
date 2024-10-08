import os
import pandas as pd

# Assign directory
directory = r"output"
 
# Iterate over files in directory
for name in os.listdir(directory):
    # Open file
    for sub_name in os.listdir(os.path.join(directory, name)):
        
        with open(os.path.join(directory, name, sub_name)) as f:
            data = pd.read_csv(os.path.join(directory, name, sub_name))
                    
