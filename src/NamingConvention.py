import imp
import re


class NamingConventionBase:
    def __init__(
        self,
        sitePad: int = 2,
        subjectPad: int = 3,
        studySplit="-",
        siteSplit="-",
        timepointSplit="-",
    ):
        self.sitePad = sitePad
        self.subjectPad = subjectPad
        self.studySplit = studySplit
        self.siteSplit = siteSplit
        self.timepointSplit = timepointSplit

    def __is_int(self, element: any) -> bool:
        try:
            int(element)
            return True
        except ValueError:
            return False

    def extract(self, name: str) -> dict:
        returnDict = {}
        split_data = re.split("[-_ ]", name)
        for idx, splitItem in enumerate(split_data):
            if idx == 0:
                returnDict["study"] = splitItem.capitalize()
            elif idx == 1 and self.__is_int(splitItem):
                returnDict["site_id"] = int(splitItem)
            elif idx == 2 and self.__is_int(splitItem):
                returnDict["subject_id"] = int(splitItem)
            elif idx == 3:
                returnDict["timepoint"] = splitItem.capitalize()
            elif idx > 3 and "other" not in returnDict:
                returnDict["other"] = [splitItem]
            elif idx > 3:
                returnDict["other"].append(splitItem)

        return returnDict

    def standardize(
        self,
        inputDict: dict,
    ) -> str:
        study = inputDict["study"] if "study" in inputDict else "UnresolvedStudy"

        site_str = (
            str(inputDict["site_id"]).zfill(self.sitePad)
            if "site_id" in inputDict
            else "0".zfill(self.sitePad)
        )
        subject_str = (
            str(inputDict["subject_id"]).zfill(self.subjectPad)
            if "subject_id" in inputDict
            else "0".zfill(self.subjectPad)
        )

        timepoint_str = inputDict["timepoint"] if "timepoint" in inputDict else ""

        return f"{study}{self.studySplit}{site_str}{self.siteSplit}{subject_str}{self.timepointSplit}{timepoint_str}"

    def jointStudyId(self, inputDict: dict):

        site_str = (
            str(inputDict["site_id"]).zfill(self.sitePad)
            if "site_id" in inputDict
            else "0".zfill(self.sitePad)
        )
        subject_str = (
            str(inputDict["subject_id"]).zfill(self.subjectPad)
            if "subject_id" in inputDict
            else "0".zfill(self.subjectPad)
        )

        return f"{site_str}{self.siteSplit}{subject_str}"
