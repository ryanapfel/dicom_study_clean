from dcmstudyclean.NamingConvention import NamingConventionBase
from datetime import timedelta


class StudyImageAbstract:
    def __init__(self, df):
        self.df = df
        self.results = {}
        self.indexName = "Procedure"
        self.unresolvedName = "Unresolved"
        self.baselineName = "Baseline"
        self.unscheduledName = "Unscheduled"
        self.otherName = "Other"
        self.postName = "Post"
        self.acceptedModalities = ["CT", "MR"]
        self.postThresholdHRS = 48
        # self.convention = NamingConvention

    def retrieve(self):
        self.indexExists, self.indexDate = self.getIndex()
        self.getAllTimepoints()
        return self.df

    def getIndex(self, maxDays=1):
        if "XA" not in self.df["modality"].unique():
            return False, None

        min = self.df.loc[self.df["modality"] == "XA", "date"].min()
        deltaMax = min + timedelta(days=maxDays)

        self.df.loc[
            (self.df["modality"] == "XA") & (self.df["date"] < deltaMax), "timepoint"
        ] = self.indexName

        return True, min

    def baseline(self):
        self.df.loc[
            (
                (self.df["modality"].isin(self.acceptedModalities))
                & (self.df["date"] < self.indexDate)
            ),
            "timepoint",
        ] = self.baselineName

    def post(self):

        postDeltaMax = self.indexDate + timedelta(hours=self.postThresholdHRS)
        self.df.loc[
            (
                (self.df["modality"].isin(self.acceptedModalities))
                & (self.df["date"] > self.indexDate)
                & (self.df["date"] < postDeltaMax)
            ),
            "timepoint",
        ] = self.baselineName

        self.df.loc[
            (
                (self.df["modality"].isin(self.acceptedModalities))
                & (self.df["date"] > self.indexDate)
                & (self.df["date"] > postDeltaMax)
            ),
            "timepoint",
        ] = self.unscheduledName

    def cleanup(self):
        self.df.loc[self.df["timepoint"] == None, "timepoint"] = self.otherName

    def getAllTimepoints(self):
        if not self.indexExists:
            self.df.loc[:, "timepoint"] = self.unresolvedName
            return True

        if not self.indexDate:
            raise ValueError("Index Date Not Set or not valid")

        self.baseline()
        self.post()
        self.cleanup()

        return True
