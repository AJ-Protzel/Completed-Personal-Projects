import os

def create_empty_csv(output_file):
    """Create an empty CSV file with the specified name."""
    with open(output_file, 'w') as file:
        pass  # Just create the file without writing anything to it

def compile_credit_amazon(root_dir):
    for subdir, _, _ in os.walk(root_dir):
        if "Amazon" in subdir:
            output_file = os.path.join(subdir, "compiled.csv")
            print(f"Creating empty CSV file: {output_file}")
            create_empty_csv(output_file)

# Example usage
if __name__ == "__main__":
    compile_credit_amazon("Data/Credit/Amazon")