import unittest
from unittest.mock import patch,MagicMock
import arguments as arg
import tempfile
import os
class TestParseArguments(unittest.TestCase):
    def test_parse_arguments(self):
        program="pptx2video.py"
        correct_input_path ="/root/work/example/sample.ppt"
        correct_output_path="/root/work/example/"
        with patch("sys.argv",[program,correct_input_path,correct_output_path]):
            args = arg.parse()
            self.assertEqual(args.input,correct_input_path)
            self.assertEqual(args.output,correct_output_path)
            self.assertEqual(args.transition,2)
            self.assertEqual(args.debug,False)
            self.assertEqual(args.width,1270)
            self.assertEqual(args.height,720)
            self.assertEqual(args.density,144)
            self.assertEqual(args.tempdir,"")
            
        with patch("sys.argv",[program,correct_input_path,correct_output_path,"-t","4"]):
            args = arg.parse()
            self.assertEqual(args.input,correct_input_path)
            self.assertEqual(args.output,correct_output_path)
            self.assertEqual(args.transition,4)
            self.assertEqual(args.debug,False)
            self.assertEqual(args.width,1270)
            self.assertEqual(args.height,720)
            self.assertEqual(args.density,144)
            self.assertEqual(args.tempdir,"")
        with patch("sys.argv",[program,correct_input_path,correct_output_path,"--transition","4"]):
            args = arg.parse()
            self.assertEqual(args.input,correct_input_path)
            self.assertEqual(args.output,correct_output_path)
            self.assertEqual(args.transition,4)
            self.assertEqual(args.debug,False)
            self.assertEqual(args.width,1270)
            self.assertEqual(args.height,720)
            self.assertEqual(args.density,144)
            self.assertEqual(args.tempdir,"")
        with patch("sys.argv",[program,correct_input_path,correct_output_path,"--transition","4","-d"]):
            args = arg.parse()
            self.assertEqual(args.input,correct_input_path)
            self.assertEqual(args.output,correct_output_path)
            self.assertEqual(args.transition,4)
            self.assertEqual(args.debug,True)
            self.assertEqual(args.width,1270)
            self.assertEqual(args.height,720)
            self.assertEqual(args.density,144)
            self.assertEqual(args.tempdir,"")
        with patch("sys.argv",[program,correct_input_path,correct_output_path,"--transition","4","--debug"]):
            args = arg.parse()
            self.assertEqual(args.input,correct_input_path)
            self.assertEqual(args.output,correct_output_path)
            self.assertEqual(args.transition,4)
            self.assertEqual(args.debug,True)
            self.assertEqual(args.width,1270)
            self.assertEqual(args.height,720)
            self.assertEqual(args.density,144)
            self.assertEqual(args.tempdir,"")
        with patch("sys.argv",[program,correct_input_path,correct_output_path,"--width","100"]):
            args = arg.parse()
            self.assertEqual(args.input,correct_input_path)
            self.assertEqual(args.output,correct_output_path)
            self.assertEqual(args.transition,2)
            self.assertEqual(args.debug,False)
            self.assertEqual(args.width,100)
            self.assertEqual(args.height,720)            
            self.assertEqual(args.density,144)
            self.assertEqual(args.tempdir,"")
        with patch("sys.argv",[program,correct_input_path,correct_output_path,"--width","100","--height","200"]):
            args = arg.parse()
            self.assertEqual(args.input,correct_input_path)
            self.assertEqual(args.output,correct_output_path)
            self.assertEqual(args.transition,2)
            self.assertEqual(args.debug,False)
            self.assertEqual(args.width,100)
            self.assertEqual(args.height,200)
            self.assertEqual(args.density,144)
            self.assertEqual(args.tempdir,"")
        with patch("sys.argv",[program,correct_input_path,correct_output_path,"--width","100","--height","200","--density","256"]):
            args = arg.parse()
            self.assertEqual(args.input,correct_input_path)
            self.assertEqual(args.output,correct_output_path)
            self.assertEqual(args.transition,2)
            self.assertEqual(args.debug,False)
            self.assertEqual(args.width,100)
            self.assertEqual(args.height,200)
            self.assertEqual(args.density,256)
            self.assertEqual(args.tempdir,"")
        with patch("sys.argv",[program,correct_input_path,correct_output_path,"--width","100","--height","200","--density","256","--tempdir","/root/src/example"]):
            args = arg.parse()
            self.assertEqual(args.input,correct_input_path)
            self.assertEqual(args.output,correct_output_path)
            self.assertEqual(args.transition,2)
            self.assertEqual(args.debug,False)
            self.assertEqual(args.width,100)
            self.assertEqual(args.height,200)
            self.assertEqual(args.density,256)
            self.assertEqual(args.tempdir,"/root/src/example")
        with patch("sys.argv",[program,correct_input_path,correct_output_path,"--debug"]):
            args = arg.parse()
            self.assertEqual(args.input,correct_input_path)
            self.assertEqual(args.output,correct_output_path)
            self.assertEqual(args.transition,2)
            self.assertEqual(args.debug,True)
            self.assertEqual(args.width,1270)
            self.assertEqual(args.height,720)
            self.assertEqual(args.density,144)
            self.assertEqual(args.tempdir,"")

    def test_parse_arguments_fail(self):
        with patch("sys.argv",["pptx2video.py"]):
            with self.assertRaises(SystemExit):
                arg.parse()
        with patch("sys.argv",["pptx2video.py","/root/work/example/sample.ppt"]):
            with self.assertRaises(SystemExit):
                arg.parse()
        with patch("sys.argv",["pptx2video.py","/root/work/example/sample.ppt","/root/work/example/","1"]):
            with self.assertRaises(SystemExit):
                arg.parse()

    def test_check_arguments1(self):
        args = MagicMock(
            input="/root/src/example/sample.pptx",
            output="/root/src/example/sample.mp4",
            transition= 4,
            debug=True,
            width=1270,
            height=720,
            density=144,
            tempdir=""
            )
        setting = arg.check(args)
        self.assertEqual(args.input,setting.get("input"))
        self.assertEqual(args.output,setting.get("output"))
        self.assertEqual(args.transition,setting.get("transition"))
        self.assertEqual(args.debug,setting.get("debug"))
        self.assertEqual(args.width,setting.get("width"))
        self.assertEqual(args.height,setting.get("height"))
        self.assertEqual(args.density,setting.get("density"))

        args = MagicMock(
            input="/root/src/example/sample.pptx",
            output="/root/src/example/",
            transition= 0,
            debug=True,
            width=1270,
            height=720,
            density=144,
            tempdir=""
            )
        setting = arg.check(args)
        self.assertEqual(args.input,setting.get("input"))
        self.assertEqual(args.output+"sample.mp4",setting.get("output"))
        self.assertEqual(args.transition,setting.get("transition"))
        self.assertEqual(args.debug,setting.get("debug"))
        self.assertEqual(args.width,setting.get("width"))
        self.assertEqual(args.height,setting.get("height"))
        self.assertEqual(args.density,setting.get("density"))

    def test_check_arguments_fail(self):
        args = MagicMock(
            input="/root/src/example/test_sample.pptx",
            output="/root/src/example/",
            transition= 4,
            debug=True,
            width=1270,
            height=720,
            density=144,
            tempdir=""
            )
        setting = arg.check(args)
        self.assertEqual(setting,False)
        args = MagicMock(
            input="/root/src/example/sample.pptx",
            output="/root/src/example/",
            transition= -1,
            debug=True,
            width=1270,
            height=720,
            density=144,
            tempdir=""
            )
        setting = arg.check(args)
        self.assertEqual(setting,False)        
        args = MagicMock(
            input="/root/src/example/sample.pptx",
            output="",
            transition= 0,
            debug=False,
            width=1270,
            height=720,
            density=144,
            tempdir=""
            )
        setting = arg.check(args)
        self.assertEqual(setting,False)

