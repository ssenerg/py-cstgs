from concurrent.futures import ProcessPoolExecutor, as_completed
from .configs import RootConfig, DataConfig
from cstgs import number_of_triangles
from typing import List, Tuple
from pathlib import Path
from sys import exit
import polars as pl
import re


class Pipe:
    def __init__(self, data_dir: Path) -> None:
        try:
            self.__root_config = RootConfig.load(data_dir)
            self.__triangles: List[Triangles] = [
                Triangles(dataset_dir) for dataset_dir in self.__root_config.folders
            ]
            self.__stats: pl.DataFrame = pl.DataFrame({
                "index": pl.Series(
                    [], 
                    dtype=pl.Struct({"folder_name": pl.String, "file_name": pl.String})
                ),
                "processing_duration": pl.Series([], dtype=pl.Float64)
            })
            self.__is_ran = False
        except KeyboardInterrupt:
            print("Process interrupted, shutting down...")
            exit(1)
        except Exception as e:
            raise e
            print(f"Error occurred: {e}")
            exit(1)

    def stats(self) -> pl.DataFrame:
        if not self.__is_ran:
            return self.run()
        return self.__stats
            
    def run(self, processors: int, edge_sampling_prob: float, wedge_sampling_prob: float) -> pl.DataFrame:
        all_index_data = []
        all_durations = []
        try:
            with ProcessPoolExecutor() as executor:
                futures = [
                    executor.submit(
                        triangle.run, processors, edge_sampling_prob, wedge_sampling_prob
                    ) for triangle in self.__triangles
                ]
                for future in as_completed(futures):
                    try:
                        dataset_name, records = future.result()
                        all_index_data.extend([{"dataset": dataset_name, "record_name": record} for record in records.keys()])
                        all_durations.extend(records.values())
                    except Exception as e:
                        print(f"Error occurred: {e}")
                        exit(1)
        except KeyboardInterrupt:
            print("Process interrupted, shutting down...")
            exit(1)
        self.__is_ran = True
        self.__stats = pl.DataFrame({
            "index": pl.Series(all_index_data, dtype=pl.Struct({"dataset": pl.String, "record_name": pl.String})),
            "processing_duration": pl.Series(all_durations, dtype=pl.Float64)
        })
        return self.__stats

    
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

    def run(self, processors: int, edge_sampling_prob: float, wedge_sampling_prob: float) -> Tuple[str, dict[str, int]]:
        file_paths = [file_path for file_path in self.data_config.folders.processed.glob("*.tsv")]
        reses: dict[str, int] = {}
        try:
            with ProcessPoolExecutor() as executor:
                futures = [
                    executor.submit(self._run, file_path, processors, edge_sampling_prob, wedge_sampling_prob) for file_path in file_paths
                ]
                for future in as_completed(futures):
                    try:
                        res = future.result()
                        reses[res[0].name] = res[1]
                    except Exception as e:
                        raise e
                        print(f"Error occurred: {e}")
                        exit(1)
        except KeyboardInterrupt:
            print("Process interrupted, shutting down...")
            exit(1)
        return self.data_config.name, reses

    def _run(self, file_path: Path, processors: int, edge_sampling_prob: float, wedge_sampling_prob: float) -> Tuple[Path, int]:
        return file_path, number_of_triangles(str(file_path), processors, edge_sampling_prob, wedge_sampling_prob)