#############################################
#                                           #
#       Flow of the training process        #
#                                           #
#############################################
from src.genetic import GeneticEngine
from src.evaluator import Evaluator
from src.dataProcessor import DataProcessor
import pandas as pd
from datetime import datetime as dt
import os

IS_DAILY = True


def load_data_daily():
    start = dt.now()

    csv_xlsx = 'data/FCPO_6_years_NUS.xlsx'

    # get training data
    csv_train = 'data/TrainDataWithInds_Daily.csv'
    if os.path.isfile(csv_train):
        data_train = pd.read_csv(csv_train)
        data_train = data_train.set_index(['DateTime'])
    else:
        df = pd.read_excel(csv_xlsx, "2011-2013")
        processor = DataProcessor(df)
        data_train = processor.process_daily(csv_train)

    # get testing data
    csv_test = 'data/TestDataWithInds_Daily.csv'
    if os.path.isfile(csv_test):
        data_test = pd.read_csv(csv_test)
        data_test = data_test.set_index(['DateTime'])
    else:
        df = pd.read_excel(csv_xlsx, "2014-2016")
        processor = DataProcessor(df)
        data_test = processor.process_daily(csv_test)

    print("::::: [main] Load daily data", dt.now() - start, ":::::")
    return data_train, data_test


def load_data():
    start = dt.now()

    csv_xlsx = 'data/FCPO_6_years_NUS.xlsx'

    # get training data
    csv_train = 'data/TrainDataWithInds.csv'
    if os.path.isfile(csv_train):
        data_train = pd.read_csv(csv_train)
        data_train = data_train.set_index(['DateTime'])
    else:
        df = pd.read_excel(csv_xlsx, "2011-2013")
        processor = DataProcessor(df)
        data_train = processor.process_raw(csv_train)

    # get testing data
    csv_test = 'data/TestDataWithInds.csv'
    if os.path.isfile(csv_test):
        data_test = pd.read_csv(csv_test)
        data_test = data_test.set_index(['DateTime'])
    else:
        df = pd.read_excel(csv_xlsx, "2014-2016")
        processor = DataProcessor(df)
        data_test = processor.process_raw(csv_test)

    print("::::: [main] Load raw data", dt.now() - start, ":::::")
    return data_train, data_test


def train(data_train):
    start = dt.now()
    engine = GeneticEngine(data_train)
    print("::::: [main] Initialize GeneticEngine", dt.now() - start, ":::::")

    start = dt.now()
    # Get the best individual and its fitness value
    best_ind = engine.best_ind()
    if best_ind is not None:
        print("::::: [main] Find the best individual", dt.now() - start, ":::::")
        evaluator = engine.evaluator
        value = evaluator.evaluate(best_ind, "data/transactions_best.csv")
        print("\n:::: [genetic] best individual", best_ind, "fitness value", value, "::::")
        return best_ind, evaluator.generator
    else:
        print("::::: [main] No individual found with positive fitness value", dt.now() - start, ":::::")
        assert (best_ind is not None)


def test(data_test, ind, rule_generator):
    start = dt.now()
    evaluator = Evaluator(data_test, rule_generator)
    rule_set = rule_generator.create_rule_set(ind)
    fit_val = evaluator.evaluate(ind, "data/transactions_test.csv")
    print("\n:::: [evaluate] individual", ind, "fitness value", fit_val, dt.now() - start, "::::")
    print(":::: Rule set ", rule_set, "::::")
    return fit_val


def main():
    if IS_DAILY:
        data_train, data_test = load_data_daily()
    else:
        data_train, data_test = load_data()
    best_ind, rule_generator = train(data_train)
    fortune = test(data_test, best_ind, rule_generator)
    print("Final fortune:", fortune)


if __name__ == "__main__":
    main()
