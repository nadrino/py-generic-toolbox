#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil


def printIf(condition_, *args, sep=' ', end='\n', file=None):
    if condition_:
        print(*args, sep=sep, end=end, file=file)


def copyFile(src_, dst_):
    if not os.path.exists(dst_) and not os.path.exists( os.path.join(dst_, os.path.basename(src_))):
        return
    shutil.copy2(src_, dst_)


def getListOfFilesInSubFolders(inputFolder_, extension_='', nameCondition_='', keepFullPath_=False, nameExclude_=None,
                               includeHiddenFolders_=False, includeHiddenFiles_=False):
    

    output = getListOfFilesInFolder(inputFolder_, extension_=extension_, nameCondition_=nameCondition_,
                                    keepFullPath_=keepFullPath_, nameExcludeList_=nameExclude_,
                                    includeHidden_=includeHiddenFiles_)

    for subFolder in getListOfFoldersInFolder(inputFolder_, keepFullPath_=False, includeHidden_=includeHiddenFolders_):
        subFilesList = getListOfFilesInSubFolders(inputFolder_ + "/" + subFolder, extension_=extension_, nameCondition_=nameCondition_,
                                             keepFullPath_=False, nameExclude_=nameExclude_,
                                             includeHiddenFolders_=includeHiddenFolders_,
                                             includeHiddenFiles_=includeHiddenFiles_)
        for iFile in range(len(subFilesList)):
            if keepFullPath_:
                subFilesList[iFile] = os.path.join(os.path.join(inputFolder_, subFolder), subFilesList[iFile])
            else:
                subFilesList[iFile] = os.path.join(subFolder, subFilesList[iFile])
        output += subFilesList

    return output


def getListOfFilesInFolder(inputFolder_, extension_='', nameCondition_='', keepFullPath_=False, nameExcludeList_=None,
                           includeHidden_=False):
    
    try:
        return sorted([
            ( os.path.join(inputFolder_, f) if keepFullPath_ else f ) for f in os.listdir(inputFolder_)
            if (
                    os.path.isfile(os.path.join(inputFolder_, f))
                    and (extension_ == '' or os.path.splitext(f)[1] == "."+extension_)
                    and (nameCondition_ == '' or nameCondition_ in f)
                    and (nameExcludeList_ == None or any(nameExclude not in f for nameExclude in nameExcludeList_) )
                    and (includeHidden_ == True or f[0] != '.')
               )
                ])
    except FileNotFoundError as error:
        return list()


def getListOfFoldersInFolder(inputFolder_, nameCondition_='', keepFullPath_=False, nameExcludeList_=None,
                             includeHidden_=False):
    
    try:
        return sorted([
            (os.path.join(inputFolder_, folderNameCandidate) if keepFullPath_ else folderNameCandidate)
            for folderNameCandidate in os.listdir(inputFolder_)
            if (
                    os.path.isdir(os.path.join(inputFolder_, folderNameCandidate))
                    and (nameCondition_ == '' or nameCondition_ in folderNameCandidate)
                    and (nameExcludeList_ == None or any(nameExclude not in folderNameCandidate for nameExclude in nameExcludeList_) )
                    and (includeHidden_ == True or folderNameCandidate[0] != '.')
               )
                ])
    except FileNotFoundError as error:
        return list()


def dumpFileLinesToList(filePath_):
    with open(filePath_) as file:
        lines = file.readlines()
        return [line.rstrip() for line in lines]


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

def mkdir(directory_path):
    

    if os.path.isdir(directory_path):
        pass
    elif os.path.isfile(directory_path):
        raise OSError("%s exists as a regular file." % directory_path)
    else:
        parent, directory = os.path.split(directory_path)
        if parent and not os.path.isdir(parent): mkdir(parent)
        if directory: os.mkdir(directory_path)

def ls(input_path_):
    

    if input_path_[0] != '/':
        input_path_ = os.getcwd() + '/' + input_path_
    return os.popen('cd ' + os.getcwd() + ' && ls ' + input_path_).read().split('\n')[:-1]

def get_list_of_files_in_folder(input_folder_, extension_='', name_format_=''):
    

    files_list = list()
    input_folder_ = input_folder_.replace('\ ', ' ')

    for path, subdirs, files in os.walk(input_folder_):
        for name in files:
            file_path = os.path.join(path, name)
            if (extension_ == '' or file_path.split('.')[-1] == extension_) \
                    and (name_format_ == '' or name_format_ in file_path):
                files_list.append(file_path)

    return files_list

def getNowTimeString():
    import time
    return time.strftime("%Y%m%d_%H%M%S", time.gmtime())

