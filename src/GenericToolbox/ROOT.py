#!/usr/bin/env python
# -*- coding: utf-8 -*-


def do_tfile_is_clean(input_tfile_path_, object_name_list_required_presence_=list(), look_for_valid_histograms_ = False):
    from ROOT import gErrorIgnoreLevel, kFatal, gROOT
    from ROOT import TFile, TH1, TH2, TH3
    from ROOT import nullptr

    old_verbosity = gErrorIgnoreLevel
    gROOT.ProcessLine("gErrorIgnoreLevel = " + str(kFatal) + ";")

    input_tfile = TFile.Open(input_tfile_path_, "READ")
    is_junk = False

    try:
        if input_tfile is None:
            is_junk = True
        elif input_tfile.IsZombie() or input_tfile.TestBit(TFile.kRecovered):
            is_junk = True
        else:
            for i_object in range(len(object_name_list_required_presence_)):
                object_handler = input_tfile.Get(object_name_list_required_presence_[i_object])
                if object_handler is None or object_handler == nullptr:
                    is_junk = True
                elif look_for_valid_histograms_:
                    try:
                        if not object_handler.InheritsFrom("TH1") and not object_handler.InheritsFrom("TH2") and not object_handler.InheritsFrom("TH3"):
                            is_junk = True
                        elif object_handler.GetMaximum() < object_handler.GetMinimum():
                            is_junk = True
                    except TypeError:
                        is_junk = True

                try:
                    object_handler.GetTitle()
                except ReferenceError:
                    is_junk = True

                if is_junk:
                    break
            input_tfile.Close()
    except ReferenceError:
        is_junk = True

    gROOT.ProcessLine("gErrorIgnoreLevel = " + str(old_verbosity) + ";")
    return not is_junk


def mkdir_cd_rootfile(root_file_, folder_path_):
    from ROOT import AddressOf

    try:
        AddressOf(root_file_.GetDirectory(folder_path_))
    except ValueError:
        root_file_.mkdir(folder_path_)

    root_file_.cd(folder_path_)
    return root_file_.GetDirectory(folder_path_)


def save_command_line_in_tfile(output_tfile_, command_line_):
    from ROOT import TNamed
    from ROOT import gDirectory

    current_directory = gDirectory
    mkdir_cd_rootfile(output_tfile_, "")
    TNamed("command_line_TNamed", command_line_).Write()
    current_directory.cd()
