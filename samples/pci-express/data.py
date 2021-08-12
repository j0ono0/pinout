# Example of importing data from a spreadsheet
#
# Python has multiple options for reading popular spreadsheet formats.
# This example uses Pandas in conjunction with openpyxl.
# Installation of these packages can be done via the command line.
# (**If you are using a virtual environment, ensure it is activated):
# >>> pip install pandas
# >>> pip install openpyxl
import pandas as pd


def assign_css(text):
    # Rather than alter then source data css classes can be
    # figured out and assigned here
    if text == "Ground":
        return "gnd"
    elif text in ["SMCLK", "SMDAT", "WAKE#", "PERST#", "CLKREQ#", "PWRBRK#"]:
        return "open-drain"
    elif text.startswith("+"):
        return "pwr"
    elif text.startswith("HSO") or text.startswith("REFCLK"):
        return "host-to-card"
    elif text.startswith("HSI") or text == "TDO":
        return "card-to-host"
    elif text.startswith("PRSNT"):
        return "sense-pin"
    return "reserved"


def get_from_xlsx(filepath):
    # read the excel spreadsheet into a 'dataframe'
    df = pd.read_excel(filepath, engine="openpyxl")

    # Remove the Description column as we are not using it
    df.drop("Description", axis=1, inplace=True)

    # Remove the rows that have notes (rather than data).
    # Luckily, those rows all have 'None' in at least one column
    df.dropna(inplace=True)

    # Problem characters are easy to replace with Pandas.
    # In this instance a minus sign is causing grief.
    df["Side A"] = df["Side A"].str.replace("−", "&#x2212;")

    # Parse the data for use with pinout
    data = df.values.tolist()
    data = [
        [
            (f"{i}", "pinid", {"body": {"width": 30}}),
            (f"{b}", assign_css(b)),
            (f"{a}", assign_css(a)),
        ]
        for (i, b, a) in data
    ]

    return data


if __name__ == "__main__":
    get_from_xlsx("pci-express_data.xlsx")