def transcriptAudio(wav_file_path_, algorithm_='google'):
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.WavFile(wav_file_path_) as source:
        audio = r.record(source)

        if algorithm_ == 'google':
            try:
                return r.recognize_google(audio, language='en-US', show_all=False)
            except LookupError:
                print('Google cannot understand audio!')
                return '??'
            except sr.UnknownValueError:
                return '??'

        elif algorithm_ == 'sphinx':
            try:
                return r.recognize_sphinx(
                    audio, language='en-US', show_all=False)
            except sr.UnknownValueError:
                print('Sphinx could not understand audio')
            except sr.RequestError as e:
                print('Sphinx error: {0}'.format(str(e)))

def isEnvVarDefined(env_variable_):
    
    return (env_variable_ in os.environ)

def get_env_variable(env_variable_):
    if not isEnvVarDefined(env_variable_):
        import sys
        print("Env variable has not been set: " + str(env_variable_))
        sys.exit(1)
    else:
        
        return os.environ.get(env_variable_)

def get_current_os():
    

    current_os = str()

    os_string = os.popen('lsb_release -si').read()
    os_string = os_string[:-1]

    if os_string == "Scientific":
        current_os = "sl6"
    elif os_string == "CentOS":
        current_os = "cl7"

    return current_os

def getTerminalSize():
    

    env = os.environ

    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr

    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        # try:
        #    cr = (env['LINES'], env['COLUMNS'])
        # except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])

def select_in_xml(root_, result_types_, result_leaf_conditions_list_, branch_conditions_list_):
    # result_type_ = \
    #     [
    #         "",
    #         "strref"
    #     ]
    # result_leaf_conditions_list = \
    #     [
    #         [
    #             {"type": 'label', "value": 'OpenLockDC'}
    #         ],[
    #             {"type": 'label', "value": 'LocName'}
    #         ]
    #     ]
    # branch_conditions_list = \
    #     [
    #         [
    #             {"type": 'label', "value": 'Locked'},
    #             {"type": '', "value": '1'},
    #         ],[
    #             {"type": 'label', "value": "ItemList"}
    #         ]
    #     ]

    global is_result_branch
    is_result_branch = False
    global result_value
    result_value = list()
    results_list = list()
    for result_index in range(len(result_types_)):
        result_value.append("")

    def recur_branches(branch_, branch_conditions_trigger_=list()):

        global is_result_branch
        global result_value

        # Default case (first branch loop)
        if branch_conditions_trigger_ == list():
            for branch_condition in branch_conditions_list_:
                branch_conditions_trigger_.append(False)

        # fill the branch_conditions_trigger_ (shared in the branch)
        for leaf_index in range(len(branch_conditions_list_)):
            if not branch_conditions_trigger_[leaf_index]:
                all_inner_leaf_conditions_fulfilled = True
                for leaf_condition_index in range(len(branch_conditions_list_[leaf_index])):
                    attrib_type = branch_conditions_list_[leaf_index][leaf_condition_index]['type']
                    attrib_value = branch_conditions_list_[leaf_index][leaf_condition_index]['value']
                    if attrib_type == '':
                        if attrib_value != branch_.text:
                            all_inner_leaf_conditions_fulfilled = False
                    else:
                        if attrib_type not in branch_.attrib:
                            all_inner_leaf_conditions_fulfilled = False
                        elif attrib_value != branch_.attrib[attrib_type]:
                            all_inner_leaf_conditions_fulfilled = False
                if all_inner_leaf_conditions_fulfilled:
                    branch_conditions_trigger_[leaf_index] = True

        # if all condition has been met, then it is the right branch
        if False not in branch_conditions_trigger_ and len(branch_conditions_trigger_) != 0:
            is_result_branch = True

        for result_leaf_index in range(len(result_types_)):

            is_result_leaf = False
            for result_condition in result_leaf_conditions_list_[result_leaf_index]:
                if result_condition['type'] == '':
                    if result_condition['value'] == branch_.text:
                        is_result_leaf = True
                else:
                    if result_condition['type'] in branch_.attrib:
                        if result_condition['value'] == branch_.attrib[result_condition['type']]:
                            is_result_leaf = True

            if is_result_leaf:
                if result_types_[result_leaf_index] == '':
                    result_value[result_leaf_index] = branch_.text
                else:
                    result_value[result_leaf_index] = branch_.attrib[result_types_[result_leaf_index]]

        if not is_result_branch \
                or True: # continue looping if it's not the result_branch
            branch_conditions_trigger = list() # sub-branch conditions
            for branch_condition in branch_conditions_list_:
                branch_conditions_trigger.append(False)

            for elem in list(branch_):
                recur_branches(elem, branch_conditions_trigger)

    recur_branches(root_)

    if is_result_branch or len(branch_conditions_list_) == 0:
        return result_value
    else:
        return None
