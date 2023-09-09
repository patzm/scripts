import logging
import os
from datetime import datetime

import click


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option(
    "--datetime_format_in",
    default="%Y%m%d_%H%M%S",
    type=str,
    help="Datetime pattern of the input files.",
)
@click.option(
    "--datetime_format_out",
    default="%Y%m%d_%H%M%S",
    type=str,
    help="Datetime pattern of the output files.",
)
@click.option(
    "--dry", default=False, type=bool, help="If set, do not rename any files."
)
def rename(files, datetime_format_in: str, datetime_format_out: str, dry: bool):
    """Renames files with date patterns.

    The patterns are defined according to the convention described here:
    https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    """
    logging.basicConfig(level=logging.INFO)
    logging.info('Parsing input files with datetime format "%s"', datetime_format_in)
    logging.info('Writing output files with datetime format "%s"', datetime_format_out)
    for file_path in files:
        if not os.path.isfile(file_path):
            logging.warning("%s is not a file. Skipping ...", file_path)
            continue
        folder, file_name = os.path.split(file_path)
        file_base_name, file_ext = os.path.splitext(file_name)

        # Extract datetime format
        try:
            file_date_time = datetime.strptime(file_base_name, datetime_format_in)
        except ValueError as err:
            logging.warning(
                "Could not automatically parse datetime from " '"%s": %s',
                file_base_name,
                err.message,
            )
            continue

        # Form new file name
        new_file_base_name = datetime.strftime(file_date_time, datetime_format_out)
        new_file_name = new_file_base_name + file_ext
        new_file_path = os.path.join(folder, new_file_name)

        # Rename the file
        logging.info("Renaming %s to %s", file_name, new_file_name)
        if not dry:
            os.rename(file_path, new_file_path)
