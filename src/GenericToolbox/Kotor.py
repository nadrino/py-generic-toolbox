#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform

import Parallel as tParallel
import IO as tIO
import Colors as tColors


class KotorExtractor():

    def __init__(self):
        self.pathToK1Dict = dict()
        self.pathToK1Dict[
            'macOS'] = "/Users/ablanche/Library/Application Support/Steam/steamapps/common/swkotor/Knights of the Old Republic.app/Contents/Assets/"
        self.pathToK1Dict['Windows'] = "/mnt/d/Games/GOG/Star Wars - KotOR/"
        self.pathToK1Dict['XBox'] = "/Users/ablanche/Desktop/temp/kotor_extraction_tools/kotor_XBox"
        self.pathToK1Dict['Switch'] = "/Users/ablanche/Desktop/temp/kotor_extraction_tools/kotor_Switch"
        self.pathToK1Dict['iOS'] = "/Users/ablanche/Documents/Kotor/iOS/KOTOR.app/"

        self.pathToK2Dict = dict()
        self.pathToK2Dict[
            'macOS'] = "/Users/ablanche/Library/Application Support/Steam/steamapps/common/Knights of the Old Republic II/KOTOR2.app/Contents/GameData/"
        self.pathToK2Dict['Windows'] = "/mnt/d/Games/GOG/Star Wars - KotOR2/"
        self.pathToK2Dict['XBox'] = "/Volumes/Adrien 8To EHD/Jeux/XBox/Jeux/Star Wars - Knights of the Old Republic 2/"

        self.debug = False
        self.currentPlatform = "macOS"
        self.currentKotorGame = "kotor1"

    def getOutputDirPath(self, name_):
        if platform.system() == "Darwin":
            return "/Users/ablanche/Desktop/temp/kotor_extraction_tools/" + name_ + "/" + self.currentPlatform + "/" + self.currentKotorGame + "/"
        else:
            return "./out/" + name_ + "/" + self.currentPlatform + "/" + self.currentKotorGame + "/"

    def getCurrentPathToKotor(self):
        if self.currentKotorGame == "kotor1":
            return self.pathToK1Dict[self.currentPlatform]
        elif self.currentKotorGame == "kotor2":
            return self.pathToK2Dict[self.currentPlatform]
        else:
            print(tColors.error + "Unknown current_kotor_game: " + str(self.currentKotorGame))
            exit(1)

    def extract_bif_files(self, game_folder_, output_folder_):
        import os
        from tqdm import tqdm

        files_list = tIO.getListOfFilesInSubFolders(game_folder_ + "/data/", 'bif')
        key_file_path = game_folder_ + "/chitin.key"

        for file_path in tqdm(files_list):

            tIO.mkdir(output_folder_ + "/" + file_path)

            command_line_arguments = list()
            command_line_arguments.append("cd")
            command_line_arguments.append("'" + output_folder_ + "/" + file_path + "'")
            command_line_arguments.append("&&")
            command_line_arguments.append("unkeybif")
            command_line_arguments.append("e")
            command_line_arguments.append("'" + key_file_path + "'")
            command_line_arguments.append("'" + game_folder_ + "/data/" + file_path + "'")

            if self.debug:
                print(" ".join(command_line_arguments))
            os.system(" ".join(command_line_arguments) + " > /dev/null 2>&1")

        return

    def extract_erf_files(self, game_folder_, output_folder_):
        import os
        from tqdm import tqdm

        files_list = tIO.getListOfFilesInSubFolders(game_folder_ + "/Modules/", 'erf')

        for file_path in tqdm(files_list):
            tIO.mkdir(output_folder_ + "/" + file_path)

            command_line_arguments = list()
            command_line_arguments.append("cd")
            command_line_arguments.append("'" + output_folder_ + "/" + file_path + "'")
            command_line_arguments.append("&&")
            command_line_arguments.append("unerf")
            command_line_arguments.append("x")
            command_line_arguments.append("'" + game_folder_ + "/Modules/" + file_path + "'")

            if self.debug:
                print(" ".join(command_line_arguments))
            os.system(" ".join(command_line_arguments) + " > /dev/null 2>&1")

        return

    def convert_dlg_to_xml(self, input_folder_, output_folder_):
        import os
        from tqdm import tqdm

        files_list = tIO.getListOfFilesInSubFolders(input_folder_, 'dlg')

        for file_path in tqdm(files_list):

            sub_folder = "/".join(file_path.split("/")[:-1])
            out_file_name = file_path.split("/")[-1]

            tIO.mkdir(output_folder_ + "/" + sub_folder)

            command_line_arguments = list()
            command_line_arguments.append("gff2xml")
            command_line_arguments.append("--" + str(self.currentKotorGame))
            command_line_arguments.append("--cp1252")
            command_line_arguments.append("'" + input_folder_ + "/" + file_path + "'")
            command_line_arguments.append("'" + output_folder_ + "/" + sub_folder + "/" + file_path + "'")

            if self.debug:
                print(" ".join(command_line_arguments))
            os.system(" ".join(command_line_arguments) + " > /dev/null 2>&1")

        return

    def extract_dlg_files(self, game_folder_, output_folder_):

        tIO.mkdir(output_folder_)

        return

    def get_item_name(self, item_ref_):
        # NOT FINISHED
        import xml.etree.ElementTree as ET

        item_file = "xml/templates/itempalstd.itp.xml"
        tree = ET.parse(item_file)
        root = tree.getroot()

        last_item_name = ""
        item_name = ""

        def look_inside(branch_):

            for sub_branch_ in branch_:
                try:
                    if sub_branch_.attrib["label"] == "NAME":
                        last_item_name = sub_branch_.text
                    if sub_branch_.attrib["label"] == "RESREF":
                        if item_ref_ == sub_branch_.text:
                            item_name = last_item_name
                        break
                except:
                    pass
                look_inside(sub_branch_)

        look_inside(root[0])

        return item_name

    def unrim_kotor(self):
        import os
        from tqdm import tqdm

        print(tColors.warning + "Unfolding .rim files...")

        files_list = tIO.getListOfFilesInSubFolders(self.getCurrentPathToKotor(), 'rim')

        for file_path in tqdm(files_list):
            outfolderpath = self.getOutputDirPath("unfolded") + file_path
            if os.path.isdir(outfolderpath):
                continue  # skip
            os.system("mkdir -p " + outfolderpath)
            command_line = "cd \"" + outfolderpath + "\"" + " && unrim e \"" + self.getCurrentPathToKotor() + "/" + file_path + "\""
            if self.debug:
                print(command_line)
            os.system(command_line + " > /dev/null 2>&1")

    def unkeybif_kotor(self):
        from tqdm import tqdm
        import os

        print(tColors.warning + "Unfolding .bif files...")

        files_list = tIO.getListOfFilesInSubFolders(self.getCurrentPathToKotor(), 'bif')

        def process(file_path_):

            if "/saves/" in file_path_:
                return  # skip

            outpath = self.getOutputDirPath("unfolded") + file_path_
            if os.path.isdir(outpath):
                return  # skip

            os.system("mkdir -p " + outpath)
            command_line = "cd \"" + outpath + "\""
            command_line += " && unkeybif e \"" + self.getCurrentPathToKotor() + "/" + file_path_ + "\""
            command_line += " \"" + self.getCurrentPathToKotor() + "/chitin.key" + "\""
            if self.debug:
                print(command_line)
            os.system(command_line + " > /dev/null 2>&1")

        tParallel.runParallel(process, files_list)

    def unerf_kotor(self):
        from tqdm import tqdm
        import os

        print(tColors.warning + "Unfolding .erf files...")

        files_list = tIO.getListOfFilesInSubFolders(self.getCurrentPathToKotor(), 'erf')
        files_list += tIO.getListOfFilesInSubFolders(self.getCurrentPathToKotor(), 'mod')
        files_list += tIO.getListOfFilesInSubFolders(self.getCurrentPathToKotor(), 'sav')

        def process(file_path_):

            if "saves/" in file_path_:
                return  # skip

            outpath = self.getOutputDirPath("unfolded") + file_path_
            if os.path.isdir(outpath):
                return  # skip

            os.system("mkdir -p " + outpath)

            command_line = "cd \"" + outpath + "\""
            command_line += " && unerf x \"" + self.getCurrentPathToKotor() + "/" + file_path_ + "\""
            if self.debug:
                print(command_line)
            os.system(command_line + " > /dev/null 2>&1")

        tParallel.runParallel(process, files_list)

    def unfold_kotor(self):
        self.unerf_kotor()
        self.unkeybif_kotor()
        self.unrim_kotor()

    def extract_and_fix_audio_kotor(self):
        from tqdm import tqdm
        import os

        files_list = list()

        if self.currentPlatform == "XBox":
            print(tColors.warning + "Extracting .wav / .wma files...")
            files_list = tIO.getListOfFilesInSubFolders(self.getCurrentPathToKotor(), 'wav')
            files_list += tIO.getListOfFilesInSubFolders(self.getCurrentPathToKotor(), 'wma')
        else:
            print(tColors.warning + "Extracting and fixing of .wav files...")
            files_list = tIO.getListOfFilesInSubFolders(self.getCurrentPathToKotor(), 'wav')

        def process(file_path):

            out_folder_path = self.getOutputDirPath("extracted") + tIO.splitFileNameAndFolderPath(file_path)[0]
            out_file_name = tIO.splitFileNameAndFolderPath(file_path)[1]
            out_file_path = out_folder_path + "/" + out_file_name
            if self.currentPlatform != "XBox":
                out_file_path += ".mp3"

            if os.path.isfile(out_file_path):
                # print("skipping " + file_path)
                return

            os.system("mkdir -p " + out_folder_path)

            command_line = list()
            if self.currentPlatform == "XBox":
                command_line.append("cp")
                command_line.append("\"" + self.getCurrentPathToKotor() + "/" + file_path + "\"")
                command_line.append("\"" + out_file_path + "\"")
                command_line.append("&>")
                command_line.append("/dev/null")
            else:
                command_line.append("sfk partcopy")
                command_line.append("\"" + self.getCurrentPathToKotor() + "/" + file_path + "\"")
                command_line.append("-allfrom 52")
                command_line.append("\"" + out_file_path + "\"")
                command_line.append("-yes")
                command_line.append("&>")
                command_line.append("/dev/null")

            if self.debug:
                print(" ".join(command_line))
            os.system(" ".join(command_line))

        tParallel.runParallel(process, files_list)

        print(tColors.warning + "Copying remaining .wav files from unfolded folder...")
        unfolded_path = self.getOutputDirPath("unfolded")
        files_list = tIO.getListOfFilesInSubFolders(unfolded_path, 'wav')

        def process(file_path):

            out_folder_path = self.getOutputDirPath("extracted") + \
                              tIO.splitFileNameAndFolderPath(file_path)[0]
            out_file_name = tIO.splitFileNameAndFolderPath(file_path)[1]
            out_file_path = out_folder_path + "/" + out_file_name
            if os.path.isfile(out_file_path):
                # print("skipping " + file_path)
                return

            os.system("mkdir -p " + out_folder_path)

            command_line = list()
            command_line.append("cp")
            command_line.append("\"" + unfolded_path + "/" + file_path + "\"")
            command_line.append("\"" + out_file_path + "\"")
            # command_line.append("&>")
            # command_line.append("/dev/null")
            if self.debug:
                print(" ".join(command_line))
            os.system(" ".join(command_line))

        tParallel.runParallel(process, files_list)

    def extract_tlk_kotor(self):
        from tqdm import tqdm
        import os

        print(tColors.warning + "Extracting .tlk files...")

        files_list = tIO.getListOfFilesInSubFolders(self.getCurrentPathToKotor(), 'tlk')

        for file_path in tqdm(files_list):
            out_folder = self.getOutputDirPath("extracted") + tIO.splitFileNameAndFolderPath(file_path)[
                0]
            out_filename = tIO.splitFileNameAndFolderPath(file_path)[1]
            out_filepath = out_folder + "/" + out_filename + ".xml"
            if os.path.isfile(out_filepath):
                continue  # skip

            os.system("mkdir -p " + out_folder)

            game_arg = "--kotor"
            if self.currentKotorGame == "kotor2":
                game_arg += "2"

            command_line = "tlk2xml " + game_arg + " '" + self.getCurrentPathToKotor() + "/" + file_path + "'"
            command_line += " \"" + out_filepath + "\""
            if self.debug:
                print(command_line)
            os.system(command_line + " > /dev/null 2>&1")

    def convertTextures(self):
        from tqdm import tqdm
        import os

        print(tColors.warning + "Converting .tpc files...")

        unfolded_path = self.getOutputDirPath("unfolded") + '/'
        files_list = tIO.getListOfFilesInSubFolders(unfolded_path, 'tpc')

        def process(file_path):
            out_folder = self.getOutputDirPath("extracted") + tIO.splitFileNameAndFolderPath(file_path)[
                0]
            out_filename = tIO.splitFileNameAndFolderPath(file_path)[1]
            out_filepath = out_folder + "/" + out_filename + ".tga"
            if os.path.isfile(out_filepath):
                return  # skip

            os.system("mkdir -p " + out_folder)

            command_line = "xoreostex2tga " + unfolded_path + "/" + file_path
            command_line += " " + out_filepath

            if self.debug:
                print(command_line)
                os.system(command_line)
            else:
                os.system(command_line + " > /dev/null 2>&1")

        tParallel.runParallel(process, files_list)

        print(tColors.warning + "Moving .tga files...")
        files_list = tIO.getListOfFilesInSubFolders(unfolded_path, 'tga')

        def process(file_path):
            out_folder = self.getOutputDirPath("extracted") + tIO.splitFileNameAndFolderPath(file_path)[
                0]
            out_filename = tIO.splitFileNameAndFolderPath(file_path)[1]
            out_filepath = out_folder + "/" + out_filename
            if os.path.isfile(out_filepath):
                os.system("rm \"" + unfolded_path + "/" + file_path + "\"")
                return

            os.system("mkdir -p " + out_folder)

            command_line = "mv " + "\"" + unfolded_path + "/" + file_path + "\""
            command_line += " " + "\"" + out_filepath + "\""
            os.system(command_line)

        tParallel.runParallel(process, files_list)

    def convert_2da_files_kotor(self):
        from tqdm import tqdm
        import os

        print(tColors.warning + "Converting .2da files...")

        unfolded_path = self.getOutputDirPath("unfolded")
        files_list = tIO.getListOfFilesInSubFolders(unfolded_path, '2da')

        def process(file_path):
            out_folder = self.getOutputDirPath("extracted") + tIO.splitFileNameAndFolderPath(file_path)[
                0]
            out_filename = tIO.splitFileNameAndFolderPath(file_path)[1]
            out_filepath = out_folder + "/" + out_filename
            if os.path.isfile(out_filepath):
                return  # skip

            os.system("mkdir -p " + "\"" + out_folder + "\"")

            if not os.path.isfile("\"" + unfolded_path + "/" + file_path + "\""):
                command_line = "convert2da --csv"
                command_line += " -o \"" + out_filepath + "\""
                command_line += " \"" + unfolded_path + "/" + file_path + "\""
                if self.debug:
                    print(command_line)
                os.system(command_line + " > /dev/null 2>&1")
                os.system("rm \"" + unfolded_path + "/" + file_path + "\"")

        tParallel.runParallel(process, files_list)

    def convert_gff_type_files_kotor(self):
        from tqdm import tqdm
        import os

        print(tColors.warning + "Converting gff type files...")

        unfolded_path = self.getOutputDirPath("unfolded")
        files_list = tIO.getListOfFilesInSubFolders(unfolded_path)

        valid_ext_list = ['gui', 'uti', 'dlg', 'utw', 'utd', 'utt', 'utc',
                          'utp', 'uts', 'utm', 'pth', 'fac', 'git', 'ifo',
                          'are', 'ute', 'jrl',
                          'itp', 'ltr', 'btc',
                          'bic', 'bti']

        new_file_list = list()
        for file_path in files_list:
            if file_path.split(".")[-1] in valid_ext_list:
                new_file_list.append(file_path)

        files_list = new_file_list

        def process(file_path_):

            out_folder = self.getOutputDirPath("extracted") + tIO.splitFileNameAndFolderPath(file_path_)[
                0]
            out_filename = tIO.splitFileNameAndFolderPath(file_path_)[1]
            out_filepath = out_folder + "/" + out_filename
            if os.path.isfile(out_filepath):
                return  # skip

            os.system("mkdir -p " + out_folder)

            game_arg = "--kotor"
            if self.currentKotorGame == "kotor2": game_arg += "2"

            if not os.path.isfile(out_folder + "/" + out_filename):
                command_line = "gff2xml " + game_arg
                command_line += " " + unfolded_path + "/" + file_path_
                command_line += " " + out_filepath
                if self.debug:
                    print(command_line)
                os.system(command_line + " > /dev/null 2>&1")

            # os.system("rm " + unfolded_path + "/" + file_path_)

        tParallel.runParallel(process, files_list)

        # print(libToolbox.alert + "VALID FILE EXTs :")
        # print(valid_file_ext_list)
        # ['gui', 'uti', 'dlg', 'utw', 'utd', 'utt', 'utc',
        # 'utp', 'uts', 'utm', 'pth', 'fac', 'git', 'ifo',
        # 'are', 'ute', 'jrl',
        # 'itp', 'ltr', 'btc',
        # 'bic', 'bti']

    def convertSsfFilesKotor(self):
        from tqdm import tqdm
        import os

        print(tColors.warning + "Converting .ssf files...")

        unfolded_path = self.getOutputDirPath("unfolded")
        files_list = tIO.getListOfFilesInSubFolders(unfolded_path, 'ssf')

        for file_path in tqdm(files_list):
            out_folder = self.getOutputDirPath("extracted") + tIO.splitFileNameAndFolderPath(file_path)[
                0]
            out_filename = tIO.splitFileNameAndFolderPath(file_path)[1]
            out_filepath = out_folder + "/" + out_filename + ".xml"
            if os.path.isfile(out_filepath):
                continue  # skip

            os.system("mkdir -p " + out_folder)

            command_line = "ssf2xml"
            command_line += " " + unfolded_path + "/" + file_path
            command_line += " " + out_folder + "/" + out_filename + ".xml"
            # os.system(command_line)
            os.system(command_line + " > /dev/null 2>&1")
            os.system("rm " + unfolded_path + "/" + file_path)

    def decompile_ncs_kotor(self):
        from tqdm import tqdm
        import os

        print(tColors.warning + "Decompiling .ncs / .nss files...")

        unfolded_path = self.getOutputDirPath("unfolded")
        files_list = tIO.getListOfFilesInSubFolders(unfolded_path, 'ncs')
        files_list += tIO.getListOfFilesInSubFolders(unfolded_path, 'nss')

        def process(file_path_):

            out_folder = self.getOutputDirPath("extracted") + tIO.splitFileNameAndFolderPath(file_path_)[
                0]
            out_filename = tIO.splitFileNameAndFolderPath(file_path_)[1]

            os.system("mkdir -p " + out_folder)

            out_file_path = out_folder + "/" + out_filename + ".ncsdis"
            if not os.path.isfile(out_file_path):
                cmd_arg = list()
                cmd_arg.append("ncsdis")
                cmd_arg.append("--" + str(self.currentKotorGame))  # game preset
                cmd_arg.append(unfolded_path + "/" + file_path_)  # input
                cmd_arg.append(out_file_path)  # output
                cmd_arg.append("&> /dev/null")  # no printout
                os.system(" ".join(cmd_arg))

            out_file_path = out_folder + "/" + out_filename + ".ncsdecomp"
            if not os.path.isfile(out_file_path):
                cmd_arg = list()
                cmd_arg.append("ncsdecomp")
                cmd_arg.append("--" + str(self.currentKotorGame))  # game preset
                cmd_arg.append(unfolded_path + "/" + file_path_)  # input
                cmd_arg.append(out_file_path)  # output
                cmd_arg.append("&> /dev/null")  # no printout
                os.system(" ".join(cmd_arg))

            # os.system("rm " + unfolded_path + "/" + file_path_)

        tParallel.runParallel(process, files_list)

    def copy_remaining_files_kotor(self):
        from tqdm import tqdm
        import os

        print(tColors.warning + "Copying remaining files...")

        unfolded_path = self.getOutputDirPath("unfolded")

        print(tColors.warning + "copying .lyt files...")
        files_list = tIO.getListOfFilesInSubFolders(unfolded_path, 'lyt')
        for file_path in tqdm(files_list):
            out_folder = self.getOutputDirPath("extracted") + tIO.splitFileNameAndFolderPath(file_path)[
                0]
            out_filename = tIO.splitFileNameAndFolderPath(file_path)[1]
            out_filepath = out_folder + "/" + out_filename
            if os.path.isfile(out_filepath):
                continue  # skip

            os.system("mkdir -p " + out_folder)

            os.system("cp " + "\"" + unfolded_path + "/" + file_path + "\" \"" + out_filepath + "\"")
            os.system("rm " + "\"" + unfolded_path + "/" + file_path + "\"")

        print(tColors.warning + "copying .vis files...")
        files_list = tIO.getListOfFilesInSubFolders(unfolded_path, 'vis')
        for file_path in tqdm(files_list):
            out_folder = self.getOutputDirPath("extracted") + tIO.splitFileNameAndFolderPath(file_path)[
                0]
            out_filename = tIO.splitFileNameAndFolderPath(file_path)[1]
            out_filepath = out_folder + "/" + out_filename
            if os.path.isfile(out_filepath):
                continue  # skip

            os.system("mkdir -p " + out_folder)

            os.system("cp " + "\"" + unfolded_path + "/" + file_path + "\" \"" + out_filepath + "\"")
            os.system("rm " + "\"" + unfolded_path + "/" + file_path + "\"")

    def get_str_from_ref(self, ref_):
        import xml.etree.ElementTree as ET

        result_string = ""

        dialog_path = self.getOutputDirPath("extracted") + "dialog.tlk.xml"
        dialog_root = ET.parse(dialog_path).getroot()

        result_string = tIO.select_in_xml(
            dialog_root,
            [""],  # output type : ("") means no attribute type i.e. branch.text
            [[{'type': 'id', 'value': ref_}]],  # conditions on leaf
            []  # no conditions on branch
        )[0]

        return result_string

    def get_map_name_from_folder(self, file_path_):
        import xml.etree.ElementTree as ET

        map_folder_path = self.get_rim_folder_from_file(file_path_)
        map_info_path = map_folder_path + tIO.getListOfFilesInSubFolders(map_folder_path, 'are')[0]

        map_info_root = ET.parse(map_info_path).getroot()
        text_id = tIO.select_in_xml(
            map_info_root,
            ["strref"],  # output type : ("") means no attribute type i.e. branch.text
            [[{'type': 'label', 'value': "Name"}]],  # conditions on leaf
            []  # no conditions on branch
        )[0]

        return self.get_str_from_ref(text_id)

    def get_rim_folder_from_file(self, file_path_):
        folder_name = file_path_.split('/')[-2]
        module_folder_path = "/".join(file_path_.split('/')[0:-2]) + "/"
        if folder_name.split('.')[0].split('_')[-1] == 's':
            folder_path = "_".join(folder_name.split('.')[0].split('_')[:-1])
        else:
            folder_path = "_".join(folder_name.split('.')[0].split('_'))
        map_folder_path = module_folder_path + folder_path + ".rim"

        return map_folder_path

    def get_object_coord_on_map(self, file_path_, template_res_ref_):
        import xml.etree.ElementTree as ET

        map_folder_path = self.get_rim_folder_from_file(file_path_)
        map_git_file_path = map_folder_path + tIO.getListOfFilesInSubFolders(map_folder_path, 'git')[0]

        map_git_root = ET.parse(map_git_file_path).getroot()
        coords = tIO.select_in_xml(
            map_git_root,
            ["", "", ""],  # output type : ("") means no attribute type i.e. branch.text
            [[{'type': 'label', 'value': "X"}], [{'type': 'label', 'value': "Y"}], [{'type': 'label', 'value': "Z"}]],
            # conditions on leaf
            [[{'type': 'label', 'value': "TemplateResRef"}, {'type': '', 'value': template_res_ref_}]]
            # no conditions on branch
        )

        return coords

    def get_string_from_strref(self, strref_):
        import xml.etree.ElementTree as ET

        dialog_path = self.getOutputDirPath("extracted") + "dialog.tlk.xml"
        dialog_root = ET.parse(dialog_path).getroot()

        output_leafs = dialog_root.findall("./*[@id='" + strref_ + "']")

        if len(output_leafs) == 0:
            return None

        return output_leafs[0].text

    def get_quests_tags(self):
        import xml.etree.ElementTree as ET

        dlg_files_list = tIO.getListOfFilesInSubFolders(self.getOutputDirPath("extracted"), "dlg")
        quests_list = list()
        for dlg_file in dlg_files_list:
            dialog_root = ET.parse(self.getOutputDirPath("extracted") + dlg_file).getroot()
            new_quests = dialog_root.findall(".//*[@label='Quest']")
            for new_quest in new_quests:
                return new_quest
                print(new_quest.getparent())
                if new_quest.text is not None and new_quest.text not in quests_list:
                    quests_list.append(new_quest.text)

        return quests_list


