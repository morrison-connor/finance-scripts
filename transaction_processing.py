# transaction_processing.csv
# add new data & processing to RBC transaction .csv files

import pandas as pd
import numpy as np

credit_pay_str = "PAYMENT - THANK YOU / PAIEMENT - MERCI"  # long string TODO may as well store all strings to help decode & flexibility

#root_dir = "C:/Users/Connor/Documents/MY DOCS/Finances/Transaction CSVs"  # TODO figure out pathlib
in_file = "C:/Users/Connor/Documents/MY DOCS/Finances/Transaction CSVs/csv37953.csv"  # \ causes escape characters
df = pd.read_csv(in_file)

# rename existing columns
df = df.rename(
    columns={
        "CAD$": "Amount",
    }
)

# add new columns
df["Type"] = np.where(df["Amount"] > 0, "Income", "Purchase")

# filter unwanted data to prevent double counting from transfers

# df = df.loc[~((df["Account Type"] == "Chequing") &
#               (df["Type"] == "Income"))]  # drop income in chequing act (not really relevant?)
# df = df.loc[~((df["Account Type"] == "Savings") &
#               (df["Type"] == "Purchase"))]  # drop purchases from savings act (some transfers to chequing)

# drop internal transfers, payments, autodeposit
df = df.loc[~(df["Description 1"].isin(["Transfer", "Payment", "PAYMENT", credit_pay_str, "E-TRF AUTODEPOSIT"]) |
              df["Description 1"].str.contains("WWW TRF DDA*"))
    ]


#df["category"] = asssign_category()  # TODO have a dictionary file with available input
#df["subcategory"] = asssign_subcategory()


# save processed .csv
print(df)

# outfile = "" root_dir + name (processed_date_transactions)