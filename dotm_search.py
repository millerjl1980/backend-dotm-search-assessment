#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Given a directory path, search all files in the path for a given text string
within the 'word/document.xml' section of a MSWord .dotm file.
"""
__author__ = 'Justin Miller'

# Updates from demo on 3/5 utalized

import os
import sys
import zipfile
import argparse

DOC_FILENAME = 'word/document.xml'

def scan_zipfile(z, search_text, full_path):
    """ Returns True if search text was found"""
    with z.open(DOC_FILENAME) as doc:
        xml_text = doc.read()
    xml_text = xml_text.decode('utf-8')
    text_location = xml_text.find(search_text)
    if text_location >= 0:
        print('Match found in file {}'.format(full_path))
        print(' ...' + xml_text[text_location-40:text_location+40] + '...')
        return True
    return False

def find_args():
    """Creates parser for the searcher and returns the args"""
    parser = argparse.ArgumentParser(description='Searches for given text within the dotm files')
    parser.add_argument('--dir', help='directory to search for dotm files')
    parser.add_argument('text', help='text to search the dotm files for')
    args = parser.parse_args()
    return args


def main():
    args = find_args()
    search_text = args.text
    search_path = args.dir

    if not search_text:
        parser.print_usage()
        sys.exit(1)
    
    print("Searching directory {} for dotm files with text '{}' ...".format(search_path, search_text))

    file_list = os.listdir(search_path)
    match_count = 0
    search_count = 0

    for file in file_list:
        if not file.endswith('.dotm'):
            print(file + "- Not .dotm file")
            continue
        else:
            search_count += 1

        full_path = os.path.join(search_path, file)

        if zipfile.is_zipfile(full_path):
            with zipfile.ZipFile(full_path) as z:
                names = z.namelist()
                if DOC_FILENAME in names:
                    if scan_zipfile(z, search_text, full_path):
                        match_count += 1
        else:
            print("Not a zipfile: " + full_path)

    print('Total dotm files searched: {}'.format(search_count))
    print('Total dotm files matched: {}'.format(match_count))


if __name__ == '__main__':
    main()
