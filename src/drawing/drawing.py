import random
import pandas as pd

def drawing():
    # Read index.xlsx
    data = pd.read_excel('src\drawing\index.xlsx')

    # Shuffle the DataFrame rows
    shuffled_data = data.sample(frac=1).reset_index(drop=True)

    # Get a random row (entry) from the shuffled DataFrame
    random_entry = shuffled_data.sample()

    # Extract key and value from the random entry
    key = random_entry.index[0]
    value = random_entry.iloc[0]

    # Print key and value
    print("Selected entry:")
    print("Key:", key)
    print("Value:", value)

if __name__ == "__main__":
    drawing()
