# transaction_processing.csv
# add new data & processing to RBC transaction .csv files

import pandas as pd
import numpy as np
import argparse
import os
from datetime import datetime

def transaction_processing(in_file):
    df = pd.read_csv(in_file)  # load data

    # edit columns
    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"]).dt.strftime('%Y-%m-%d')
    df["Type"] = np.where(df["CAD$"] > 0, "Income", "Purchase")
    df["Amount"] = abs(df["CAD$"])
    df = df.drop(columns=["Cheque Number", "CAD$", "USD$"])

    # drop unwanted entries (internal transfers, payments, autodeposit)
    credit_pay_str = "PAYMENT - THANK YOU / PAIEMENT - MERCI"  # long string
    df = df.loc[~(df["Description 1"].isin(["Transfer", "Payment", "PAYMENT", credit_pay_str, "E-TRF AUTODEPOSIT"]) |
                df["Description 1"].str.contains("WWW TRF DDA*"))
        ]

    #df["category"] = asssign_category()  # TODO have a dictionary file with available input
    #df["subcategory"] = asssign_subcategory()

    # save processed .csv
    print(df)
    root_dir = os.path.dirname(in_file)
    date = datetime.today().strftime('%Y-%m-%d')
    ext = ".csv"
    out_file = os.path.join(root_dir, "Transactions " + date + ext)
    df.to_csv(out_file)

if __name__ == "__main__":
    try:
        # set up argparser
        parser = argparse.ArgumentParser()
        parser.add_argument("file", type=str, help="File to process.")

        # get args
        args = parser.parse_args()
        in_file = args.file

        # start pass to script
        transaction_processing(in_file)
    except KeyboardInterrupt:
        print('User has exited the program')