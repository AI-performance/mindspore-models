#!/usr/bin/python
# -*- coding: UTF-8 -*-

import hashlib
import os
import sys
import subprocess

DEBUG = False

def get_file_size_mb(file_path):
    try:
        file_size = os.path.getsize(file_path)
	if DEBUG: print(file_size)
        return file_size / (1000000.)
    except Exception as err:
        print(err)


def get_file_md5(file_path):
    if not os.path.isfile(file_path):
        return ""
    myhash = hashlib.md5()
    f = open(file_path, "rb")
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    if DEBUG: print(myhash.hexdigest())
    return myhash.hexdigest()


def main():
    output_file_name = "README.md"
    work_dir = sys.argv[1] if len(sys.argv) > 1 else "."

    output = subprocess.Popen(['ls -l ' + work_dir],stdout=subprocess.PIPE, shell=True).communicate()
    summary_str = ""
    summary_header = "| fileName | fileAuthor | modifyDate | MB | md5 |\n"
    summary_format = "|:--|:--|:--|:--|:--|\n"
    summary_str += summary_header + summary_format

    print output[0]
    each_file_lines = output[0].split("\n")[1:]
    for line_idx in range(len(each_file_lines)):
	line = each_file_lines[line_idx]
        line_info_list = line.split()
	if DEBUG: print line_info_list
        author = "/".join(line_info_list[2:4]) if len(line_info_list) > 3 else "AuthorIsNull"
        size_mb = int(line_info_list[4]) / 1000000. if len(line_info_list) > 4 else "SizeIsNull"
        modify_date = "-".join(line_info_list[5:8]) if len(line_info_list) > 7 else "DateIsNull"
	name = line_info_list[8] if len(line_info_list) > 8 else "NameIsNull"
        md5 = get_file_md5(name)
        summary_line_list = [name, author, modify_date, size_mb, md5]
        summary_line_list = map(str, summary_line_list)
        summary_line = "|" + " | ".join(summary_line_list) + " |\n"
        summary_str += summary_line
	if DEBUG: print(summary_line)

    with open(output_file_name, "w") as out_file:
	out_file.write(summary_str)


if __name__ == "__main__":
    main()
