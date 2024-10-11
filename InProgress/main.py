import os
from compilers import compile_credit_bilt, compile_credit_amazon, compile_credit_bofa, compile_credit_flex, compile_credit_sapphire, compile_debit_bofa

def main():
    root_dir = "Data"
    account_types = {
        "credit_bilt": compile_credit_bilt,
        "credit_amazon": compile_credit_amazon,
        "credit_bofa": compile_credit_bofa,
        "credit_flex": compile_credit_flex,
        "credit_sapphire": compile_credit_sapphire,
        "debit_bofa": compile_debit_bofa
    }

    for compile_function in account_types.values():
        compile_function(root_dir)

if __name__ == "__main__":
    main()
    print("complete")
