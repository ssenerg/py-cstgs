from pydantic import BaseModel, field_validator, ValidationInfo, model_validator
from re import compile, error
from typing import List, Dict
from pathlib import Path
from os import makedirs
from json import load


class RootConfig(BaseModel):
    folders: List[Path]

    @field_validator("folders", mode="before")
    @classmethod
    def validate_folders(cls, folders: List[str], info: ValidationInfo) -> List[Path]:
        if not info.context or "data_dir" not in info.context:
            raise ValueError("data_dir must be provided in the context")
        data_dir = info.context["data_dir"]
        result = []
        for path_str in folders:
            dataset_dir = data_dir / path_str
            if not dataset_dir.exists():
                raise ValueError(f'Dataset folder not found: "{dataset_dir}"')
            result.append(dataset_dir)
        return result

    @classmethod
    def load(cls, data_dir: Path) -> "RootConfig":
        if not data_dir.exists():
            raise ValueError(f'Data folder not found: "{data_dir}"')
        file = data_dir / ".root.json"
        if not file.exists():
            raise FileNotFoundError(f'Data config file not found: "{str(file)}"')

        with open(file, "r") as f:
            data = load(f)

        return cls.model_validate(data, context={"data_dir": data_dir})


class DataConfigFolders(BaseModel):
    raw: Path
    processed: Path
    statistics: Path

    @field_validator("raw", "processed", "statistics", mode="before")
    @classmethod
    def validate_paths(cls, path: str, info: ValidationInfo) -> Path:
        if not path:
            raise ValueError(f"Path for {info.field_name} cannot be empty")
        if not info.context or "dataset_dir" not in info.context:
            raise ValueError("dataset_dir must be provided in the context")
        dataset_dir = info.context["dataset_dir"]
        full_path = dataset_dir / path
        return full_path

    @field_validator("raw")
    @classmethod
    def validate_raw(cls, raw_path: Path, info: ValidationInfo) -> Path:
        if not raw_path.exists():
            raise ValueError(f'Raw folder not found: "{raw_path}"')
        if not info.context or "extensions" not in info.context:
            raise ValueError("extensions must be provided in the context")
        extension = info.context["extensions"]
        if not any(raw_path.glob(f"*{extension}")):
            raise ValueError(
                f"No files with extension '{extension}' found in raw folder: \"{raw_path}\""
            )
        return raw_path

    @field_validator("processed")
    @classmethod
    def validate_processed(cls, processed_path: Path) -> Path:
        if not processed_path.exists():
            makedirs(processed_path)
        return processed_path

    @field_validator("statistics")
    @classmethod
    def validate_statistics(cls, statistics_path: Path) -> Path:
        if not statistics_path.exists():
            makedirs(statistics_path)
        return statistics_path


class DataConfigFormat(BaseModel):
    extensions: str
    regex_ignore: str
    regex_find: str
    skip_first_not_ignore: bool

    @field_validator("extensions")
    @classmethod
    def validate_extensions(cls, extensions: str) -> str:
        if not extensions.startswith("."):
            raise ValueError("Extension must start with a dot (.)")
        if "." in extensions[1:] or " " in extensions:
            raise ValueError("Extension must not contain additional dots or whitespace")
        if not extensions[1:].isascii():
            raise ValueError(
                "Extension must contain only ASCII characters after the dot"
            )
        return extensions

    @field_validator("regex_ignore")
    @classmethod
    def validate_regex_ignore(cls, regex_ignore: str) -> str:
        try:
            compile(regex_ignore)
        except error as e:
            raise ValueError(f"Invalid regex_ignore pattern: {str(e)}")
        return regex_ignore

    @field_validator("regex_find")
    @classmethod
    def validate_regex_find(cls, regex_find: str) -> str:
        try:
            pattern = compile(regex_find)
            if pattern.groups != 2:
                raise ValueError("regex_find must contain two capturing groups")
        except error as e:
            raise ValueError(f"Invalid regex_find pattern: {str(e)}")
        return regex_find


class DataConfig(BaseModel):
    name: str
    folders: DataConfigFolders
    format: DataConfigFormat
    known_triangle_counts: Dict[str, int]

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        if not name:
            raise ValueError("Name cannot be empty")
        return name

    @model_validator(mode="after")
    def validate_known_triangle_counts(self) -> "DataConfig":
        raw_folder = self.folders.raw
        extension = self.format.extensions

        for dataset_name, count in self.known_triangle_counts.items():
            if count < 0:
                raise ValueError(
                    f"Triangle count for {dataset_name} must be non-negative"
                )

            dataset_file = raw_folder / f"{dataset_name}{extension}"
            if not dataset_file.exists():
                raise ValueError(
                    f'Dataset file not found for {dataset_name}: "{dataset_file}"'
                )
        return self

    @classmethod
    def load(cls, dataset_dir: Path) -> "DataConfig":
        if not dataset_dir.exists():
            raise ValueError(f'Dataset folder not found: "{dataset_dir}"')
        file = dataset_dir / ".data.json"
        if not file.exists():
            raise FileNotFoundError(f'Dataset config file not found: "{str(file)}"')

        with open(file, "r") as f:
            data = load(f)

        context = {
            "dataset_dir": dataset_dir,
            "extensions": data.get("format", {}).get("extensions", ""),
        }
        return cls.model_validate(data, context=context)
