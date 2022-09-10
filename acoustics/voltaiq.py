'''Functions specific to voltaiq_studio'''

import pandas as pd
from typing import List

import voltaiq_studio as vs
from voltaiq_studio.test_record.test_record import TestRecord


def filter_by_keyword(dataset: List[TestRecord],
                      keyword: str) -> List[TestRecord]:
    """Filters datasets by keyword in cell/experiment name.

    Args:
        dataset (List[TestRecord]): Results from vs.get_test_records()
        keyword (str): The keyword to filter on.
    
    Returns:
        List[TestRecord]: Filtered TestRecords
    """
    return [data for data in dataset if(keyword in data.name)]


def load_data_by_experiment(experiment: TestRecord,
                            trace_keys: list) -> pd.DataFrame:
    """Loads in experiment as pandas dataframe.
    
    Args:
        experiment (TestRecord): Experiment data
        trace_keys (list): Data features to be loaded from dataset
        
    Returns:
        pd.DataFrame: Experiment time-series.
    """

    reader = experiment.make_time_series_reader()

    for trace_key in trace_keys:
        reader.add_trace_keys(trace_key)

    df = reader.read_pandas()
    df.set_index(trace_keys[0], inplace=True)

    return df

def load_from_vs():
    """Loads all datasets available.

    Returns:
        list[TestRecord]: All available datasets.
    """
    return vs.get_test_records()