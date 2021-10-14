import os
from pathlib import Path
import re
from datetime import datetime
import subprocess
import csv
import conf.config as config

COLUMNS = list(filter(None, config.COLUMNS.split(",")))
DATE = datetime.now().strftime("%Y-%m-%d")


def filter_csv(csv_file, directory):
    print(f"Filtering {csv_file} ...")
    with open(csv_file, encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        data = {}
        for row in reader:
            for header, value in row.items():
                if header in COLUMNS:
                    try:
                        data[header].append(value)
                    except KeyError:
                        data[header] = [value]

    with open(directory / f"{DATE}_[FLTRD].csv", "w") as out_file:
        rows = []

        header_row = []
        for col_header in data:
            header_row.append(col_header)
        rows.append(header_row)

        for i in range(len(data[COLUMNS[0]])):
            row = []
            for d in data:
                row.append(data[d][i])

            rows.append(row)

        out_writer = csv.writer(out_file)

        for row in rows:
            out_writer.writerow(row)


def crawl(url, task_name):
    print(f"Crawling {task_name} ...")
    output_directory = Path(config.OUTPUT_PATH) / task_name
    export = "Internal:All"

    stream = subprocess.Popen([
        f"{config.APP}",
        f"--headless",
        f"--output-folder {output_directory}",
        f"--export-format csv",
        f"--export-tabs {export}",
        f"--crawl {url}",
    ])

    stream.wait()

    pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
    for file in os.listdir(output_directory):
        if not pattern.match(file):
            filter_csv(Path(output_directory) / file, Path(output_directory))
            print(f"Renaming {file} to {DATE}_{task_name}_{file}")
            os.rename(f"{output_directory}/{file}",
                      f"{output_directory}/{DATE}_{task_name}_{file}")
    print(f"{task_name}: Done.")
