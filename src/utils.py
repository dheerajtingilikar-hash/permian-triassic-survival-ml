import pandas as pd

def clean_occurrences(path):

    df = pd.read_csv(path)

    cols = [
        'accepted_name',
        'early_interval',
        'late_interval',
        'paleolat',
        'paleolng',
        'environment',
        'collection_no'
    ]

    df = df[cols]

    df.dropna(inplace=True)

    return df