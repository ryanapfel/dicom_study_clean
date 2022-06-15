import pandas as pd
from datetime import datetime
import os
import click
import logging

from src.StudyPipeline import StudyPipeline

LEVEL = logging.INFO
logging.basicConfig(level=LEVEL)


"""
Returns dataframe to do work directly from hors database
"""


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
    "--subjectPad",
    help="Padding to add before subject # EX: pad = 3... 3 -> 003",
    required=True,
)
@click.option(
    "--sitePad",
    help="Padding to add before site #. EX: pad = 3... 3 -> 003",
    required=True,
)
@click.option("--studySplit", help="delimiter between study name and site")
@click.option("--siteSplit", help="delimitter between site and subject")
@click.option("--timepointSplit", help="delimitter between study and timepoint")
def clean(
    input_path, output_path, subjectPad, sitePad, studySplit, siteSplit, timepointSplit
):
    logging.info(f"Cleaning has started")
    logging.info(f"Exporting from {input_path}")
    logging.info(f"Exporting to {output_path}")

    sp = StudyPipeline()
    sp.ETL()


if __name__ == "__main__":
    cli()
