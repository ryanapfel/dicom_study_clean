import pandas as pd
from datetime import datetime
import os
import click
import logging

from dcmstudyclean.StudyPipeline import StudyPipeline
from dcmstudyclean.RecordStudyInfo import RecordStudyDataPipeline
from dcmstudyclean.Archive import archvieDirectorySubFolders
from dcmstudyclean.InsertOutput import InsertOutput
import warnings

warnings.filterwarnings("ignore")
LEVEL = logging.DEBUG
logging.basicConfig(level=LEVEL)


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-i",
    "--input_path",
    help="Path to directory that contains all of the raw dicom files",
    required=True,
)
@click.option(
    "-o",
    "--output_path",
    help="Directory to output cleaned files to",
    required=True,
)
@click.option(
    "--subject_pad",
    help="Padding to add before subject # EX: pad = 3 (3 -> 003)",
    required=True,
    type=(int),
)
@click.option(
    "--site_pad",
    help="Padding to add before site #. EX: pad = 3... 3 -> 003",
    required=True,
    type=(int),
)
# @click.option("--studySplit", help="delimiter between study name and site")
# @click.option("--siteSplit", help="delimitter between site and subject")
# @click.option("--timepointSplit", help="delimitter between study and timepoint")
@click.option(
    "--batch_size",
    help="number of images to proccess at once. Larger if more ram available",
    default=2500,
    type=(int),
)
def clean(
    input_path,
    output_path,
    subject_pad,
    site_pad,
    batch_size,
):

    print(type(site_pad))
    logging.info(f"Exporting from {input_path}")
    logging.info(f"Exporting to {output_path}")

    sp = StudyPipeline(
        sourcepath=input_path,
        exportDestination=output_path,
        batchsize=batch_size,
        subjectPad=subject_pad,
        sitePad=site_pad,
    )

    sp.ETL()


@cli.command()
@click.option(
    "-i",
    "--input_path",
    help="Path to directory that contains all of cleaned study files",
    required=True,
)
def extract(input_path):
    rsdp = RecordStudyDataPipeline(input_path)
    rsdp.ETL()


@cli.command()
@click.option(
    "-i",
    "--input_path",
    help="Path to directory that contains all of the cleaned directories",
    required=True,
)
@click.option(
    "-o",
    "--output_path",
    help="Directory to output cleaned zipped files to",
    required=True,
)
def archive(input_path, output_path):
    archvieDirectorySubFolders(input_path, output_path)


@cli.command()
@click.option(
    "-i",
    "--input_path",
    help="Path to directory that contains all of the cleaned directories",
    required=True,
)
@click.option(
    "-e",
    "--excel_path",
    help="Path to excel file containing the output to insert",
    required=True,
)
@click.option(
    "--col",
    help="Column in scpreadsheet that contains the subject ID. format in spreadsheet must match format in directory folder",
    default="Subject ID",
)
def addOutput(input_path, excel_path, col):
    IO = InsertOutput(excel_path, input_directory=input_path, identifier_column=col)
    IO.run()


if __name__ == "__main__":
    cli()
