import os
from pathlib import Path
import time
import platform
import re
from customdiff import CustomHtmlDiff
import conf.config as config


# courtesy of Stack Overflow
def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime


def get_latest_file(files, current_directory):
    """
    Calculate the smallest difference between now and the creation of file,
    then remove it from list, to get second youngest file in the following call
    """
    time_deltas = [
        time.time() - creation_date(Path(current_directory) / f) for f in files]
    latest_file = files.pop(time_deltas.index(min(time_deltas)))

    return Path(current_directory) / latest_file


def compare(task_name):
    current_directory = Path(config.OUTPUT_PATH, task_name)
    pattern = re.compile(r"\d{4}-\d{2}-\d{2}_\[FLTRD\]")

    files = [f for f in os.listdir(current_directory) if pattern.match(
        f) and os.path.isfile(Path(current_directory) / f)]

    if len(files) <= 1:
        return False

    new_file = get_latest_file(files, current_directory)
    old_file = get_latest_file(files, current_directory)

    with open(old_file) as ff:
        fromlines = ff.readlines()
    with open(new_file) as tf:
        tolines = tf.readlines()

    fromlines = fromlines[1:]
    fromlines.sort()

    tolines = tolines[1:]
    tolines.sort()

    diff = CustomHtmlDiff(wrapcolumn=75).make_file(
        fromlines, tolines, os.path.split(old_file)[1], os.path.split(new_file)[1])

    return diff
