import os
import pandas as pd


def get_datasets(path):
    res = []
    for f in os.listdir(path):
        if not f.endswith(".nc"):
            continue
        entry = parse_dataset_name(f)
        entry["path"] = os.path.join(path, f)
        res.append(entry)
    return pd.DataFrame.from_records(res).set_index("path")


def parse_dataset_name(f):
    parts = f.replace(".nc", "").split("_")
    variable, period, model, scenario, init_params, timespan = parts[:6]
    timespan_from, timespan_to = timespan.split("-")
    entry = {"variable": variable,
             "frequency": period,
             "model": model,
             "scenario": scenario,
             "init_params": init_params,
             "timespan": f'{timespan_from[1:5]}-{timespan_to[:4]}'}
    return entry


def get_model_weights(path):
    res = []
    for f in os.listdir(path):
        if not f.endswith(".tsv"):
            continue
        entry = {}
        entry["path"] = os.path.join(path, f)
        entry["name"] = f[:-4]
        res.append(entry)
    return pd.DataFrame.from_records(res).set_index("path")