strref_db = dict()


class dlgReader():

    def __init__(self, dlg_file_path_, parseNow_=True):
        from lxml import etree

        self.dlg_file_path = dlg_file_path_
        self.parse_now = parseNow_

        if self.parse_now:
            self.dlg_file = etree.parse(self.dlg_file_path)

        self.tlk_file_path = str()
        self.tlk_file = None
        self.tlk_strings = dict()

        self.dialog_entries = dict()
        self.dialog_replies = dict()
        self.dialog_starts = dict()

        self.global_adjacency_matrix = None

        self.verbose = False

    # Booleans
    def does_strref_in_dlg_file(self, strref_):

        global strref_db
        buildCache = False
        if self.dlg_file_path not in strref_db:
            buildCache = True
            strref_db[self.dlg_file_path] = list()

        dialog_element_types = list()
        dialog_element_types.append("EntryList")
        dialog_element_types.append("RepliesList")

        if not buildCache:
            return str(strref_) in strref_db[self.dlg_file_path]
        else:
            if not self.parse_now:  # then parse now !
                from lxml import etree
                self.dlg_file = etree.parse(self.dlg_file_path)
            isFound = False
            for dialog_element_type in dialog_element_types:
                for dialog_element in self.dlg_file.xpath(
                        '/gff3/struct/list[@label="' + dialog_element_type + '"]/struct'):
                    strref_db[self.dlg_file_path].append(
                        str(dialog_element.xpath('locstring[@label="Text"]')[0].get('strref')))
                    if str(dialog_element.xpath('locstring[@label="Text"]')[0].get('strref')) == str(strref_):
                        isFound = True
            return isFound

    def get_dialog_entries(self):
        if not self.dialog_entries:
            self.dialog_entries = self.get_dialog_elements_dictionary("EntryList")
        return self.dialog_entries

    def get_dialog_replies(self):
        if not self.dialog_replies:
            self.dialog_replies = self.get_dialog_elements_dictionary("ReplyList")
        return self.dialog_replies

    def get_dialog_starts(self):
        if not self.dialog_starts:
            self.dialog_starts = self.get_dialog_elements_dictionary("StartingList")
        return self.dialog_starts

    def get_dialog_elements_dictionary(self, dialog_element_type_):
        # dialog_type_str_ can be ether EntryList, ReplyList, StartingList
        if self.tlk_file and not self.tlk_strings:
            self.get_all_strings_from_tlk_file()
        next_dialog_element_type = "EntriesList"
        if dialog_element_type_ == "EntryList":
            next_dialog_element_type = "RepliesList"

        dialog_elements = list()
        for dialog_element in self.dlg_file.xpath('/gff3/struct/list[@label="' + dialog_element_type_ + '"]/struct'):
            element_id = int(dialog_element.get("id"))
            dialog_elements.append(dict())
            dialog_elements[-1]["id"] = element_id
            dialog_elements[-1]["next_id_list"] = list()
            if dialog_element_type_ == "StartingList":
                if len(dialog_element.xpath('uint32[@label="Index"]')) > 0:
                    dialog_elements[-1]["next_id_list"].append(dialog_element.xpath('uint32[@label="Index"]')[0].text)
            else:
                dialog_elements[-1]["strref"] = dialog_element.xpath('locstring[@label="Text"]')[0].get('strref')
                if dialog_elements[-1]["strref"] in self.tlk_strings:
                    dialog_elements[-1]["text"] = self.tlk_strings[dialog_elements[-1]["strref"]]
                next_index_list = dialog_element.xpath(
                    'list[@label="' + next_dialog_element_type + '"]/struct/uint32[@label="Index"]')
                for next_index in next_index_list:
                    dialog_elements[-1]["next_id_list"].append(next_index.text)
        return dialog_elements

    def set_tlk_file_path(self, tlk_file_path_):
        from lxml import etree
        self.tlk_file_path = tlk_file_path_
        self.tlk_file = etree.parse(self.tlk_file_path)

    def get_all_strings_from_tlk_file(self):
        if not self.tlk_file:
            raise Exception("tlk file has not been set.")
        if not self.tlk_strings:
            for string_entry in self.tlk_file.xpath("/tlk/string"):
                self.tlk_strings[string_entry.get("id")] = string_entry.text
        return self.tlk_strings

    def define_adjacency_matrix(self):
        if self.global_adjacency_matrix is None:
            import numpy
            matrix_size = 0
            matrix_size += len(self.get_dialog_starts())
            matrix_size += len(self.get_dialog_entries())
            matrix_size += len(self.get_dialog_replies())
            self.global_adjacency_matrix = numpy.zeros(shape=(matrix_size, matrix_size))

    def get_global_adjacency_matrix(self):
        if self.global_adjacency_matrix is None:
            self.define_adjacency_matrix()

        for starting_point in self.dialog_starts:
            start_index = int(starting_point["id"])
            self.dialog_recursive_walk(start_index, self.fill_global_adjacency_matrix)

        return self.global_adjacency_matrix

    def get_global_index(self, dialog_element_type_, element_index_):

        if dialog_element_type_ == "StartingList":
            return int(element_index_)
        elif dialog_element_type_ == "EntryList":
            return len(self.get_dialog_starts()) + int(element_index_)
        elif dialog_element_type_ == "ReplyList":
            return len(self.get_dialog_starts()) + len(self.get_dialog_entries()) + int(element_index_)
        else:
            return -1

    def get_element_type(self, global_index_):

        if int(global_index_) < len(self.get_dialog_starts()):
            return "StartingList"
        elif int(global_index_) < len(self.get_dialog_starts()) + len(self.get_dialog_entries()):
            return "EntryList"
        elif int(global_index_) < len(self.get_dialog_starts()) + len(self.get_dialog_entries()) + len(
                self.get_dialog_replies()):
            return "ReplyList"
        else:
            return ""

    def get_element_index(self, global_index_):

        if global_index_ < len(self.get_dialog_starts()):
            return global_index_
        elif global_index_ < len(self.get_dialog_starts()) + len(self.get_dialog_entries()):
            return global_index_ - len(self.get_dialog_starts())
        elif global_index_ < len(self.get_dialog_starts()) + len(self.get_dialog_entries()) + len(
                self.get_dialog_replies()):
            return global_index_ - len(self.get_dialog_starts()) - len(self.get_dialog_entries())
        else:
            return -1

    def get_dialog_dict(self, element_type_):
        if element_type_ == "StartingList":
            return self.get_dialog_starts()
        elif element_type_ == "EntryList":
            return self.get_dialog_entries()
        elif element_type_ == "ReplyList":
            return self.get_dialog_replies()
        else:
            return dict()

    def get_next_element_type(self, current_element_type_):
        if current_element_type_ == "StartingList" or current_element_type_ == "ReplyList":
            return "EntryList"
        elif current_element_type_ == "EntryList":
            return "ReplyList"
        else:
            return ""

    def fill_global_adjacency_matrix(self, global_index_, next_global_id_):
        break_loop = False
        if self.global_adjacency_matrix is None:
            self.define_adjacency_matrix()
        if self.global_adjacency_matrix[global_index_, next_global_id_] == 0:
            self.global_adjacency_matrix[global_index_, next_global_id_] = 1
        else:
            break_loop = True
        return break_loop

    def dialog_recursive_walk(self, global_index_, action_function_):
        element_type = self.get_element_type(global_index_)
        element_index = self.get_element_index(global_index_)
        next_element_type = self.get_next_element_type(element_type)
        next_ids_list = self.get_dialog_dict(element_type)[element_index]["next_id_list"]
        if self.verbose:
            import inspect
            recursion_depth = len(inspect.stack())
            try:
                print('  ' * recursion_depth + ">", self.get_dialog_dict(element_type)[element_index]['text'])
            except KeyError:
                pass
        for next_id in next_ids_list:
            next_global_id = self.get_global_index(next_element_type, next_id)
            break_loop = action_function_(global_index_, next_global_id)
            if not break_loop:
                self.dialog_recursive_walk(next_global_id, action_function_)

    def get_input_rank_nodes(self):

        # How many other nodes merge into a given node
        input_rank_nodes = list()
        self.get_global_adjacency_matrix()

        for col_index in range(self.global_adjacency_matrix.shape[1]):
            input_rank_nodes.append(dict())

            input_rank_nodes[-1]['global_index'] = col_index
            input_rank_nodes[-1]['type'] = self.get_element_type(col_index)
            input_rank_nodes[-1]['index'] = self.get_element_index(col_index)
            try:
                input_rank_nodes[-1]['strref'] = \
                    self.get_dialog_dict(input_rank_nodes[-1]['type'])[input_rank_nodes[-1]['index']]['strref']
                input_rank_nodes[-1]['text'] = \
                    self.get_dialog_dict(input_rank_nodes[-1]['type'])[input_rank_nodes[-1]['index']]['text']
            except KeyError:
                pass
            input_rank_nodes[-1]['rank'] = 0
            for line_index in range(self.global_adjacency_matrix.shape[0]):
                input_rank_nodes[-1]['rank'] += self.global_adjacency_matrix[line_index, col_index]

        return sorted(input_rank_nodes, key=lambda k: k['rank'], reverse=True)

    def build_matrix_from_index(self, index_):

        import numpy
        matrix_size = 0
        matrix_size += len(self.get_dialog_starts())
        matrix_size += len(self.get_dialog_entries())
        matrix_size += len(self.get_dialog_replies())
        adjacency_matrix = numpy.zeros(shape=(matrix_size, matrix_size))

        self.nb_recurse = 0.

        # self.verbose = True
        def fill_local_matrix(global_index_, next_global_id_):
            break_loop = False
            if adjacency_matrix[global_index_, next_global_id_] == 0:
                self.nb_recurse += 1
                adjacency_matrix[global_index_, next_global_id_] = 1
            else:
                break_loop = True
            return break_loop

        self.dialog_recursive_walk(index_, fill_local_matrix)

        if self.verbose:
            print("number of connections = ", self.nb_recurse)

        return adjacency_matrix

    def get_text_from_global_index(self, global_index_):
        text = ''
        try:
            text = self.get_dialog_dict(self.get_element_type(global_index_))[self.get_element_index(global_index_)][
                'text']
        except KeyError:
            pass
        return text

    ## Conversion tools
    # Global index
    def get_global_index_from_strref(self, strref_):

        for dialog_entry in self.get_dialog_entries():
            try:
                if dialog_entry['strref'] == strref_:
                    return self.get_global_index("EntryList", dialog_entry['id'])
            except KeyError:
                pass

        for dialog_reply in self.get_dialog_replies():
            try:
                if dialog_reply['strref'] == strref_:
                    return self.get_global_index("ReplyList", dialog_reply['id'])
            except KeyError:
                pass

        return -1

    def get_global_index_from_string(self, string_):

        for dialog_start in self.get_dialog_starts():
            try:
                if dialog_start['text'] == string_:
                    return self.get_global_index("StartingList", dialog_start['id'])
            except KeyError:
                pass

        for dialog_entry in self.get_dialog_entries():
            try:
                if dialog_entry['text'] == string_:
                    return self.get_global_index("EntryList", dialog_entry['id'])
            except KeyError:
                pass

        for dialog_reply in self.get_dialog_replies():
            try:
                if dialog_reply['text'] == string_:
                    return self.get_global_index("ReplyList", dialog_reply['id'])
            except KeyError:
                pass

        return -1

    # Graph functions
    def get_color_indexes(self):

        color_indexes = list()
        for global_index in range(self.global_adjacency_matrix.shape[0]):

            index_type = self.get_element_type(global_index)
            if index_type == "StartingList":
                color_indexes.append('red')
            elif index_type == "EntryList":
                color_indexes.append('blue')
            elif index_type == "ReplyList":
                color_indexes.append('green')
            else:
                color_indexes.append('grey')

        return color_indexes

    def get_label_indexes(self):

        label_indexes = list()
        for global_index in range(self.global_adjacency_matrix.shape[0]):
            label_indexes.append(self.get_text_from_global_index(global_index))
        return label_indexes
