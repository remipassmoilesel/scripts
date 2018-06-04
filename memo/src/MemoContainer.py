# -*- coding: utf-8 -*-
import re

from MemoElement import *


# TODO:
# - Make persistence happen on demand, on write() call

class MemoContainer:

    def __init__(self):
        self.memoList = []

    def createEmptyStorage(self):
        with open(self.path, "a") as inFile:
            inFile.write(os.linesep)
            inFile.close()
            Logger.info("File have been created at: " + self.path)

    def loadStorageFile(self, path):
        self.path = path
        if not os.path.isfile(self.path):
            Logger.warning("Memo file does not exist ...")
            self.createEmptyStorage()

        with open(self.path, "r") as inFile:
            lines = inFile.readlines()
            self.loadTextLines(lines)

    def loadTextLines(self, lines):
        self.memoList = self.parseLines(lines)

    def parseLines(self, lines):

        lines.append(Configuration.MEMO_HEADER_MARK + " Fake header")
        memoList = []

        category = ""
        header = ""
        content = ""

        headerRegex = "^ *" + Configuration.MEMO_HEADER_MARK + " *(?:(.+)" + Configuration.MEMO_CATEGORY_MARK + ")? *(.+)"

        for lineNumber, line in enumerate(lines):
            matcher = re.match(headerRegex, line)

            # this line is a memo header
            if matcher:

                if content and category:
                    memoList.append(MemoElement(header.strip(), content.strip(), category.strip(), lineNumber))

                groups = matcher.groups()
                category = (groups[0] if groups[0] is not None else Configuration.DEFAULT_CATEGORY)
                header = groups[1]

                content = ""

            # this line is part of memo content
            elif re.search("\\w+", line):
                content += line

        return memoList

    def searchByKeywords(self, keywords, categoryFilter=None):

        result = []

        regexPartsArray = []
        for word in keywords:
            wordWithoutSpecialChars = re.sub("[^a-z0-9-]", ".?", word, re.IGNORECASE)
            regexPartsArray.append(wordWithoutSpecialChars)

        separatorPattern = "[-_\s]+"
        regexArray = [
            "^" + (separatorPattern + "|" + separatorPattern).join(regexPartsArray) + separatorPattern,
            separatorPattern + (separatorPattern + "|" + separatorPattern).join(regexPartsArray) + separatorPattern,
        ]

        for memo in self.memoList:

            if categoryFilter and memo.getCategory() != categoryFilter:
                continue

            for regex in regexArray:
                matchHeader = re.search(regex, memo.getHeader(), re.IGNORECASE)
                matchCategory = re.search(regex, memo.getCategory(), re.IGNORECASE)

                contentLines = memo.getContent().split('\n')
                matchContent = False

                for line in range(0, len(contentLines)):
                    matchContent = re.search(regex, contentLines[line], re.IGNORECASE)
                    if matchContent:
                        break

                if matchHeader or matchContent or matchCategory:
                    result.append(memo)
                    break

        return result

    def getById(self, id):
        for memo in self.memoList:
            if int(memo.id) == int(id):
                return memo

        return None

    def getMemoList(self, categoryFilter=None):
        if not categoryFilter:
            return self.memoList

        else:
            result = []
            for memo in self.memoList:
                if memo.getCategory() == categoryFilter:
                    result.append(memo)

            return result

    def updateMemo(self, memoToUpdate):
        for index, memo in enumerate(self.memoList):
            if memo.id == memoToUpdate.id:
                self.memoList[index] = memoToUpdate
                break

    def persistToStorage(self):
        with open(self.path, "w") as storageFile:
            for memo in self.memoList:
                storageFile.writelines(memo.getWritableRepresentation())
            storageFile.close()

    def deleteMemo(self, memo):
        memoReadFile = open(self.path, "r")
        fileLines = memoReadFile.readlines()
        memoReadFile.close()

        # first, delete memo content
        i = memo.lineNumber
        end = False
        while end != True and i < len(fileLines):
            if re.search("\\w+", fileLines[i]):
                del fileLines[i]
            else:
                end = True

        # then delete blank lines
        end = False
        while end != True and i < len(fileLines):
            if re.search("^\\s*$", fileLines[i]):
                del fileLines[i]
            else:
                end = True

        memoWriteFile = open(self.path, "w")
        memoWriteFile.writelines(fileLines)
        memoWriteFile.close()

    def appendMemo(self, memo):
        try:
            inFile = open(self.path, "a")
            inFile.write(memo.getWritableRepresentation())
            inFile.close()
            return True
        except Exception as e:
            Logger.debug(e)
            return False