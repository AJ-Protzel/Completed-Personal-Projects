import os

def print_running_file(file_path):
  file_name = os.path.basename(file_path)
  print(f"Running {file_name}")

# Example usage:
file_path = "path/to/your/file.py"
print_running_file(file_path)
