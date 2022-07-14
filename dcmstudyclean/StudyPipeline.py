from dcmstudyclean.NamingConvention import NamingConventionBase
from dcmstudyclean.StudyImage import StudyImage
import logging
import traceback
import os
from tqdm import tqdm


class StudyPipeline:
    def __init__(
        self,
        sourcepath: str,
        exportDestination: str,
        batchsize: int,
        **kwargs,
    ):
        if not os.path.isdir(sourcepath):
            raise ValueError(f"{sourcepath} is not a valid source directory")

        if not os.path.isdir(exportDestination):
            raise ValueError(f"{exportDestination} is not a valid export directory")

        self.sourcepath = sourcepath
        # self.studyDefinition = studyDefinition
        self.exportDestination = exportDestination
        self.namingConvention = NamingConventionBase(**kwargs)
        self.batch = batchsize
        self.imProcessed = 0
        self.studiesProccessed = 0
        self.pipelineData = []
        self.images = {}

    def ETL(self, *args, **kwargs):
        for batch in self._walk_dirs(self.batch):
            try:
                studyimages = self.extract(batch)
                updatedImages = self.transform(studyimages)
                self.load(updatedImages)
                logging.info(f"Proccessed {len(list(batch))} images")
            except Exception as e:
                logging.debug(traceback.format_exc())
                logging.warning(e)

        self._cleanUp()

    def _cleanUp(self):
        logging.info(f"------FINISHED CLEANUP-------")
        logging.info(f"Images Proccessed: {self.imProcessed}")
        logging.info(f"Unique Studies Extracted: {self.studiesProccessed}")

        logging.info("Site Variations: ")
        print(self.namingConvention.sites)
        logging.info("Subject Variations: ")
        print(self.namingConvention.subjects)
        logging.info("Timepoint Variations: ")
        print(self.namingConvention.timepoints)
        logging.info("StudyName Variations: ")
        print(self.namingConvention.studynames)

    def __write_files_timepoint(self, imageInstance):
        """
        Writes dicom to a master study folder by subject id seperated by timepoin
        """
        exportPath = self.exportDestination
        jointName = imageInstance.nameConvention.jointStudyId(imageInstance.studyInfo)

        studyPath = os.path.join(exportPath, jointName)

        if not os.path.isdir(studyPath):
            os.mkdir(studyPath)
            self.studiesProccessed += 1

        if "timepoint" in imageInstance.studyInfo:
            timepoint = imageInstance.studyInfo["timepoint"]
            #  add in timepoint
            studyPath = os.path.join(studyPath, timepoint)

            if not os.path.isdir(studyPath):
                os.mkdir(studyPath)

        nFiles = len(os.listdir(studyPath))

        name = f"{nFiles + 1}.dcm"
        studyPath = os.path.join(studyPath, name)

        imageInstance.dataset.save_as(studyPath)

    def _walk_dirs(self, batch_size):
        """
        Walks a directory in batches instead of iteratively so that ram doesn't fill up
        """
        walk_dirs_generator = os.walk(self.sourcepath)
        for dirname, _, filenames in walk_dirs_generator:
            for i in range(0, len(filenames), batch_size):
                yield [
                    os.path.join(dirname, filename)
                    for filename in filenames[i : i + batch_size]
                ]

    def extract(self, files):
        objs = []
        for file in files:
            try:
                tmpStudyImage = StudyImage(file, self.namingConvention)
                objs.append(tmpStudyImage)
            except Exception as e:
                print(e)

        return objs

    def transform(self, items: list):
        for ithStudyImage in items:
            ithStudyImage.updateName()

        return items

    def load(self, items: list):
        for ithImage in items:
            self.__write_files_timepoint(ithImage)
            self.imProcessed += 1
