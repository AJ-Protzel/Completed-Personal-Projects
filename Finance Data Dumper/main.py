import csv
import sqlite3
import os

MONTHS = {
  1: "January",
  2: "February",
  3: "March",
  4: "April",
  5: "May",
  6: "June",
  7: "July",
  8: "August",
  9: "September",
  10: "October",
  11: "November",
  12: "December"
}

#======================================================================================== load_mappings
def load_mappings(file_path):
  mapping = {}
  with open(file_path, 'r') as file:
    for line in file:
      key, value = line.strip().split('=')
      mapping[key] = value
  return mapping

description_mapping = load_mappings("description_mapping.txt")
category_mapping = load_mappings("category_mapping.txt")

#===================================================================================== contains_keyword
def contains_keyword(text):
  with open("key.txt", "r") as file:
    words = file.readlines()
    words = [word.strip() for word in words]
  
  for word in words:
    if word.lower() in text.lower():
      return word.lower()
  return None

########################################################################################## create_table
def create_table(cursor):
  create_table_query = """
    CREATE TABLE IF NOT EXISTS transactions (
      year INTEGER,
      month TEXT,
      date TEXT,
      description TEXT,
      amount REAL,
      category TEXT,
      bank TEXT,
      account TEXT
    )
  """
  cursor.execute(create_table_query)

############################################################################################ read_files
def read_files(cursor, data_folder_path):
    for file in os.listdir(data_folder_path):
        # [skip lines, date, description, debit-, credit+]
        csv_key_map = {
          "redneck checking.csv": [1,1,3,4,5],
          "redneck savings.csv": [1,1,3,4,5],
          "bofa credit.csv": [1,0,2,4,0],
          "bofa savings.csv": [7,0,1,2,0],
          "prime credit.csv": [1,1,2,5,0],
          "chase credit.csv": [1,1,2,5,0],
        }

        if file in csv_key_map:
          print(f"Processing: {file}")
          fill_table(cursor, os.path.join(data_folder_path, file), csv_key_map[file])
        else:
          print(f"Error: {file}")

############################################################################################ fill_table
def fill_table(cursor, file_path, key):
  with open(file_path, 'r') as file:
    reader = csv.reader(file)
    for _ in range(key[0]):
      next(reader)

    for row in reader:
      if row[key[3]] == '' and row[key[4]] == '':
        continue

      month, day, year = row[key[1]].split('/')
      month = MONTHS.get(int(month))
      date = str(row[key[1]])

      filename = os.path.basename(file_path).split(" ", 1)
      bank = filename[0]
      account = filename[1].split(".")[0]
      
      amount = get_amount(row[key[3]], row[key[4]], bank, account)

      description = get_description(row[key[2]], amount)

      category = get_category(description)

      insert_query = """
        INSERT INTO transactions (year, month, date, description, amount, category, bank, account)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)  
      """
      cursor.execute(insert_query, (year, month, date, description, amount, category, bank, account))

  cursor.connection.commit()

#-------------------------------------------------------------------------------------- get_description
def get_description(desc, amount):
  description = contains_keyword(desc)
  if description == "ach debit" or "ach credit":
    description = "transfer"

  if description is None:
    description = description_mapping.get(desc, None)
    if description is None:
      user_input = input(f"Description {amount} {desc} = ")
      user_input.lower()
      with open('description_mapping.txt', 'a') as mapping_file:
        mapping_file.write(f"{desc}={user_input}\n")
      description = user_input
  
    with open('key.txt', 'a') as key_file:
      key_file.write(f"{description}\n")

  return description.lower()

#----------------------------------------------------------------------------------------- get_category
def get_category(desc):
  category = category_mapping.get(desc, None)
  if category is None:
    user_input = input(f"Category {desc} = ")
    user_input.lower()
    with open('category_mapping.txt', 'a') as mapping_file:
      mapping_file.write(f"{desc}={user_input}\n")
    category = user_input
  
  return category.lower()

#------------------------------------------------------------------------------------------- get_amount
def get_amount(debit, credit, bank, account):
  if bank == "redneck":
    if debit != '':
      amount = float(debit) * -1
    else:
      amount = float(credit)
  else:
    print("=========",debit)
    amount = float(debit.replace(",", ""))
    if account == "credit":
      amount = amount * -1
  
  return amount

##################################################################################### remove_duplicates
def remove_duplicates(cursor):
    deduplication_query = """
        DELETE FROM transactions AS t1
        WHERE EXISTS (
            SELECT 1
            FROM transactions AS t2
            WHERE t1.year = t2.year
                AND t1.month = t2.month
                AND t1.date = t2.date
                AND t1.description = t2.description
                AND t1.amount = t2.amount
                AND t1.category = t2.category
                AND t1.bank = t2.bank
                AND t1.account = t2.account
                AND t1.rowid > t2.rowid
        );
    """
    cursor.execute(deduplication_query)

#######################################################################################################
################################################################################################## Main
#######################################################################################################
def main():
    data_folder_path = "data"
    database_file = "main.db"
    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    create_table(cursor)
    read_files(cursor, data_folder_path)
    remove_duplicates(cursor)

    connection.commit()
    connection.close()

    print("Success")

if __name__ == "__main__":
  main()