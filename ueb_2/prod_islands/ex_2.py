import pandas as pd

from pathlib import Path
from rich.pretty import pprint


def load_matrix(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, header=0, index_col="index")

    return df


def calculate_binary_values(mat: pd.DataFrame) -> pd.Series:
    values = []
    for row in mat.itertuples():
        bin_value = "".join([str(x) for x in row[1:]])
        values.append(int(bin_value, 2))

    return pd.Series(values)


def calculate_binary_col_values(mat: pd.DataFrame) -> pd.Series:
    values = []
    for col in mat.columns:
        bin_value = "".join([str(x) for x in mat[col]])
        values.append(int(bin_value, 2))

    return pd.Series(values, index=mat.columns)


def reorder_by_row(mat: pd.DataFrame) -> pd.DataFrame:
    row_bin = calculate_binary_values(mat)
    mat.loc[:, "bin"] = row_bin.values

    return mat.sort_values("bin", ascending=False).drop(columns=["bin"])


def reorder_by_column(mat: pd.DataFrame) -> pd.DataFrame:
    col_bin = calculate_binary_col_values(mat)
    col_bin = col_bin.sort_values(ascending=False)

    return mat.reindex(columns=col_bin.index.tolist())


def is_ordered(mat: pd.DataFrame, prev: pd.DataFrame | None) -> bool:
    if prev is None:
        return False
    else:
        return prev.equals(mat)


def main():
    mat = load_matrix(Path(__file__).parent / "mat.csv")

    prev = None
    ordered = False
    while not ordered:
        prev = mat.copy()

        mat = reorder_by_row(mat)
        mat = reorder_by_column(mat)

        ordered = is_ordered(mat, prev)

    return mat


if __name__ == "__main__":
    mat = main()

    pprint(mat)
