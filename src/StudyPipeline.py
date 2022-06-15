import imp
from src.NamingConvention import NamingConventionBase
from src.StudyImage import StudyImage
import logging
import traceback
import os
from tqdm import tqdm


class StudyPipeline:
    def __init__(
        self,
        sourcepath: str,
        studyDefinition: dict,
        exportDestination: str,
        batchsize: int,
        **kwargs,
    ):
        self.sourcepath = sourcepath
        self.studyDefinition = studyDefinition
        self.exportDestination = exportDestination
        self.namingConvention = NamingConventionBase(**kwargs)
        self.batch = batchsize

        self.pipelineData = []
        self.images = {}

    def ETL(self, *args, **kwargs):
        #

        for batch in self._walk_dirs(self.batch):
            try:
                studyimages = self.extract(batch)
                updatedImages = self.transform(studyimages)
                self.load(updatedImages)
                logging.info(f"Proccessed {self.batch} images")
            except Exception as e:
                logging.debug(traceback.format_exc())
                logging.warning(e)

    def __write_files_timepoint(self, imageInstance):
        """
        Writes dicom to a master study folder by subject id seperated by timepoin
        """
        exportPath = self.exportDestination
        jointName = imageInstance.nameConvention.jointStudyId(imageInstance.studyInfo)

        studyPath = os.path.join(exportPath, jointName)

        if not os.path.isdir(studyPath):
            os.mkdir(studyPath)

        if "timepoint" in imageInstance.studyInfo:
            timepoint = imageInstance.studyInfo["timepoint"]
            #  add in timepoint
            studyPath = os.path.join(studyPath, timepoint)

            if not os.path.isdir(studyPath):
                os.mkdir(studyPath)

        name = f"{imageInstance.instanceUID}.dcm"
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
