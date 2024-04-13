import pandas


def read_csv(file_path: str, index_col: str, column_defs: dict):
    if not file_path:
        return
    df = pandas.read_csv(file_path, dtype=column_defs)
    df.set_index(index_col, inplace=True)
    return df


def get_file_path(folder: str, file_name: str = None):
    return '/'.join([folder, file_name])