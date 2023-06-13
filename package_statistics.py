#!/usr/bin/env python3
import os
import sys
import requests
import gzip
from bs4 import BeautifulSoup
import time


class DebPackage:
    """
    This class is used to download the compressed Contents and parse the file /
    and output the statistics of the top 10 packages that have the most files /
    associated with them.
    """
    def __init__(self) -> None:
        self.url = "http://ftp.uk.debian.org/debian/dists/stable/main/"
        #self.contextIndex = self.getContextIndex()
        self.pacList = {}
    
    def checkArchValid(self, arch: str, contextIndex: dict):
        """
        This function is check whether the input architecture is valid.
        """
        if arch in contextIndex:
            return True
        else:
            return False
        
    def getContextIndex(self):
        """
        This function classifies "Contents indices" by architecture /
        and returns dictionary.
        key: architecture
        value: "Contents indices"
        """
        ContextList = {}
        res = requests.get(self.url)
        res = BeautifulSoup(res.text, "html.parser")
        links = res.find_all("a")
        for link in links:
            href = link.get("href")
            if href.split("-")[0] == "Contents":
                arch = href.split("-")[-1].split(".")[0]
                if arch not in ContextList:
                    ContextList[arch] = []
                ContextList[arch].append(href)
            
        return ContextList
    

    def getInfo(self, file: str):
        """
        Fetch the content from a particular resource.
        """
        downloadURL = self.url+file
        Info = (requests.get(downloadURL).content)
        return Info
    
    def downloadFile(self, file: str):
        """
        Download the compressed file
        """
        if not os.path.exists(file):
            Info = self.getInfo(file)
            with open(file, 'wb') as file:
                file.write(Info)
                print(f"{file} is successfully downloaded!")
            return True
        else:
            print(f"{file} exists!")
            return False


    def parseFile(self, file: str):
        """
        Build the dictionary that record the package_name /
        and the files associated with it.
        key: package_name
        value: number of files
        """
        Info = gzip.open(file,'rt')   
        self.parseFirstLine(next(Info))
        for line in Info:
            self.parseLine(line)
        Info.close()
        self.pacList = sorted(self.pacList.items(), key=lambda x:x[1], reverse=True)
        return self.pacList


    def parseLine(self, line):
        """
        Parse one line in the file. 
        Adds 1 on "number of files" that corresponds to package_name.
        """
        line = line.split()
        if len(line) >= 2:
            for package in line[1:]:
                package_name = package.split("/")[-1]
                if package_name in self.pacList:
                    self.pacList[package_name] += 1
                else:
                    self.pacList[package_name] = 1
        
    def parseFirstLine(self, line):
        """
        This function determines if the first line is useful and
        adds 1 on "number of files" that corresponds to package_name.
        """
        line = line.split()
        if len(line) >= 2:
            if line[0] != "EMPTY_PACKAGE":
                for package in line[1:]:
                    package_name = package.split("/")[-1]
                    self.pacList[package_name] = 1
        
    def clearPack(self):
        """
        Clear pacList
        """
        self.pacList = {}
        return self.pacList
         

if __name__ == "__main__":
    start = time.time()

    stats = DebPackage()
    contextIndex = stats.getContextIndex()
    if stats.checkArchValid(sys.argv[1], contextIndex) == True:
        #gzFile = stats.contextIndex[sys.argv[1]]
        gzFile = contextIndex[sys.argv[1]]
        for file in gzFile:
            stats.downloadFile(file)
            pacList = stats.parseFile(file)
            print(file)
            ptr = 0
            dash = '-'*80
            print(dash)
            print('{:<10s}{:<50s}{:>20s}'.format("#", "Package_Name", "Files_Counts"))
            print(dash)
            while (ptr<10 and ptr<len(pacList)):
                print('{:<10s}{:<50s}{:>20s}'.format(
                "{}.".format(ptr+1),  pacList[ptr][0],  str(pacList[ptr][1])))
                ptr += 1
            stats.clearPack()
             
    else:
        print(" There is no matching architecture! ")
    end = time.time()

    Exec_time = end-start
    hour = int(Exec_time // 3600)
    minute = int((Exec_time%3600) // 60)
    sec = int(Exec_time % 60)

    print("Execution time: {}hours {}mins {}seconds".format(hour, minute, sec))








