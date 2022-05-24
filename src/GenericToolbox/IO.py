#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


def getListOfFilesInSubFolders(inputFolder_, extension_='', nameCondition_='', keepFullPath_=False):
    files_list = list()
    inputFolder_ = inputFolder_.replace('\ ', ' ')

    for path, subDirs, files in os.walk(inputFolder_):
        for name in files:
            file_path = os.path.join(path, name)
            if (extension_ == '' or file_path.split('.')[-1] == extension_) \
                    and (nameCondition_ == '' or nameCondition_ in file_path):
                index_shift = 0
                if not keepFullPath_:
                    index_shift = len(inputFolder_)
                files_list.append(file_path[index_shift:])

    return files_list


def splitFileNameAndFolderPath(filePath_):

    if os.name == 'nt':
        splited_string = filePath_.split('\\')
        file_name = splited_string[-1]
        folder_path = '\\'.join(splited_string[0:-1])
    else:
        splited_string = filePath_.split('/')
        file_name = splited_string[-1]
        folder_path = '/'.join(splited_string[0:-1])

    return folder_path, file_name



