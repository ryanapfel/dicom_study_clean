import os
from dcmstudyclean.NamingConvention import NamingConventionBase
from dcmstudyclean.StudyImage import StudyImage
import json
import logging
import traceback


class RecordStudyDataPipeline:
    def __init__(self, input_dir):
        self.input_dir = input_dir
        self.allStudies = []

    def ETL(self):
        for dirLike in os.listdir(self.input_dir):

            subject_name = dirLike
            cur_path = os.path.join(self.input_dir, subject_name)

            if os.path.isdir(cur_path):

                try:
                    helper = RecordStudyDataHelper(cur_path)
                    helper.extract()
                    dict = helper.saveFile()
                    self.allStudies.append(dict)
                except Exception:
                    logging.warn(
                        f"Error when writing json for {subject_name} at {cur_path}"
                    )
                    logging.debug(traceback.format_exc())
        self.cleanUp()

    def cleanUp(self, filename: str = "study.json"):
        path = os.path.join(self.input_dir, filename)
        with open(path, "w") as fp:
            json.dump(self.allStudies, fp, indent=4)

        logging.info(f"Completed writing all files for study")
        logging.info(f" Database stored at {path}")


class RecordStudyDataHelper:
    def __init__(self, source_directory):
        self.source_directory = source_directory
        self.convention = NamingConventionBase()
        self.modalities = set()
        self.studyname = ""
        self.site = ""
        self.subject = ""
        self.timepoints = set()

    def extract(self):
        for root, dirs, files in os.walk(self.source_directory):
            for name in files:
                path = os.path.join(root, name)
                if os.path.splitext(path)[1] == ".dcm":
                    image = StudyImage(filepath=path, nameConvention=self.convention)
                    obj = image.studyInfo
                    self.studyname = obj["study"]
                    self.site = obj["site_id"]
                    self.subject = obj["subject_id"]
                    self.timepoints.add(obj["timepoint"])
                    self.modalities.add(image.modality)

    def saveFile(self, filename: str = "study.json"):
        dict = {
            "Study": self.studyname,
            "SiteID": self.site,
            "SubjectID": self.subject,
            "Timepoints": list(self.timepoints),
            "Modalities": list(self.modalities),
            "Path": self.source_directory,
        }
        filepath = os.path.join(self.source_directory, filename)

        with open(filepath, "w") as fp:
            json.dump(dict, fp, indent=4)

        logging.info(f"Saved study info for {self.site} {self.subject}")

        return dict
