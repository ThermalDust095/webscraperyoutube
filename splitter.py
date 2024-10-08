import os
import pandas as pd
import re

def sanitize_filename(filename, max_length=100):
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized[:max_length]

input_csv = 'scraped_data5.csv'
df = pd.read_csv(input_csv)

output_base_dir = 'scraped'
os.makedirs(output_base_dir, exist_ok=True)

for sector, sector_df in df.groupby('Sector'):
    sanitized_sector = sanitize_filename(sector, max_length=50)
    sector_dir = os.path.join(output_base_dir, sanitized_sector)
    os.makedirs(sector_dir, exist_ok=True)
    
    for course_name, course_df in sector_df.groupby('CourseName'):
        sanitized_course_name = sanitize_filename(course_name, max_length=50)
        course_file = os.path.join(sector_dir, f'{sanitized_course_name}.csv')
        course_df.to_csv(course_file, index=False)

print("CSV files created successfully.")