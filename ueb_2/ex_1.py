import pandas as pd

from pathlib import Path

from itertools import permutations


def load_distance_matrix(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, index_col="index", header=0)
    return df


def load_transport_matrix(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, index_col="index", header=0)
    return df


def get_column_permutations(transport_matrix: pd.DataFrame):
    columns = transport_matrix.columns.tolist()
    all_permutations = permutations(columns, len(columns))

    return all_permutations


def calculate_transport_cost(
    transport_matrix: pd.DataFrame, distance_matrix: pd.DataFrame
) -> float:
    if transport_matrix.shape != distance_matrix.shape:
        raise ValueError

    rows, _ = transport_matrix.shape
    total = 0.0
    for i, j in permutations(range(rows), 2):
        local_value = transport_matrix.iloc[i, j] * distance_matrix.iloc[i, j]
        total += local_value

    return total


def main():
    distance_matrix = load_distance_matrix(Path(__file__).parent / "dm.csv")
    transport_matrix = load_transport_matrix(Path(__file__).parent / "tm.csv")

    permutations = get_column_permutations(transport_matrix)

    for perm in permutations:
        local_tm = transport_matrix.reindex(columns=perm, index=perm)

        v = calculate_transport_cost(local_tm, distance_matrix)

        print(f"{''.join(perm)} -> {v}")


if __name__ == "__main__":
    main()
