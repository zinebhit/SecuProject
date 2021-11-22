from optimization.speed_up_random import *
import numpy as np
from tqdm import tqdm


class Defense:

    def __init__(self):
        self.old_to_new = None
        self.new_to_old = None

    def disturb_id(self, df_original):
        """
        This function will replace every unique (ID, Week) by a new ID
        """
        df = df_original.copy()
        all_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"

        # Check if df already has the 'Week' column
        if 'Week' not in df.columns:
            df['Week'] = df.DateTime.dt.isocalendar().week

        # Choose only ID and Week columns, then remove duplicates by keeping (ID, Week) unique
        id_week_unique = df.loc[:, ['ID', 'Week']].drop_duplicates(['ID', 'Week'])

        # Now we have 449 unique values (ID, Week)
        # print(id_week_unique)

        # Use dictionary of dictionary - [ID][Week] to speed up retrieving values.
        # This is not really necessary because we have only 449 values.
        # But it helps, anyway! We'll have to retrieve N=34 000 000 times
        new_to_old, old_to_new = {}, {}
        for _, _id, week in id_week_unique.itertuples():
            anonymized_id = ''.join({all_characters[randint(0, 93)] for i in range(4)})
            # If dictionary wasn't existed, create and add values
            try:
                old_to_new[_id][week] = anonymized_id
            except:
                old_to_new[_id] = {week: anonymized_id}

            try:
                new_to_old[anonymized_id][week] = _id
            except:
                new_to_old[anonymized_id] = {week: _id}

        # Create an numpy-string-array to store new_id when we go through the table
        new_ids = np.zeros((len(df)), dtype=object)

        # Iterate through the table, for each row, save the ID
        for i, row in tqdm(enumerate(df.itertuples()), total=df.shape[0]):
            new_ids[i] = old_to_new[row.ID][row.Week]

        df.ID = new_ids

        self.old_to_new = old_to_new
        self.new_to_old = new_to_old

        return df
