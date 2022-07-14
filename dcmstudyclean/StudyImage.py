from dcmstudyclean.NamingConvention import NamingConventionBase
from pydicom import dcmread
import pandas as pd
from datetime import datetime as dtt


class StudyImage:
    def __init__(
        self,
        filepath: str,
        nameConvention: NamingConventionBase,
        dateRequired: bool = False,
        loglevel: str = "Debug",
    ):
        self.filepath = filepath
        self.study = None
        self.siteId = None
        self.subjectId = None
        self.timepoint = None
        self.index = False
        self.dateRequired = dateRequired
        self.loglevel = loglevel
        self.nameConvention = nameConvention
        self.retrieve()

    def retrieve(self):

        self.dataset = dcmread(self.filepath, force=True)

        # self.seriesUID = self.get("SeriesInstanceUID")
        # self.studyUID = self.get("StudyInstanceUID")
        # self.instanceUID = self.get("SOPInstanceUID")
        self.modality = self.get("Modality")
        # self.date = self.getDateTime()

        self.name = self.get("PatientName")
        self.studyInfo = self.nameConvention.extract(self.name)

    def __repr__(self):
        return f"{self.study}-{self.siteId}_{self.subjectId}-{self.timepoint}"

    def writeMeta(self, key, value):
        try:
            self.dataset[key].value = value
            self.retrieve(readFile=False)
            return True
        except Exception as e:
            return False

    def updateName(self):
        newName = self.nameConvention.standardize(self.studyInfo)
        self.dataset.PatientName = newName

    def dicom_time_to_datetime(self, t):
        if "." in t:
            return dtt.strptime(t, "%H%M%S.%f")
        else:
            return dtt.strptime(t, "%H%M%S")

    def dicom_date_to_datetime(self, d):
        return dtt.strptime(d, "%Y%m%d")

    def getDateTime(self):

        if ("StudyDate" not in self.dataset and "SeriesTime" not in self.dataset) and (
            "ContentDate" not in self.dataset and "ContentTime" not in self.dataset
        ):
            return None

        date = ""
        time = ""

        if "StudyDate" in self.dataset:
            date = self.dicom_date_to_datetime(self.get("StudyDate"))
        elif "ContentDate" in self.dataset:
            date = self.dicom_date_to_datetime(self.get("ContentDate"))

        if "SeriesTime" in self.dataset:
            time = self.dicom_time_to_datetime(self.get("SeriesTime"))
        elif "ContentTime" in self.dataset:
            time = self.dicom_time_to_datetime(self.get("ContentTime"))

        if time and date:
            return dtt.combine(date, time.time())
        elif date:
            return date
        else:
            raise ValueError("Not able to extact date and time")

    def get(self, key):
        if key not in self.dataset:
            raise ValueError(f"{key} not in DICOM data at {self.filepath}")

        return self.dataset[key].repval.replace("'", "")
