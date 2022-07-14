import re


class NamingConventionBase:
    def __init__(
        self,
        sitePad: int = 3,
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
        self.studynames = set()
        self.sites = set()
        self.subjects = set()
        self.timepoints = set()

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
                returnDict["site_id"] = splitItem
            elif idx == 2 and self.__is_int(splitItem):
                returnDict["subject_id"] = splitItem
            elif idx == 3:
                returnDict["timepoint"] = splitItem.capitalize()
            elif idx > 3 and "other" not in returnDict:
                returnDict["other"] = [splitItem]
            elif idx > 3:
                returnDict["other"].append(splitItem)

        return returnDict

    def _get_site_subject(self, inputDict: dict):

        if "site_id" in inputDict and len(inputDict["site_id"]) <= self.sitePad:
            site_str = str(inputDict["site_id"]).zfill(self.sitePad)
        elif "site_id" in inputDict and len(inputDict["site_id"]) > self.sitePad:
            site_str = str(inputDict["site_id"])[-self.sitePad :]
        else:
            site_str = "NA"

        if (
            "subject_id" in inputDict
            and len(inputDict["subject_id"]) <= self.subjectPad
        ):
            subject_str = str(inputDict["subject_id"]).zfill(self.subjectPad)
        elif (
            "subject_id" in inputDict and len(inputDict["subject_id"]) > self.subjectPad
        ):
            subject_str = str(inputDict["subject_id"])[-self.subjectPad :]
        else:
            subject_str = "NA"

        return site_str, subject_str

    def standardize(self, inputDict: dict, keepTrackNames: bool = True) -> str:
        study = inputDict["study"] if "study" in inputDict else "UnresolvedStudy"

        site_str, subject_str = self._get_site_subject(inputDict)

        timepoint_str = inputDict["timepoint"] if "timepoint" in inputDict else "None"

        if keepTrackNames:
            self.studynames.add(study)
            self.sites.add(site_str)
            self.subjects.add(subject_str)
            self.timepoints.add(timepoint_str)

        return f"{study}{self.studySplit}{site_str}{self.siteSplit}{subject_str}{self.timepointSplit}{timepoint_str}"

    def jointStudyId(self, inputDict: dict):

        site_str, subject_str = self._get_site_subject(inputDict)

        return f"{site_str}{self.siteSplit}{subject_str}"
