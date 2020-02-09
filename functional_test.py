import unittest
import bencode


# Test the exceptions
class TestExceptions(unittest.TestCase):
    def test(self):
        self.assertRaises(bencode.UnsupportedDataTypeException, bencode.encode, 1.2)


# Test the functionality of the encoding
class TestEncoding(unittest.TestCase):
    def test(self):
        cases = [                                                               # A sample input list:
            0,                                                                  # A zero
            123,                                                                # A sample integer
            "abc",                                                              # A sample string
            [],                                                                 # An empty list
            [1, 2, 3, 4, 5],                                                    # A sample simple list
            ["led light", "elderly", "del montieee"],                           # Text with control letters
            ['January', 2, {"march": "APRIL"}, ["May", "June", "July", -8]],    # A sample complex list
            {},                                                                 # An empty dictionary
            {1: "a", 2: "b", 3: "c"},                                           # A sample simple dictionary
            {11: "x", 22: "y", 33: "z", 44: {0: [-1, 2, -3]}}                   # A sample complex dictionary
            ]

        codes = [                                                               # The expected results_encode list:
            "i0e",                                                              # for the zero
            "i123e",                                                            # for the sample integer
            "3:abc",                                                            # for the sample string
            "le",                                                               # for the empty list
            "li1ei2ei3ei4ei5ee",                                                # for the sample simple list
            "l9:led light7:elderly12:del montieeee",                            # for the text with control letters
            "l7:Januaryi2ed5:march5:APRILel3:May4:June4:Julyi-8eee",            # for the sample complex list
            "de",                                                               # for the empty dictionary
            "di1e1:ai2e1:bi3e1:ce",                                             # for the sample simple dictionary
            "di11e1:xi22e1:yi33e1:zi44edi0eli-1ei2ei-3eeee"                     # for the sample complex dictionary
            ]

        results_en = []
        results_de = []
        for index in range(0, len(cases)):
            result_en = bencode.encode(cases[index])
            result_de = bencode.decode(codes[index])
            results_en.append(result_en)
            results_de.append(result_de)
            print("---")
            print("Given Input:   " + cases[index].__repr__())
            print("Given Code:    " + codes[index].__repr__())
            print("Result Code:   " + results_en[index].__repr__())
            print("Result Decode: " + results_de[index].__repr__())
            assert codes[index].__eq__(results_en[index])
            assert cases[index].__eq__(results_de[index])


if __name__ == '__main__':
    unittest.main()
