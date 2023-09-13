import os.path
import subprocess
from typing import Optional

import click


@click.command()
@click.argument("url_file")
@click.option("--path", "-p", default=None, type=str)
def download_urls(url_file: str, path: Optional[str]):
    path_arg = ""
    if path:
        path_arg = f"--path {path}"
        os.makedirs(path, exist_ok=True)

    with open(url_file, "r") as f:
        urls = set(s.strip() for s in f.readlines())

    n_urls = len(urls)
    print(f"Found {n_urls} URLs")

    n_failed = 0
    failed_file = os.path.join(path, "failed.txt")
    with open(failed_file, "w") as failed:
        for url in sorted(urls):
            print(f"\nDownloading {url}")
            command = f"scdl {path_arg} -c -l {url}"
            try:
                output = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
            except subprocess.CalledProcessError as e:
                if "already downloaded" not in str(e.stderr):
                    n_failed += 1
                    failed.write(f"{url} - {e.output}")
                    print(f"Failed: {e.stderr}")
                else:
                    print("... skipping, already downloaded.")
                continue

            print(output.stdout)
