import os
import unittest
import requests
import gzip
from package_statistics import DebPackage


class TestDebPackage(unittest.TestCase):
    def setUp(self) -> None:
        self.url = "http://ftp.uk.debian.org/debian/dists/stable/main/"
        self.stats = DebPackage()
        self.archList = ["amd64", "arm64", "armel"]
        self.randList = [0,"Apple", 1.0, True,False, " ", None]
        return super().setUp()
    
    def tearDown(self) -> None:
        self.stats = None
        return super().tearDown()
    
    def gettestList(self):
        testList = {}
        for arch in self.archList:
            testList[arch] = f"Contents-{arch}.gz"
        return testList         
    
    def test_getContextIndex(self):
        result = self.stats.getContextIndex()
        testList = self.gettestList()
        for arch in self.archList:
            self.assertIsInstance(result, dict)
            self.assertTrue(arch in result)
            self.assertTrue(len(result[arch])>0)
            self.assertTrue(testList[arch] in result[arch])
        

    def test_checkArchValid(self):
        contextIndex = self.stats.getContextIndex()
        for arch in self.archList:
            result = self.stats.checkArchValid(arch, contextIndex)
            self.assertTrue(result)
        
        for rand in self.randList:
            result = self.stats.checkArchValid(rand, contextIndex)
            self.assertFalse(result)

        with self.assertRaises(TypeError):
            self.stats.checkArchValid()
            self.stats.checkArchValid("amd64", 0)



    def test_getInfo(self):
        context = self.stats.getContextIndex()

        for arch in self.archList:
            result = self.stats.getInfo(context[arch][0])
            self.assertIsInstance(result, bytes)

    def test_downloadFile(self):
        testList = self.gettestList()
        for arch in testList:
            if os.path.exists(testList[arch]):
                self.assertFalse(self.stats.downloadFile(testList[arch]))
            else:
                self.assertTrue(self.stats.downloadFile(testList[arch]))

    def test_parseFile(self):
        testList = self.gettestList()
        for arch in testList:
            result = self.stats.parseFile(testList[arch])
            for i in range(1,10):
                self.assertTrue((result[i-1][1] >= result[i][1]))
                self.assertNotEqual(result[i-1][0], result[i][0])
            self.stats.pacList = {}
            
        with self.assertRaises(FileNotFoundError):
            result = self.stats.parseFile("abc")

    def test_clearPack(self):
        pacList = self.stats.clearPack()
        self.assertTrue(pacList == {})

    
if __name__ == "__main__":
    unittest.main()





        