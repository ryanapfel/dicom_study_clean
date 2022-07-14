import pandas as pd
import os
import simplejson as json


class InsertOutput:
    def __init__(
        self,
        input,
        input_directory,
        identifier_column="Subject ID",
        json_file_name="study.json",
    ):
        self.input_path = input
        self.identifier_column = identifier_column
        self.input_directory = input_directory
        self.json_file_name = json_file_name

    def _read_excel(self):
        self.df = pd.read_excel(self.input_path)
        self.cols = list(self.df.columns)

        if self.identifier_column not in self.cols:
            raise ValueError(
                f"{self.identifier_column} not in input file. Must specify subject id column"
            )

    def _to_dict(self):
        self.df.set_index(self.identifier_column, inplace=True)
        self.dict = self.df.to_dict(orient="index")
        self.cols.remove(self.identifier_column)

    def _check_dir_exists(self, id: str):
        temp_path = os.path.join(self.input_directory, id)
        os.makedirs(temp_path, exist_ok=True)

        json_file_path = os.path.join(temp_path, self.json_file_name)

        if not os.path.isfile(json_file_path):
            with open(json_file_path, "w+") as f:
                json.dump({}, f, indent=2)

        return json_file_path

    def run(self):
        self._read_excel()
        self._to_dict()
        for subject_id, values in self.dict.items():
            path = self._check_dir_exists(subject_id)
            with open(path, "r", errors="ignore") as f:
                obj = json.load(f)
                obj["adjudicated"] = values

            with open(path, "w") as f:
                json.dump(
                    obj, f, indent=4, sort_keys=True, default=str, ignore_nan=True
                )
