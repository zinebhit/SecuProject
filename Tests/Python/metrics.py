import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame
# visualization library
# import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.dates as mdates
import matplotlib.cm as cm
from matplotlib.colors import Normalize

# Efficiency
from numba import njit, prange
# Date Time
from datetime import timedelta


class Metrics:
    def __init__(self, df_anonymized, df_original):
        assert(len(df_anonymized) == len(df_original))
        self.df_anonymized = df_anonymized
        self.df_original = df_original
        self.number_of_lines = len(df_original)
    
    def calculate_all(self, poi=False, graph=True):
        score = {'date': 0, 'hour': 0, 'poi':0, 'meet': 0, 'tuile': 0, 'distance': 0}
        score['date'] = self.date()
        print('Date : ', score['date'])
        
        score['hour'] = self.hour()
        print('Hour : ', score['hour'])
        
        score['distance'] = self.distance()
        print('Distance : ', score['distance'])
        
        score['meet'] = self.meet()
        print('Meet : ', score['meet'])
        
        score['tuile'] = self.tuile()
        print('Tuile : ', score['tuile'])
        if poi:
            score['poi'] = self.poi()
            print('Poi : ', score['poi'])
        else:
            score.pop('poi')
        
        print('------------------------')
        mean = list(score.values())
        mean = sum(mean) / len(mean)
        print('Mean : ', mean)
        
        #---------------------------------
        names = list(score.keys())
        values = list(score.values())
        fig, ax = plt.subplots(1, 1)
        # get a color map
        my_cmap = cm.get_cmap('jet')
        # get normalize function (takes data in range [vmin, vmax] -> [0, 1])
        my_norm = Normalize(vmin=0, vmax=5)
        my_data = 5 * np.random.rand(5)
        ax.bar(names, values, color=my_cmap(my_norm(my_data)))

        plt.show() 
        #---------------------------------
    
    def all_complicate_and_slow(self):
        # distance + date + hour
        @njit(parallel=True)
        def support(anonymized_weeks, original_weeks, 
                    anonymized_dates, original_dates,
                    anonymized_hours, original_hours,
                    distance_differences):
            N = len(anonymized_weeks)
            dx = 0.1
            hourdec = [
                1, 0.9, 0.8, 0.6, 0.4, 0.2, 0, 0.1, 0.2, 0.3,
                0.4, 0.5, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0, 0.2,
                0.4, 0.6, 0.8, 0.9
            ]
            hour, date, distance = 0, 0, 0
            for i in prange(N):
                # ---------------in same week----------
                if anonymized_weeks[i] != original_weeks[i]:
                    print('Index : ', i)
                    print('Anonymized week :', anonymized_weeks[i])
                    print('Original week :', original_weeks[i])
                    raise AssertionError()
                # #####################################
                
                
                # ----------------date-----------------
                difference = anonymized_dates[i] - original_dates[i]
                if difference == -2 or difference == -1:
                    date += 3 + difference
                elif difference == 0 or difference == 1 or difference == 2:
                    date += 3 - difference
                # #####################################

                
                # ----------------hour-----------------
                hour += hourdec[abs(anonymized_hours[i] - original_hours[i])]
                # #####################################

                
                # ----------------distance-----------------
                tmp = distance_differences[i] * (1/dx) + 1
                tmp = 0 if tmp <= 0 else tmp
                distance += tmp
                # #####################################
            date /= N*3
            hour /= N
            distance /= N
            return [date, hour, distance]
        
        df_distance_diff = (self.df_anonymized.X - self.df_original.X).abs() + (self.df_anonymized.Y - self.df_original.Y).abs()

        date, hour, distance = support(self.df_anonymized.DateTime.dt.dayofweek.values, self.df_original.DateTime.dt.dayofweek.values,
                    self.df_anonymized.DateTime.dt.dayofweek.values, self.df_original.DateTime.dt.dayofweek.values,
                    self.df_anonymized.DateTime.dt.hour.values, self.df_original.DateTime.dt.hour.values,
                    df_distance_diff.to_numpy())
        print('Date : ', date)
        print('Hour : ', hour)
        print('Distance : ', distance)
        score = [date, hour, distance]
        mean = sum(score) / len(score)
        print('-----------------\nMean : ', mean)
        return mean
    
    def meet(self):
        percentage = 0.1
        self.add_rounded_X_Y_columns(self.df_anonymized)
        self.add_rounded_X_Y_columns(self.df_original)
        
        df_original_unique = self.df_original.drop_duplicates(subset=['RoundedX', 'RoundedY', 'ID'])
        meet_table = df_original_unique.groupby(['RoundedX', 'RoundedY']).size().reset_index(
                name='Counts')
        table_size_keep = int(meet_table.shape[0] * percentage) + 1
        meet_table = meet_table.sort_values(['Counts'], ascending=False).head(table_size_keep)
        
        anonymized_unique_xy = self.df_anonymized.drop_duplicates(subset=['RoundedX', 'RoundedY'])
        
        score = anonymized_unique_xy.merge(meet_table, how='inner', on=['RoundedX', 'RoundedY']).shape[0] / table_size_keep
        
        return score

    def distance(self):
        @njit(parallel=True)
        def formula(diffs):
            N = len(diffs)
            score = 0
            dx = 0.1
            for i in prange(N):
                tmp = diffs[i] * (-1/dx) + 1
                tmp = 0 if tmp <= 0 else tmp
                score += tmp
            return score /N
        df_distance_diff = (self.df_anonymized.X - self.df_original.X).abs() + \
            (self.df_anonymized.Y - self.df_original.Y).abs()
        score = formula(df_distance_diff.to_numpy())
        return score
    
    def tuile(self):
        def regroup_points(df):
            return df.groupby(['RoundedX', 'RoundedY']).size().reset_index(
                name='Counts').sort_values(['Counts'], ascending=False)

        def support(x, y):
            if x == 0 or y == 0:
                return 0
            return y / x if x > y else x / y
        self.add_rounded_X_Y_columns(self.df_anonymized)
        self.add_rounded_X_Y_columns(self.df_original)
        anonymized_xy = regroup_points(self.df_anonymized)
        original_xy = regroup_points(self.df_original)
        joins = original_xy.merge(anonymized_xy, how='left', on=[
                                  'RoundedX', 'RoundedY']).fillna(0)
        return joins.apply(lambda row: support(row['Counts_x'],
                                               row['Counts_y']), axis=1).sum() / len(joins)

    def date(self):
        @njit(parallel=True)
        def days_difference_optimized(anonymized_dates, original_dates):
            N = len(original_dates)
            score = 0
            for i in prange(N):
                difference = anonymized_dates[i] - original_dates[i]
                if difference == -2 or difference == -1:
                    score += 3 + difference
                elif difference == 0 or difference == 1 or difference == 2:
                    score += 3 - difference
            return score / N / 3

        @njit(parallel=True)
        def in_same_week(anonymized_weeks, original_weeks, N):
            # N = len(original_weeks)
            for i in prange(N):
                if anonymized_weeks[i] != original_weeks[i]:
                    print('Error! Index = ', i)
                    print('Anonymized week :', anonymized_weeks[i])
                    print('Original week :', original_weeks[i])
                    return False
            return True

        # print(self.df_anonymized['DateTime'].dt.isocalendar().week.values)
        if not in_same_week(self.df_anonymized['DateTime'].dt.isocalendar().week.to_numpy(dtype=int), self.df_original['DateTime'].dt.isocalendar().week.to_numpy(dtype=int), self.number_of_lines):
            raise Exception("Weeks must be the same!")

        date_score = days_difference_optimized(
            self.df_anonymized.DateTime.dt.dayofweek.values, self.df_original.DateTime.dt.dayofweek.values)
        #         print('Date Utility :', date_score)
        return date_score

    def hour(self):
        @njit(parallel=True)
        def hours_difference_optimized(anonymized_hours, original_hours):
            N = len(original_hours)
            hourdec = [
                1, 0.9, 0.8, 0.6, 0.4, 0.2, 0, 0.1, 0.2, 0.3,
                0.4, 0.5, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0, 0.2,
                0.4, 0.6, 0.8, 0.9
            ]
            score = 0
            for i in prange(N):
                score += hourdec[abs(anonymized_hours[i] - original_hours[i])]
            return score / N

        date_score = hours_difference_optimized(
            self.df_anonymized.DateTime.dt.hour.values, self.df_original.DateTime.dt.hour.values)
        #         print('Hour Utility :', date_score)
        return date_score
    
    def poi(self):
        # Using code of INSA
        return Old.insa_poi(self.df_anonymized, self.df_original, len(self.df_original))
        
    def poi_according_to_my_interpretation(self):
        @njit(parallel=True)
        def assign_poi_label_support(df_hours, df_weekdays):
            N = len(df_hours)
            poi_list = np.zeros((N), dtype=np.int64)
            score = 0
            for i in prange(N):
                hour = df_hours[i]
                if hour >= 22 or hour < 6:
                    poi_list[i] = 1
                elif df_weekdays[i] == 5 or df_weekdays[i] == 6:
                    # if week-end
                    if hour >= 10 and hour < 18:
                        poi_list[i] = 3
                else:
                    if hour >= 9 and hour < 18:
                        poi_list[i] = 2
            return poi_list

        def assign_poi_label(df):
            df['PoiLabel'] = assign_poi_label_support(
                df.DateTime.dt.hour.values, df.DateTime.dt.weekday.values)

        def add_day_of_week(df):
            df['DayOfWeek'] = df.DateTime.dt.dayofweek

        def add_week_of_year_column(df):
            df['WeekOfYear'] = df.DateTime.dt.isocalendar().week

        # 0 : nothing;
        # 1 : home
        # 2 : work
        # 3 : activity
        # Assigning POI label
        assign_poi_label(self.df_anonymized)
        assign_poi_label(self.df_original)
        #         print(self.df_anonymized)
        #         print(self.df_original)
        add_week_of_year_column(self.df_anonymized)
        add_week_of_year_column(self.df_original)

        add_day_of_week(self.df_anonymized)
        add_day_of_week(self.df_original)

        self.add_rounded_X_Y_columns(self.df_anonymized)
        self.add_rounded_X_Y_columns(self.df_original)

        original_poi_table = self.df_original[self.df_original.PoiLabel != 0].groupby('ID').apply(lambda x: x.groupby(
            ['WeekOfYear', 'PoiLabel', 'RoundedX', 'RoundedY']).size().reset_index(name='Counts').sort_values(
            ['WeekOfYear', 'PoiLabel', 'Counts', ], ascending=False).groupby(['WeekOfYear', 'PoiLabel']).head(1))
        print(original_poi_table)
        # Filter
        anonymized_poi = self.df_anonymized.loc[:, [
            'ID', 'PoiLabel', 'WeekOfYear', 'RoundedX', 'RoundedY']]
        anonymized_poi = anonymized_poi[anonymized_poi['PoiLabel'] != 0]

        score = 0
        for index, row in original_poi_table.iterrows():
            id, _ = index
            WeekOfYear, PoiLabel, RoundedX, RoundedY, Counts = row
            tmp = anonymized_poi.loc[(anonymized_poi.ID == id) & (anonymized_poi.WeekOfYear == WeekOfYear) & (anonymized_poi.PoiLabel == PoiLabel)
                                     & (anonymized_poi.RoundedX == RoundedX) & (anonymized_poi.RoundedY == RoundedY)].shape[0]
            score += tmp / Counts
            # if (tmp/Counts != 1):
            #     print a(tmp, Counts, id, WeekOfYear, PoiLabel, RoundedX, RoundedY)
        score /= len(original_poi_table)
        return score

    def add_rounded_X_Y_columns(self, df):
        if not 'RoundedX' in df.columns:
            df['RoundedX'] = df.X.round(2)
        if not 'RoundedY' in df.columns:
            df['RoundedY'] = df.Y.round(2)

