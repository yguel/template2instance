#! /usr/bin/python3
import unittest

from template2instance import *
 
class TestMatchingFileMethods(unittest.TestCase):

    def test_ends_with_template_suffix(self):
        res,name = file_ends_with_template_suffix("toto.template","")
        self.assertTrue(res)
        self.assertEqual("toto",name)
        res,name = file_ends_with_template_suffix("toto","")
        self.assertFalse(res)
        res,name = file_ends_with_template_suffix( "toto_template.txt", "" )
        self.assertFalse(res)
        res,name = file_ends_with_template_suffix( "toto_template", "" )
        self.assertFalse(res)
        res,name = file_ends_with_template_suffix( "toto.template.txt", "" )
        self.assertFalse(res)
        res,name = file_ends_with_template_suffix( ".template", "" )
        self.assertFalse(res)
 
    def test_template_before_suffix_or_ends_with_template_suffix(self):
        res,name = file_has_template_before_suffix_or_ends_with_template_suffix( "toto_template.txt", "" )
        self.assertFalse(res)
        res,name = file_has_template_before_suffix_or_ends_with_template_suffix( "toto.template.txt", "" )
        self.assertTrue(res)
        self.assertEqual("toto.txt",name)
        res,name = file_has_template_before_suffix_or_ends_with_template_suffix("toto.template","")
        self.assertTrue(res)
        self.assertEqual("toto",name)
        res,name = file_has_template_before_suffix_or_ends_with_template_suffix(".template", "" )
        self.assertFalse(res)
 
    
 
if __name__ == '__main__':
    unittest.main()