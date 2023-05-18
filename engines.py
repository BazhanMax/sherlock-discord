import discord
from discord import app_commands
import sys
import os
import configparser
from threading import Thread
import threading
import asyncio
import queue
from abc import abstractclassmethod

patchToFile = os.path.dirname(os.path.abspath(__file__))


class BaseClass:
    def splitResultsLinksMsg(self, results_list):
        results_for_msg = ""
        msg_lists = []
        for i, link in enumerate(results_list, start=1):
            prev = results_for_msg
            if len(results_for_msg) < 1930:
                results_for_msg += "\n" + f"[{i}] > {link}"
            else:
                results_for_msg = ""
                msg_lists.append(prev)
        msg_lists.append(results_for_msg)
        return msg_lists

    @abstractclassmethod
    def Search(self):
        pass

    @abstractclassmethod
    def getStatus(self):
        pass

    @abstractclassmethod
    def getResultsList(self):
        pass

    @abstractclassmethod
    def getResultsMsgs(self):
        pass

    def saveResults(self, foundBy, user, listToSave):
        if not os.path.isdir(f"{patchToFile}/{foundBy}"):
            os.mkdir(f"{patchToFile}/{foundBy}")

        if os.path.isfile(f"{patchToFile}/{foundBy}/{user}.txt"):
            os.remove(f"{patchToFile}/{foundBy}/{user}.txt")
        else:
            with open(
                f"{patchToFile}/{foundBy}/{user}.txt", "x", encoding="utf-8"
            ) as file:
                file.write(
                    f"{user} found at {len(listToSave)} sites by {foundBy}" + "\n"
                )

                for link in listToSave:
                    file.write(link + "\n")

    @abstractclassmethod
    def getResultsFile(self):
        pass
