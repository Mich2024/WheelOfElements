import os
import re
from CardDefinitions_WheelOfFate import *
import copy
import pandas as pd

def removeLinebreaks(lines):
    res = []
    for line in lines:
        res.append(line.replace("\n",""))
    return res

def removeDoubleQuotes(lines):
    res = []
    for line in lines:
        res.append(line.replace('"',""))
    return res

def removeComments(lines):
    res = []
    for line in lines:
        if not line[0] == "#":
            res.append(line)
    return res

def removeEmptyLines(lines):
    res = []
    for line in lines:
        spacelessLine = removeSpaces(line)
        if not spacelessLine == "":
            res.append(line)
    return res

def addSpacesAfterText(lines):
    res = []
    for line in lines:
        res.append(line.replace('Text:"', 'Text: "'))
    return res

def addSpacesBetweenEmptyText(lines):
    res = []
    for line in lines:
        res.append(line.replace('""', '" "'))
    return res

def removeTrailingSpaces(lines):
    res = []
    for line in lines:
        strippedLine = line.strip()
        res.append(strippedLine)
    return res

def removeMonAIAnnotation(lines):
    res = []
    for line in lines:
        spacelessLine = removeSpaces(line)
        if spacelessLine != "StatsNormal" and spacelessLine != "StatsElite":
            res.append(line)
    return res


def removeSpaces(str):
    return str.replace(" ", "")



def truncateFile(lines):
    res = []
    for line in lines:
        if line == "End Of File":
            return res
        else:
            res.append(line)
    return res

def startsWith(line, word):
    res = False
    if(len(line) > len(word)):
        if line[:len(word)] == word:
            res = True
    return res

def sanitizeLines(lines):
            res = removeComments(lines)
            res = removeLinebreaks(res)
            res = removeEmptyLines(res)
            res = truncateFile(res)
            res = addSpacesAfterText(res)
            print("completed sanitization")
            return res