import os

def run_clean_scripts(file_path, module_path):
  """
  Processes a CSV file and identifies the corresponding Python script to run.

  Args:
      file_path: Path to the CSV file.
      module_path: Path to the folder containing Python scripts (Modules).
  """
  # Extract folder names representing module and script
  folder_names = os.path.dirname(file_path).split(os.sep)[-2:]  # Get last two folders
  if len(folder_names) != 2:
    print(f"Unexpected folder structure for: {file_path}")
    return

  # Construct script name
  script_name = "_".join(folder_names) + ".py"  # Join with underscore
  script_path = os.path.join(module_path, script_name)

  # Check if script exists
  if os.path.exists(script_path):
    print(f"Running {script_name}")
  else:
    print(f"Script not found: {script_path}")

def main():
  accounts_path = "Accounts"
  modules_path = "Modules"

  # Walk through Accounts folder and its subfolders
  for root, _, files in os.walk(accounts_path):
    for filename in files:
      if filename.endswith(".csv"):
        file_path = os.path.join(root, filename)
        run_clean_scripts(file_path, modules_path)

if __name__ == "__main__":
  main()
