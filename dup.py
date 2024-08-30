import shutil

# Define the source HTML file
source_file = '강두한.html'

# List of new names for the HTML files
new_names = [
    '조진우', '김호연', '박유진', '박지호', '김승범', 
    '이의호', '이신형', '임다빈', '홍다솜', '최서연', 
    '정의진', '정서진', '유준모'
]

# Loop to create duplicates with different names
for name in new_names:
    # Define the new file name
    new_file = f'{name}.html'
    
    # Copy the content of the source file to the new file
    shutil.copyfile(source_file, new_file)

print("13 files have been successfully duplicated with new names.")
