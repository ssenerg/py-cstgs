from argparse import ArgumentParser
from python import Triangles
from pathlib import Path
import polars as pl


if __name__ == "__main__":
    parser = ArgumentParser(
        description="Counting and Sampling Triangles from a Graph Stream"
    )
    parser.add_argument(
        "-d",
        "--data-dir",
        type=str,
        help="Path to the data directory",
        default="data",
    )
    parser.add_argument(
        "-p", "--processors", type=int, help="Number of processors to use", default=12
    )
    parser.add_argument(
        "-e",
        "--edge-sampling-prob",
        type=float,
        help="Edge sampling probability",
        default=0.568,
    )
    parser.add_argument(
        "-w",
        "--wedge-sampling-prob",
        type=float,
        help="Wedge sampling probability",
        default=0.8,
    )
    args = parser.parse_args()
    res, unknown_res = Triangles(Path(args.data_dir)).run(
        args.processors, args.edge_sampling_prob, args.wedge_sampling_prob
    )
    pl.Config.set_tbl_rows(-1)
    print(
        "\n\033[1m::All Results::\033[0m\n\n",
        res,
        "\n\n\033[1m::Known Results::\033[0m\n\n",
        unknown_res,
    )
