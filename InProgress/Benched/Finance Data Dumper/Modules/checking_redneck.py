import os
import pandas as pd

# file_description_map = r"Mappings/description_map.txt"
# file_category_map = r"Mappings/category_map.txt"
# file_account_map = r"Mappings/account_map.txt"
# file_key = r"Mappings/key.txt"

# #======================================================================================== load_mappings
# def load_mappings(file_path):
#   mapping = {}
#   with open(file_path, 'r') as file:
#     for line in file:
#       key, value = line.strip().split('=')
#       mapping[key] = value
#   return mapping

# description_map = load_mappings(file_description_map)
# category_map = load_mappings(file_category_map)
# account_map = load_mappings(file_account_map)

# #===================================================================================== contains_keyword
# def contains_keyword(text):
#   with open(file_key, "r") as file:
#     words = file.readlines()
#     words = [word.strip() for word in words]
  
#   for word in words:
#     if word.lower() in text.lower():
#       return word.lower()
#   return None








def get_file_path():
    # script_name, _ = os.path.splitext(os.path.basename(__file__))
    # target_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Accounts', script_name.split('_')[0], script_name.split('_')[1])

    # file_names = []
    # for root, _, files in os.walk(target_folder):
    #     for file in files:
    #         file_names.append(file)

    # return target_folder, file_names
    file_paths = []
    for file in os.listdir(target_folder):
        file_path = os.path.join(target_folder, file)
        file_paths.append(file_path)
    return file_paths

def process_csv_files(target_folder, file_names):
    for file_name in file_names:
        if file_name.endswith('.csv'):
            file_path = os.path.join(target_folder, file_name)
            df = pd.read_csv(file_path)

            create_cols(df)
            fill_cols(df)
            remove_cols(df)

            # def get_description(desc, amount):
            # description = contains_keyword(desc)
            # if description == "ach debit" or "ach credit":
            # description = "transfer"
            # if description is None:
            # description = description_map.get(desc, None)
            # if description is None:
            # user_input = input(f"Description {amount} {desc} = ")
            # user_input.lower()
            # with open(file_description_map, 'a') as mapping_file:
            # mapping_file.write(f"{desc}={user_input}\n")
            # description = user_input
            # with open(file_key, 'a') as key_file:
            # key_file.write(f"{description}\n")
            # return description.lower()

            

            df.to_csv(file_path, index=False)



def create_cols(df):
    # Create the 'Amount' column, fill with -(Debit) and Credit
    # if 'Amount' not in df.columns:
    #     df['Amount'] = -df['Debit'].fillna(0) + df['Credit'].fillna(0)

    if 'Amount' not in df.columns:
        df['Amount']

    # Create the 'Category' column, fill with -(Debit) and Credit
    if 'Category' not in df.columns:
        df['Category']

    # Create the 'Bank' column, fill with -(Debit) and Credit
    if 'Bank' not in df.columns:
        df['Bank']

    # Create the 'Account' column, fill with -(Debit) and Credit
    if 'Account' not in df.columns:
        df['Account']

def fill_cols(df):
    # edit description

    # edit amount
    df['Amount'] = -df['Debit'].fillna(0) + df['Credit'].fillna(0)

    # edit category 

    # edit bank

    # edit account 
    

def remove_cols(df):
    # drop unnessessary columns
    for column in ["Account Number", "Check", "Status", "Balance", "Debit", "Credit"]:
        if column in df.columns:
            df = df.drop(columns=[column])

def main():
    # Adjust the path to the Mappings folder
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # mappings_dir = os.path.join(script_dir, '..', 'Mappings')
    # mapping_file_path = os.path.join(mappings_dir, 'Descriptions.txt')
    # mapping = load_mapping(mapping_file_path)

    # target_folder, file_names = get_file_path()
    # process_csv_files(target_folder, file_names, mapping)

    target_folder, file_names = get_file_path()
    process_csv_files(target_folder, file_names)

    # target_folder = get_target_path()  # Assuming get_target_path still returns the target folder
    # file_paths = get_file_path(target_folder)
    # process_csv_files(file_paths)

if __name__ == "__main__":
    main()
