import json
import pandas as pd
import numpy as np
from sortedcontainers import SortedList
import random
from numba import njit, prange
from datetime import datetime, date, timedelta, time
from tqdm import tqdm
import math


@njit
def seed(a):
    random.seed(a)


@njit
def rand():
    return random.random()


@njit
def randint(a, b):
    return random.randint(a, b)


@njit
def floor(a):
    return math.floor(a)


def load_tuile(tuile_file_name):
    with open(tuile_file_name, 'r') as file:
        return json.load(file)


def load_meet(meet_file_name):
    with open(meet_file_name, 'r') as file:
        data_meet = {}
        for line in file.readlines():
            line = line.strip().split('\t')
            X = float(line[0])
            Y = float(line[1])
            meet = int(line[2])
            try:
                data_meet[X][Y] = meet
            except:
                data_meet[X] = {Y: meet}
        return data_meet


def load_poi_dict(poi_file_name):
    with open(poi_file_name, 'r') as file:
        data_poi = {}
        for line in file.readlines():
            line = line.strip().split('\t')
            ID = line[0]
            poi_type = line[1]
            X = float(line[2])
            Y = float(line[3])
            seconds = int(float(line[4]))
            data_poi[(ID, poi_type, X, Y)] = seconds
        return data_poi


def load_poi_data_frame(poi_file_name):
    column_names = ["ID", "Type", "RoundedX", "RoundedY", "Duration"]
    dtypes = {'ID': 'str', "Type": 'str', 'RoundedX': 'float64', 'RoundedY': 'float64', "Duration": 'float64'}
    df = pd.read_csv(poi_file_name, sep='\t', header=None, names=column_names, dtype=dtypes)
    return df


