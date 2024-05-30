import csv
import sqlite3
import os

FILES = {
  "bofa credit.csv",
  "bofa savings.csv",
  "chase credit.csv"
}

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

######################################################################################### load_mappings
def load_mappings(file_path):
  mapping = {}
  with open(file_path, 'r') as file:
    for line in file:
      key, value = line.strip().split('=')
      mapping[key] = value
  return mapping

description_mapping = load_mappings("description_mapping.txt")
category_mapping = load_mappings("category_mapping.txt")

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
        # [skip header, date row, description row, amount row]
        csv_key_map = {
          "bofa credit.csv": [1,0,2,4],
          "bofa savings.csv": [7,0,1,2],
          "chase credit.csv": [1,1,2,5],
        }

        if file in csv_key_map:
          print(f"Processing: {file}")
          fill_table(cursor, os.path.join(data_folder_path, file), csv_key_map[file])
        else:
          print(f"Error: {file} Function Not Found")

############################################################################################ fill_table
def fill_table(cursor, file_path, key):
  with open(file_path, 'r') as file:
    reader = csv.reader(file)
    for _ in range(key[0]):
      next(reader)

    for row in reader:
      month, day, year = row[key[1]].split('/')
      month = MONTHS.get(int(month))

      date = str(row[key[1]])
      description = description_mapping.get(row[key[2]], "None")
      amount = row[key[3]] if row[key[3]] is not None and row[key[3]] != '' else 0.00
      category = category_mapping.get(row[key[2]], "None")

      filename = os.path.basename(file_path).split(" ", 1)
      bank = filename[0]
      account = filename[1].split(".")[0]

      insert_query = """
        INSERT INTO transactions (year, month, date, description, amount, category, bank, account)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)  
      """
      cursor.execute(insert_query, (year, month, date, description, amount, category, bank, account))

  cursor.connection.commit()

###################################################################################### remove_duplicate
def remove_duplicate(cursor):
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
    remove_duplicate(cursor)

    connection.commit()
    connection.close()

    print("Success")

if __name__ == "__main__":
  main()