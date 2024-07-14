import json
import unittest
from parse_html import parseFromLink

class test_output_json(unittest.TestCase):

    def test_van_gogh(self):
        self.checkJson('files/van-gogh-paintings.html', 'paintings')

    def test_jessica_pratt(self):
        self.checkJson('files/jessica-pratt-related.html', 'related people')

    def test_haruki_murakami(self):
        self.checkJson('files/haruki-murakami-related.html', 'related people')

    def checkJson(self, url, outputArrName):

        #Parse the HTML file
        parseFromLink(url, outputArrName)

        #Open the solution array it generated
        with open('files/output-array.json', 'r') as file:
            data = json.load(file)

        #Retrieve value from the outputArrName
        artworks = data[outputArrName]

        #Make sure outputArrName is an array and is not empty
        self.assertIsInstance(artworks, list, "Output should be an array")
        self.assertGreater(len(artworks), 0, "Output array should not be empty")

        #Check each in the outputArr
        for index, artwork in enumerate(artworks):

            #Make sure the name is populated as a string and not empty
            self.assertIsInstance(artworks[index]["name"], str, "Name should be a string")
            self.assertNotEqual(artworks[index]["name"], "", "Name should not be empty")

            #Extensions does not necessarily need to exist, but if it does make sure its an array that is not empty
            if "extensions" in artworks[index]:
                self.assertIsInstance(artworks[index]["extensions"], list, "Extensions should be an array")
                self.assertGreater(len(artworks[index]["extensions"]), 0, "Extensions should not be empty")

            #The link should always be populated and have a non empty str value 
            self.assertIsInstance(artworks[index]["link"], str, "Link should be a string")
            self.assertNotEqual(artworks[index]["link"], "", "Link should not be empty")

            #Image should always be populated, but it can have a string or none
            self.assertTrue(isinstance(artworks[index]["image"], str) or artworks[index]["image"] is None, "Image should be a string or nonetype")

if __name__ == "__main__":
    unittest.main()


#RESOURCES
#https://docs.python.org/3/library/unittest.html