class Build:
    def __init__(self, df,
                 poi_data,
                 meet_data,
                 tuile_data,
                 meet_file,
                 poi_dataframe):
        self.df = df.copy()
        self.add_columns()
        self.poi_data = poi_data.copy()
        self.meet_data = meet_data.copy()
        self.tuile_data = tuile_data.copy()
        self.N = len(df)
        self.meet_file = meet_file
        self.meet_size = sum(len(meet_data[key]) for key in meet_data)
        self.poi_dataframe = poi_dataframe
        self.init_poi()

        self.parameters()

        self.ID = self.df.ID.copy().to_numpy()
        self.X = np.zeros(self.N, dtype=float)
        self.Y = np.zeros(self.N, dtype=float)
        self.Type = np.zeros(self.N, dtype='U')  # string
        self.Sensible = np.zeros(self.N, dtype=int)

        self.tuile = {}
        for _id in df.ID.unique():
            self.tuile[_id] = set()
        self.tuile_fairy_points = {}
        for _id in df.ID.unique():
            self.tuile_fairy_points[_id] = [set(), []]

        self.DayOfWeek = np.ones(self.N, dtype=np.int8)
        self.Week = self.df.Week.to_numpy()
        self.Hour = np.zeros(self.N, dtype=int)
        self.Minute = np.zeros(self.N, dtype=int)
        self.Second = np.ones(self.N, dtype=int)

    def init_poi(self):
        tmp = self.poi_dataframe.drop_duplicates(['RoundedX', 'RoundedY'])
        _x = tmp.RoundedX.copy().to_numpy()
        _y = tmp.RoundedY.copy().to_numpy()
        d = []
        for i in range(len(_x)):
            d.append((_x[i], _y[i]))
        self.except_x_y = d
        self.poi_id_dict = {}
        self.list_poi_x_y = []
        self.poi_sorted = {}

        for i, _id, _type, rounded_x, rounded_y, duration in self.poi_dataframe.itertuples():
            if _id in self.poi_id_dict:
                self.poi_sorted[_id].append((rounded_x, rounded_y))
                self.poi_id_dict[_id].append((_type, rounded_x, rounded_y, duration))
            else:
                self.poi_sorted[_id] = [(rounded_x, rounded_y)]
                self.poi_id_dict[_id] = [(_type, rounded_x, rounded_y, duration)]
            if (rounded_x, rounded_y) not in self.list_poi_x_y:
                self.list_poi_x_y.append((rounded_x, rounded_y))


    def parameters(self):
        self.EU = 0.7
        self.meet_sacrify_points = round(self.meet_size * 0.1)
        self.number_same_id_week = 4
        self.keep_distance = 0.1
        self.same_week_id = 2

    def main(self):
        self.retrieve_fairy_point()

        self.step_one()

        self.improve_distance()

        self.assign_big_point_randomly()

        self.step_5_datetime()

        self.step_6_poi()

        self.delete()

        self.step_three()

        self.disturb_id()

    def step_one(self):

        def min_max(a):
            return (a[0] - 0.0049, a[0] + 0.0049), (a[1] - 0.0049, a[1] + 0.0049)

        def distance(left_x, x):
            if left_x[0] <= x and x <= left_x[1]:
                distance_x = 0
            elif left_x[0] > x:
                distance_x = left_x[0] - x
                x = left_x[0]
            elif left_x[1] < x:
                distance_x = x - left_x[1]
                x = left_x[1]
            else:
                print('Error')
            return distance_x, x

        f = lambda a, x, y: abs(a[0] - x) + abs(a[1] - y)
        check = lambda a, x, y: a[0] + 0.0049 > x and x > a[0] - 0.0049 and a[1] + 0.0049 > y and y > a[1] - 0.0049
        fix_suffix = lambda x: (floor(x * 10000) + rand()) / 10000
        changed_lines = 0
        df_view = self.df.loc[:, ['ID', 'X', 'Y']]
        for index, _id, x, y in tqdm(df_view.itertuples(), total=self.N):
            if self.Sensible[index] == 1:
                continue
            place_index = self.fairy_points.bisect_right((x, y))
            try:
                left, right = self.fairy_points[place_index], self.fairy_points[place_index + 1]
                left_x, left_y = min_max(left)
                right_x, right_y = min_max(right)

                left_distance_x, left_x0 = distance(left_x, x)
                left_distance_y, left_y0 = distance(left_y, y)
                right_distance_x, right_x0 = distance(right_x, x)
                right_distance_y, right_y0 = distance(right_y, y)

                diff_left0 = left_distance_x + left_distance_y
                diff_right0 = right_distance_x + right_distance_y
                if (diff_left0 > diff_right0):
                    diff_left0 = diff_right0
                    left_x0 = right_x0
                    left_y0 = right_y0
                    left_x, left_y = right_x, right_y
                    left = right
                if diff_left0 >= 0.1: continue
                new_x, new_y = fix_suffix(left_x0), fix_suffix(left_y0)
                if diff_left0 >= 0.8:
                    print("Eureka!!!")
                    print(left)
                    print('x, y :', x, y, ' index :', place_index)
                    print(diff_left0, left_x0, left_y0)
                    print(new_x, new_y)
                    print('Check round:', round(new_x, 2), round(new_y, 2))
                assert round(new_x, 2) == left[0] and round(new_y, 2) == left[1]
                self.tuile[_id].add(left)
                if left not in self.tuile_fairy_points[_id][0]:
                    self.tuile_fairy_points[_id][1].append(left)
                self.tuile_fairy_points[_id][0].add(left)
                changed_lines += 1

                assert self.Sensible[index] != 1
                self.X[index], self.Y[index] = new_x, new_y
                self.Sensible[index] = 2
            except IndexError:
                pass
        print('      ', changed_lines, ' rows are changed successfully !')

    def improve_distance(self):
        self.generate_conserved_points()
        df_view = self.df.loc[:, ['ID', 'Week', 'X', 'Y', 'RoundedX', 'RoundedY']]
        CP = self.conserved_points
        changed_lines = 0

        for index, _id, week, x, y, rounded_x, rounded_y in tqdm(df_view.itertuples(), total=df_view.shape[0]):
            if self.Sensible[index] != 0 or (_id, week) not in CP: continue
            if (rounded_x, rounded_y) in CP[(_id, week)]:
                if CP[(_id, week)][(rounded_x, rounded_y)] <= 0: continue
                CP[(_id, week)][(rounded_x, rounded_y)] -= 1
                self.X[index] = self.fix_suffix(x)
                self.Y[index] = self.fix_suffix(y)
                self.Sensible[index] = 3
                changed_lines += 1
        print(changed_lines, 'lines are modified successfully !')

    def get_x_y_nearly_and_not_poi(self, _id, RX, RY):
        def exist_in_dict(l, RX, RY):
            has = False
            for tup in l:
                if tup[0] == RX and tup[1] == RY:
                    has = True
                    break
            return has

        if _id == 'DEL': return 0, 0
        fix_suffix_0_1 = lambda x: (floor(x * 100) + rand()) / 100
        if not exist_in_dict(self.poi_sorted[_id], RX, RY):
            pass
        elif not exist_in_dict(self.poi_sorted[_id], RX + 0.01, RY):
            RX += 0.01
        elif not exist_in_dict(self.poi_sorted[_id], RX - 0.01, RY):
            RX -= 0.01
        elif not exist_in_dict(self.poi_sorted[_id], RX, RY + 0.01):
            RY += 0.01
        elif not exist_in_dict(self.poi_sorted[_id], RX, RY - 0.01):
            RY -= 0.01

        elif not exist_in_dict(self.poi_sorted[_id], RX + 0.02, RY):
            RX += 0.02
        elif not exist_in_dict(self.poi_sorted[_id], RX - 0.02, RY):
            RX -= 0.02
        elif not exist_in_dict(self.poi_sorted[_id], RX, RY + 0.02):
            RY += 0.02
        elif not exist_in_dict(self.poi_sorted[_id], RX, RY - 0.02):
            RY -= 0.02
        else:
            RY, RX = 0, 0
        return fix_suffix_0_1(RX), fix_suffix_0_1(RY)

    def step_6_poi(self):
        print('################################################')
        RoundedX, RoundedY = np.around(self.X, decimals=2), np.around(self.Y, decimals=2)
        fix_suffix_0_1 = lambda x: (floor(x * 100) + rand()) / 100
        #####################################################################################
        print('        Reset POI points = 0 ...')


        def is_POI(actual_date):
            if actual_date.isocalendar()[2] <= 5:
                if actual_date.time() > time(22, 0) or actual_date.time() < time(6, 0):
                    return True
                elif actual_date.time() > time(9, 0) and actual_date.time() < time(16, 0):
                    return True
            else:
                if actual_date.time() > time(10, 0) and actual_date.time() < time(18, 0):
                    return True
            return False

        def find_next_POI(actual_date):
            week_of_year, day_of_week = actual_date.isocalendar()[1:]
            hour = actual_date.hour
            hms = ()
            if day_of_week in [1, 2, 3, 4, 5]:
                if 6 <= hour and hour <= 9:
                    hms = (9, 0, 1)
                elif 16 <= hour and hour <= 22:
                    hms = (22, 0, 1)
                else:
                    assert False
            elif day_of_week == 6:
                if hour <= 10:
                    hms = (10, 0, 1)
                elif hour >= 17:
                    day_of_week += 1
                    hms = (10, 0, 1)
                else:
                    assert False
            else:
                if hour >= 18: assert False
                hms = (10, 0, 1)
            return datetime.combine(date.fromisocalendar(2015, week_of_year, day_of_week), time(*hms))

        return_datetime = lambda dt: (dt.isocalendar()[2], dt.hour, dt.minute, dt.second)
        first_line_id = []
        for i in tqdm(prange(self.N)):
            _id = self.ID[i]
            if _id not in first_line_id:
                first_line_id.append(_id)
                continue
            if _id not in self.poi_id_dict: continue
            if len(self.poi_id_dict[_id]) <= 0 or i == 0:
                continue
            if self.Week[i] != self.Week[i - 1] or self.Sensible[i] != 0 or self.Sensible[i - 1] != 0:
                continue
            j = len(self.poi_id_dict[_id]) - 1
            _type, rounded_x, rounded_y, duration = self.poi_id_dict[_id][j]
            self.X[i], self.Y[i] = rounded_x, rounded_y
            start_of_week = (0, 0, 0)
            start_of_weekend, end_of_weekend = (10, 0, 1), (17, 59, 59)
            end_of_work = (15, 59, 59)
            end_of_night = (23, 59, 59)
            if _type == 'weekend':
                self.DayOfWeek[i] = 7
                self.Hour[i], self.Minute[i], self.Second[i] = end_of_weekend
                end_day = datetime.combine(date.fromisocalendar(2015, self.Week[i], 7), time(*end_of_weekend))
                if duration < 583199:
                    begin_day = end_day - timedelta(seconds=duration)
                    if not is_POI(begin_day): begin_day = find_next_POI(begin_day)
                    self.DayOfWeek[i - 1], self.Hour[i - 1], self.Minute[i - 1], self.Second[i - 1] = return_datetime(
                        begin_day)
                    duration -= (end_day - begin_day).total_seconds()
                else:
                    begin_day = datetime.combine(date.fromisocalendar(2015, self.Week[i], 1), time(*start_of_week))
                    self.DayOfWeek[i - 1], self.Hour[i - 1], self.Minute[i - 1], self.Second[i - 1] = 1, 0, 0, 0
                    duration -= (end_day - begin_day).total_seconds()
                    assert duration >= 0

            elif _type == 'work':
                self.DayOfWeek[i] = 5
                self.Hour[i], self.Minute[i], self.Second[i] = end_of_work
                end_day = datetime.combine(date.fromisocalendar(2015, self.Week[i], 5), time(*end_of_work))
                if duration < 403199:
                    begin_day = end_day - timedelta(seconds=duration)
                    if not is_POI(begin_day): begin_day = find_next_POI(begin_day)
                    self.DayOfWeek[i - 1], self.Hour[i - 1], self.Minute[i - 1], self.Second[i - 1] = return_datetime(
                        begin_day)
                    duration -= (end_day - begin_day).total_seconds()
                else:
                    begin_day = datetime.combine(date.fromisocalendar(2015, self.Week[i], 1), time(*start_of_week))
                    self.DayOfWeek[i - 1], self.Hour[i - 1], self.Minute[i - 1], self.Second[i - 1] = 1, 0, 0, 0
                    duration -= (end_day - begin_day).total_seconds()
                    assert duration >= 0

            elif _type == 'night':
                self.DayOfWeek[i] = 5
                self.Hour[i], self.Minute[i], self.Second[i] = end_of_night
                end_day = datetime.combine(date.fromisocalendar(2015, self.Week[i], 5), time(*end_of_night))
                if duration < 431999:
                    begin_day = end_day - timedelta(seconds=duration)
                    if not is_POI(begin_day): begin_day = find_next_POI(begin_day)
                    self.DayOfWeek[i - 1], self.Hour[i - 1], self.Minute[i - 1], self.Second[i - 1] = return_datetime(
                        begin_day)
                    duration -= (end_day - begin_day).total_seconds()
                else:
                    begin_day = datetime.combine(date.fromisocalendar(2015, self.Week[i], 1), time(*start_of_week))
                    self.DayOfWeek[i - 1], self.Hour[i - 1], self.Minute[i - 1], self.Second[i - 1] = 1, 0, 0, 0
                    duration -= (end_day - begin_day).total_seconds()
                    assert duration >= 0
            else:
                assert False, "not recognize !"
            if duration < 0: assert False
            if duration == 0:
                self.poi_id_dict[_id].pop()
            else:
                self.poi_id_dict[_id][j] = (_type, rounded_x, rounded_y, duration)
            self.Sensible[i - 1], self.Sensible[i] = 5, 5
            i += 1
        print(self.poi_id_dict)

    def step_5_datetime(self):
        origin_day = self.df.DayOfWeek.to_numpy()
        good_day = lambda x: x >= 1 and x <= 7
        for i in tqdm(prange(self.N)):
            ran_day = randint(1, 9)
            if ran_day in [1, 2, 3, 7]:
                new_day = origin_day[i]
            elif ran_day in [4, 5, 6]:
                if randint(0, 1) == 1:
                    if good_day(origin_day[i] - 1):
                        new_day = origin_day[i] - 1
                    else:
                        new_day = origin_day[i] + 1
                else:
                    if good_day(origin_day[i] + 1):
                        new_day = origin_day[i] + 1
                    else:
                        new_day = origin_day[i] - 1
            elif ran_day in [8]:
                if randint(0, 1) == 1:
                    if good_day(origin_day[i] - 2):
                        new_day = origin_day[i] - 2
                    else:
                        new_day = origin_day[i] + 2
                else:
                    if good_day(origin_day[i] + 2):
                        new_day = origin_day[i] + 2
                    else:
                        new_day = origin_day[i] - 2
            else:
                for k in range(6, 1, -1):
                    if good_day(origin_day[i] - k):
                        new_day = origin_day[i] - k
                        break
                    elif good_day(origin_day[i] + k):
                        new_day = origin_day[i] + k
                        break
            self.DayOfWeek[i] = new_day
            self.Hour[i], self.Minute[i], self.Second[i] = self.hour_modify(new_day)

    def generate_conserved_points(self):
        meet_class = []
        with open(self.meet_file, 'r') as file:
            for line in file.readlines():
                line = line.strip().split('\t')
                X = float(line[0])
                Y = float(line[1])
                meet = int(line[2])
                meet_class.append((meet, X, Y))
        meet_class.sort(reverse=True)
        self.meet_class = meet_class
        conserved_points = {}
        for i_point in tqdm(prange(self.meet_sacrify_points)):
            n, x, y = meet_class[i_point]
            count_table = self.df.loc[(self.df.RoundedX == x) & (self.df.RoundedY == y), [
                'ID', 'Week', 'RoundedX', 'RoundedY']].groupby([
                'ID', 'Week']).size().reset_index(name='Count').sort_values('Count', ascending=False)
            last, tmp = 0, []
            for i, row in enumerate(count_table.itertuples()):
                index, _id, week, count = row

                if i % 3 == 0:
                    if i != 0:
                        for id_week in tmp:
                            __id, __week = id_week
                            try:
                                conserved_points[(__id, __week)][(x, y)] = last
                            except:
                                conserved_points[(__id, __week)] = {(x, y): last}
                    last = count
                    tmp = []
                else:
                    last = min(last, count)
                if count < 1000: break
                tmp.append((_id, week))
        self.conserved_points = conserved_points

    def update_tuile_data(self):
        print(self.tuile_data)
        for _id in self.tuile_data:
            self.tuile_data[_id] -= len(self.tuile[_id])
        print(self.tuile_data)

    def step_three(self):

        self.update_tuile_data()

        l = len(self.fairy_points)
        permutations = {}
        for _id in self.tuile:
            permutations[_id] = [0, np.random.permutation(self.fairy_points)]

        for i in tqdm(prange(self.N)):
            if self.Sensible[i] != 0:
                continue

            _id = self.ID[i]
            work = True
            if self.tuile_data[_id] > 0:
                tmp = permutations[_id]
                if tmp[0] >= len(tmp[1]):
                    work = False
                else:
                    new_x_y = tuple(tmp[1][tmp[0]])
                    self.test = new_x_y
                    permutations[_id][0] += 1

                    self.tuile_data[_id] -= 1
                    self.tuile[_id].add(new_x_y)
                    self.tuile_fairy_points[_id][0].add(new_x_y)
                    self.tuile_fairy_points[_id][1].append(new_x_y)
            if self.tuile_data[_id] <= 0 or not work:
                tmp = self.tuile_fairy_points[_id][1]
                if len(tmp) != 0:
                    new_x_y = tmp[randint(0, len(tmp) - 1)]
                else:
                    continue

            self.X[i], self.Y[i] = new_x_y

    def assign_big_point_randomly(self):
        indexs = np.random.randint(self.N, size=len(self.big_points))
        for i in tqdm(prange(len(indexs)), total=len(indexs)):
            index = indexs[i]
            while self.Sensible[index] != 0:
                index = randint(0, self.N - 1)
            self.X[index], self.Y[index] = self.big_points[i]
            self.Sensible[index] = 1
            self.tuile[self.ID[index]].add(self.big_points[i])
        print('      ', len(indexs), ' rows are changed successfully!!!')

    def retrieve_fairy_point(self):
        from sortedcontainers import SortedList
        fairy_points = SortedList()
        big_points = SortedList()
        for X in self.meet_data:
            for Y in self.meet_data[X]:
                value = self.meet_data[X][Y]
                if value == 0:
                    fairy_points.add((X, Y))
                else:
                    big_points.add((X, Y))
        self.fairy_points = fairy_points
        self.big_points = big_points

    def create_data_frame(self):
        self.date_list = self.concatenate_datetime()
        self.new_df = pd.DataFrame({'ID': self.ID,
                                    'DateTime': self.date_list,
                                    'X': self.X,
                                    'Y': self.Y})

    def export_to_csv(self, file_name):
        self.create_data_frame()
        self.new_df.to_csv(file_name, index=False, header=False, sep='\t')

    def concatenate_datetime(self):
        from datetime import datetime
        date_list = np.full(self.N, "", dtype=object)
        for i in tqdm(prange(self.N)):
            hour = str(self.Hour[i])
            hour = hour if len(hour) == 2 else '0' + hour
            minute = str(self.Minute[i])
            minute = minute if len(minute) == 2 else '0' + minute
            second = str(self.Second[i])
            second = second if len(second) == 2 else '0' + second
            week = str(self.Week[i])
            week = week if len(week) == 2 else '0' + week
            date_time = "2015 " + week + ' ' + str(self.DayOfWeek[i]) + ' ' + hour + ' ' + minute + ' ' + second
            date_list[i] = datetime.strptime(date_time, "%G %V %u %H %M %S")
        return date_list

    def add_columns(self):
        if 'Week' not in self.df.columns:
            self.df.loc[:, 'Week'] = self.df.DateTime.dt.isocalendar().week
        if 'DayOfWeek' not in self.df.columns:
            self.df.loc[:, 'DayOfWeek'] = self.df.DateTime.dt.isocalendar().day
        if 'Hour' not in self.df.columns:
            self.df.loc[:, 'Hour'] = self.df.DateTime.dt.hour.to_numpy()
        if 'Minute' not in self.df.columns:
            self.df.loc[:, 'Minute'] = self.df.DateTime.dt.minute.to_numpy()
        if 'Second' not in self.df.columns:
            self.df.loc[:, 'Second'] = self.df.DateTime.dt.second.to_numpy()
        if 'RoundedX' not in self.df.columns:
            self.df.loc[:, 'RoundedX'] = self.df.X.round(2)
        if 'RoundedY' not in self.df.columns:
            self.df.loc[:, 'RoundedY'] = self.df.Y.round(2)

    def statistics(self):
        unique, counts = np.unique(self.Sensible, return_counts=True)
        stats = dict(zip(unique, counts))
        for key in stats:
            print(key, ' : ', round(stats[key] / self.N * 100, 2), '%')

    def fix_suffix(self, x):
        return (floor(x * 10000) + rand()) / 10000

    def disturb_id(self):
        all_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"
        id_week_unique = self.df.loc[:, ['ID', 'Week']].drop_duplicates(['ID', 'Week'])

        new_to_old, old_to_new = {}, {}
        for _, _id, week in id_week_unique.itertuples():
            anonymized_id = ''.join({all_characters[randint(0, 93)] for i in range(10)})
            try:
                old_to_new[_id][week] = anonymized_id
            except:
                old_to_new[_id] = {week: anonymized_id}

            try:
                new_to_old[anonymized_id][week] = _id
            except:
                new_to_old[anonymized_id] = {week: _id}
        self.old_to_new = old_to_new
        self.new_to_old = new_to_old
        for i in tqdm(prange(self.N)):
            if self.ID[i] == 'DEL': continue
            self.ID[i] = old_to_new[self.ID[i]][self.Week[i]]

    def hour_modify(self, day):
        hours = [6, 7, 8, 9, 16, 17, 18, 19, 20, 21, 22] if (1 <= day <= 5) else [18, 19, 20, 21, 22, 23, 0, 1, 2, 3, 4,
                                                                                  5, 6, 7, 8, 9, 10]
        limits = [6, 9, 16, 22] if (1 <= day <= 5) else [10, 18]
        h, m, s = hours[randint(0, len(hours) - 1)], 0, 0
        if h not in limits:
            m, s = randint(0, 59), randint(0, 59)
        return h, m, s

    def add_type_column(self):
        for i in tqdm(prange(self.N)):
            if self.Second[i] == 0 and self.Minute[i] == 0 and self.Hour[i] in [10, 9, 22]:
                continue
            if self.DayOfWeek[i] in [6, 7]:
                if self.Hour[i] >= 10 and self.Hour[i] < 18:
                    self.Type[i] = 'Weekend'
            else:
                if self.Hour[i] >= 9 and self.Hour[i] < 16:
                    self.Type[i] = 'Work'
                elif self.Hour[i] >= 22 or self.Hour[i] < 6:
                    self.Type[i] = 'Night'

    def delete(self):
        k = self.df.groupby(['Week', 'ID']).size().reset_index(name='Count')
        delete_dict_id_week = {}
        for week_num in range(10, 21):
            w = k[k.Week == week_num].sort_values('Count').reset_index()
            last_count = 0
            for _index, __, _week, _id, _count in w.itertuples():
                if _index % self.same_week_id == 0:
                    last_count = _count
                else:
                    delete_dict_id_week[(_id, _week)] = _count - last_count

        for i in tqdm(prange(self.N)):
            _id, _week = self.ID[i], self.Week[i]
            if (_id, _week) in delete_dict_id_week:
                if delete_dict_id_week[(_id, _week)] != 0:
                    delete_dict_id_week[(_id, _week)] -= 1
                    self.ID[i] = "DEL"
                    self.Sensible[i] = 7




