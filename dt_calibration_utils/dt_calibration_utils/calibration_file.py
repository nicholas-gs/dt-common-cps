import os
import time
import yaml

from os.path import expanduser


__all__ = [
    'save_calibration',
    'read_calibration'
]


HOME_DIR = expanduser("~")
BASE_DIR = os.path.join(HOME_DIR, ".dt-cps/data/calibrations")


def save_calibration(rel_file_path, data) -> str:
    """Save data into YAML file
    Returns the full path to the written YAML file.
    """
    data["calibration_time"] = time.strftime("%Y-%m-%d-%H-%M-%S")
    full_fp = os.path.join(BASE_DIR, rel_file_path)
    try:
        os.makedirs(os.path.dirname(full_fp))
    except OSError as _:
        pass
    with open(full_fp, 'w') as outfile:
        outfile.write(yaml.safe_dump(data, default_flow_style=False))
    return full_fp

def read_calibration(rel_file_path: str, vars=None):
    full_fp = os.path.join(BASE_DIR, rel_file_path)
    if not os.path.isfile(full_fp):
        return None, full_fp, None
    else:
        with open(full_fp, 'r') as in_file:
            try:
                data = yaml.safe_load(in_file)
                if vars is None:
                    return data, full_fp, None
                else:
                    return {var : data.get(var) for var in vars}, full_fp, data.get("calibration_time")
            except yaml.YAMLError as _:
                return None, full_fp, None
