#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


class CmdLineReader:
    def __init__(self):
        self.optionsBuffer = dict()
        self.keepTailArgs = False
        self.trailArgList = list()

    def addOption(self, optionName_, callList_, description_="", nbExpectedArgs_=-1, possibleValueList_=None,
                  isMandatory_=False):
        if possibleValueList_ is None: possibleValueList_ = list()
        if optionName_ in self.optionsBuffer: raise ValueError(optionName_ + " already in options list.")
        if len(callList_) == 0: raise ValueError("Empty call list")

        self.optionsBuffer[optionName_] = dict()
        self.optionsBuffer[optionName_]["calls"] = callList_
        self.optionsBuffer[optionName_]["description"] = description_
        self.optionsBuffer[optionName_]["nArgs"] = nbExpectedArgs_
        self.optionsBuffer[optionName_]["possibleValues"] = possibleValueList_
        self.optionsBuffer[optionName_]["isMandatory"] = isMandatory_

        self.optionsBuffer[optionName_]["values"] = list()
        self.optionsBuffer[optionName_]["isTriggered"] = False

    def printConfigSummary(self):
        print("Keeping trailing args? " + str(self.keepTailArgs))
        for name, option in self.optionsBuffer.items():
            print("Option: \"" + name + "\": " + str(option["calls"]) + " " + str(option["description"]) + " -> " + str(
                option["possibleValues"]))

    def printTriggerArgs(self):
        print("Triggered options are:")
        for name, option in self.optionsBuffer.items():
            if option["isTriggered"]:
                if option["nArgs"] == 0:
                    print("\"" + name + "\": True")
                else:
                    print("\"" + name + "\": " + str(self.getOptionValues(name)))

    def readCommandLineArgs(self):
        lastOptionName = None
        for arg in sys.argv:

            if len(self.trailArgList) != 0:
                self.trailArgList.append(arg)
                continue

            if lastOptionName != "":  # when lastOptionName == "", catching the tail args
                argIsOption = False
                for name, option in self.optionsBuffer.items():
                    if argIsOption: break
                    for call in option["calls"]:
                        if argIsOption: break
                        if arg == call:
                            lastOptionName = name
                            argIsOption = True
                if argIsOption: continue

            if lastOptionName is not None:
                if 0 < self.optionsBuffer[lastOptionName]["nArgs"] <= len(self.optionsBuffer[lastOptionName]["values"]):
                    if not self.keepTailArgs:
                        raise ValueError("Too many options provided")
                    else:
                        print("Tail catcher triggered...")
                        self.trailArgList.append(arg)
                        lastOptionName = ""
                        continue

                if len(self.optionsBuffer[lastOptionName]["possibleValues"]) != 0:
                    if arg not in self.optionsBuffer[lastOptionName]["possibleValues"]:
                        raise ValueError(arg + " not in " + str(self.optionsBuffer[lastOptionName]["possibleValues"]))

                self.optionsBuffer[lastOptionName]["isTriggered"] = True
                self.optionsBuffer[lastOptionName]["values"].append(arg)
                continue

        for name, option in self.optionsBuffer.items():
            if option["isMandatory"] and not option["isTriggered"]:
                raise ValueError(name + " option not triggered.")

    def isOptionTriggered(self, optionName_):
        return self.optionsBuffer[optionName_]["isTriggered"]

    def getOptionValues(self, optionName_):
        return self.optionsBuffer[optionName_]["values"]

    def getOptionValue(self, optionName_, default_):
        if optionName_ in self.optionsBuffer:
            default_ = self.optionsBuffer[optionName_]["values"]
        return default_
