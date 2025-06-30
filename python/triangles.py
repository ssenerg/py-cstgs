from concurrent.futures import ProcessPoolExecutor, as_completed
from .configs import RootConfig, DataConfig
from cstgs import number_of_triangles
from typing import List, Tuple
from datetime import datetime
from pathlib import Path
from sys import exit
import polars as pl
import re


class Pipe:
    def __init__(self, data_dir: Path) -> None:
        try:
            self.__data_dir = data_dir
            self.__root_config = RootConfig.load(data_dir)
            self.__triangles: List[Triangles] = [
                Triangles(dataset_dir) for dataset_dir in self.__root_config.folders
            ]
            self.__stats: pl.DataFrame = None
            self.__unknown_stats: pl.DataFrame = None
            self.__is_ran = False
        except KeyboardInterrupt:
            print("Process interrupted, shutting down...")
            exit(1)
        except Exception as e:
            raise e
            print(f"Error occurred: {e}")
            exit(1)

    def stats(self) -> Tuple[pl.DataFrame, pl.DataFrame]:
        if not self.__is_ran:
            return self.run()
        return self.__stats, self.__unknown_stats
            
    def run(self, processors: int, edge_sampling_prob: float, wedge_sampling_prob: float) -> Tuple[pl.DataFrame, pl.DataFrame]:
        records: pl.DataFrame = None
        try:
            with ProcessPoolExecutor() as executor:
                futures = [
                    executor.submit(
                        triangle.run, processors, edge_sampling_prob, wedge_sampling_prob
                    ) for triangle in self.__triangles
                ]
                for future in as_completed(futures):
                    try:
                        recs: pl.DataFrame = future.result()
                        if records is None:
                            records = recs
                        else:
                            records = pl.concat([records, recs], how="vertical")
                    except Exception as e:
                        print(f"Error occurred: {e}")
                        exit(1)
        except KeyboardInterrupt:
            print("Process interrupted, shutting down...")
            exit(1)
        self.__is_ran = True
        self.__stats = records.sort("process_took_", descending=False).drop("process_took_")
        self.__unknown_stats = self.__stats.filter(pl.col("actual_triangles").is_not_null())
        self.__unknown_stats.write_csv(self.__data_dir / "known_results.csv")
        self.__stats.drop_in_place("actual_triangles")
        self.__stats.write_csv(self.__data_dir / "results.csv")
        return self.__stats, self.__unknown_stats

    
class Triangles:
    def __init__(self, dataset_dir: Path) -> None:
        try:
            self.data_config: DataConfig = DataConfig.load(dataset_dir)
            self.preprocess()
        except KeyboardInterrupt:
            print("Process interrupted, shutting down...")
            exit(1)
        except Exception as e:
            raise e
            print(f"Error occurred: {e}")
            exit(1)

    def preprocess(self) -> None:
        re_ignore = re.compile(self.data_config.format.regex_ignore)
        re_find = re.compile(self.data_config.format.regex_find)
        file_paths = [file_path for file_path in self.data_config.folders.raw.glob(f"*{self.data_config.format.extensions}")]
        ignore_first_match = self.data_config.format.skip_first_not_ignore
        try:
            with ProcessPoolExecutor() as executor:
                futures = [
                    executor.submit(self._preprocess, file_path, re_ignore, re_find, ignore_first_match) for file_path in file_paths
                ]
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        raise e
                        print(f"Error occurred: {e}")
                        exit(1)
        except KeyboardInterrupt:
            print("Process interrupted, shutting down...")
            exit(1)

    def _preprocess(self, file_path: Path, re_ignore: re.Pattern, re_find: re.Pattern, ignore_first_match: bool) -> None:
            proc_file_name = ".".join(file_path.name.split(".")[:-1]) + ".tsv"
            proc_path = self.data_config.folders.processed / proc_file_name
            with open(proc_path, 'w') as proc_file:
                with open(file_path, 'r') as file:
                    first_match = not ignore_first_match
                    for i, line in enumerate(file.readlines()):
                        if re_ignore.fullmatch(line):
                            continue
                        if not first_match:
                            first_match = True
                            continue
                        match = re_find.fullmatch(line)
                        if not match:
                            proc_file.close()
                            raise ValueError(f"{self.data_config.name}::{file_path.name} does not match on line {i+1}.")
                        proc_file.write(f"{match.group(1)}\t{match.group(2)}\n")

    def _format_time(self, microseconds: int) -> str:
        if microseconds < 1000:
            return f"{microseconds}μs"
        elif microseconds < 1000000:
            return f"{microseconds / 1000:.2f}ms"
        elif microseconds < 60000000:
            return f"{microseconds / 1000000:.2f}s"
        else:
            return f"{microseconds / 60000000:.2f}m"

    def run(self, processors: int, edge_sampling_prob: float, wedge_sampling_prob: float) -> pl.DataFrame:
        file_paths = [file_path for file_path in self.data_config.folders.processed.glob("*.tsv")]
        all_index_data = []
        all_triangles = []
        all_durations = []
        actual_triangles = []
        try:
            with ProcessPoolExecutor() as executor:
                futures = [
                    executor.submit(self._run, file_path, processors, edge_sampling_prob, wedge_sampling_prob) for file_path in file_paths
                ]
                for future in as_completed(futures):
                    try:
                        res = future.result()
                        all_index_data.append(f"{self.data_config.name}::{res[0].name}")
                        all_triangles.append(res[1])
                        all_durations.append(res[2])
                        file_name = ".".join(res[0].name.split(".")[:-1])
                        if file_name in self.data_config.known_triangle_counts:
                            actual_triangles.append(self.data_config.known_triangle_counts[file_name])
                        else:
                            actual_triangles.append(None)
                    except Exception as e:
                        raise e
                        print(f"Error occurred: {e}")
                        exit(1)
        except KeyboardInterrupt:
            print("Process interrupted, shutting down...")
            exit(1)
        records = pl.DataFrame({
            "dataset": all_index_data,
            "triangles": all_triangles,
            "actual_triangles": actual_triangles,
            "process_took_": all_durations
        }).with_columns(
            pl.col("process_took_").map_elements(self._format_time, return_dtype=pl.Utf8).alias("process_took")
        ).sort("process_took_", descending=False)
        records.drop("process_took_").drop("actual_triangles").write_csv(self.data_config.folders.statistics / "results.csv")
        known_records = records.filter(pl.col("actual_triangles").is_not_null())
        known_records.drop("process_took_").write_csv(self.data_config.folders.statistics / "known_results.csv")
        return records

    def _run(self, file_path: Path, processors: int, edge_sampling_prob: float, wedge_sampling_prob: float) -> Tuple[Path, int, float]:
        now = datetime.now()
        res = number_of_triangles(str(file_path), processors, edge_sampling_prob, wedge_sampling_prob)
        elapsed = (datetime.now() - now).total_seconds() * 1000000
        return file_path, res, elapsed