if __name__ == '__main__':
    seed(1234)
    small_data = False
    if small_data:
        meet_file = 'person12_meet_data.txt'
        poi_data = load_poi_dict('person12_poi_data.txt')
        meet_data = load_meet(meet_file)
        tuile_data = load_tuile('person12_tuile_data.txt')
        poi_dataframe = load_poi_data_frame('person12_poi_data.txt')
        data_set = 'person12.csv'
    else:
        meet_file = 'meet_data.txt'
        poi_data = load_poi_dict('poi_data.txt')
        meet_data = load_meet(meet_file)
        tuile_data = load_tuile('tuile_data.txt')
        poi_dataframe = load_poi_data_frame('poi_data.txt')
        data_set = 'data_set.csv'
    column_names = ["ID", "DateTime", "X", "Y"]
    dtypes = {'ID': 'str', 'DateTime': 'str', 'X': 'float64', 'Y': 'float64'}
    parse_dates = ['DateTime']
    data_set = pd.read_csv(data_set, sep='\t', header=None, names=column_names, dtype=dtypes,
                           parse_dates=parse_dates)

   
    TB = Build(data_set, poi_data, meet_data, tuile_data, meet_file, poi_dataframe)
   
    TB.main()
    
    TB.statistics()
    if small_data:
        TB.export_to_csv('my_small.csv')
    else:
        TB.export_to_csv('my_big.csv')

