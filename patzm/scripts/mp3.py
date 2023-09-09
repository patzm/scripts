import os

import click

WORKDIR = os.path.expanduser("~/Downloads/A Princess of Mars")
CHAPTERS_FILE = os.path.join(WORKDIR, "chapters.txt")
OUTPUT_DIR = os.path.expanduser("~/Music/A Princess of Mars")


def join():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(CHAPTERS_FILE, "r") as chapters_file:
        for i_line, line in enumerate(chapters_file):
            line = line.rstrip()
            title, pages = line.split(": ")
            p_start, p_stop = pages.split(" - ")
            p_start = int(p_start)
            p_stop = int(p_stop)
            print(p_start, p_stop)
            new_file_name = "{i:02d} {title}.mp3".format(
                i=i_line + 1, title=title[0].upper() + title[1:]
            )
            old_file_pattern = "{i:03d} - A Princess of Mars.mp3"
            old_path_names = [
                os.path.join(WORKDIR, old_file_pattern.format(i=i))
                for i in range(p_start, p_stop + 1)
            ]
            new_path_name = os.path.join(OUTPUT_DIR, new_file_name)
            command = 'cat {files_in} \\\n> "{file_out}"'.format(
                files_in=" ".join(
                    '"' + old_path_name + '"' for old_path_name in old_path_names
                ),
                file_out=new_path_name,
            )
            print(command)
            os.system(command)
