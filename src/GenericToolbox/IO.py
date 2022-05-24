#!/usr/bin/env python
# -*- coding: utf-8 -*-


def getListOfFilesInSubFolders(inputFolder_, extension_='', nameCondition_='', keepFullPath_=False):
    import os
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
    import os

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
    import os

    if os.path.isdir(directory_path):
        pass
    elif os.path.isfile(directory_path):
        raise OSError("%s exists as a regular file." % directory_path)
    else:
        parent, directory = os.path.split(directory_path)
        if parent and not os.path.isdir(parent): mkdir(parent)
        if directory: os.mkdir(directory_path)


def ls(input_path_):
    import os

    if input_path_[0] != '/':
        input_path_ = os.getcwd() + '/' + input_path_
    return os.popen('cd ' + os.getcwd() + ' && ls ' + input_path_).read().split('\n')[:-1]


def get_list_of_files_in_folder(input_folder_, extension_='', name_format_=''):
    import os

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
    import os
    return (env_variable_ in os.environ)


def get_env_variable(env_variable_):
    if not isEnvVarDefined(env_variable_):
        import sys
        print("Env variable has not been set: " + str(env_variable_))
        sys.exit(1)
    else:
        import os
        return os.environ.get(env_variable_)


def get_current_os():
    import os

    current_os = str()

    os_string = os.popen('lsb_release -si').read()
    os_string = os_string[:-1]

    if os_string == "Scientific":
        current_os = "sl6"
    elif os_string == "CentOS":
        current_os = "cl7"

    return current_os


def getTerminalSize():
    import os

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
