import argparse
import contextlib
import importlib.util
import io
import unittest
from pathlib import Path
from unittest.mock import patch
spec=importlib.util.spec_from_file_location('framedrop_setup',Path(__file__).resolve().parents[1]/'setup.py')
setup=importlib.util.module_from_spec(spec);spec.loader.exec_module(setup)

class SetupTests(unittest.TestCase):
    def resolve(self,browser='chrome',value=None):
        return setup.resolve_id(argparse.Namespace(browser=browser,id=value),argparse.ArgumentParser())
    def test_interactive_id_prompt(self):
        for browser in ('chrome','edge','chromium'):
            with self.subTest(browser=browser),patch.object(setup.sys.stdin,'isatty',return_value=True),patch('builtins.input',return_value=' '+ 'a'*32+' ') as prompt,contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(self.resolve(browser),'a'*32);prompt.assert_called_once()
    def test_explicit_id_does_not_prompt(self):
        with patch('builtins.input') as prompt:
            self.assertEqual(self.resolve(value='b'*32),'b'*32);prompt.assert_not_called()
    def test_noninteractive_requires_id(self):
        with patch.object(setup.sys.stdin,'isatty',return_value=False),contextlib.redirect_stderr(io.StringIO()) as errors,self.assertRaises(SystemExit):self.resolve()
        self.assertIn('--id YOUR_EXTENSION_ID',errors.getvalue())
    def test_firefox_fixed_id(self):
        with patch('builtins.input') as prompt:
            self.assertEqual(self.resolve('firefox'),setup.FIREFOX_ID);prompt.assert_not_called()
    def test_invalid_ids_before_any_install(self):
        for value in ('','YOUR_EXTENSION_ID','z'*32,'a'*31,'https://example.com'):
            with self.subTest(value=value),patch.object(setup.subprocess,'run') as run,patch.object(setup.venv,'EnvBuilder') as builder,contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):
                try:setup.main(['--browser','chrome','--id',value])
                finally:run.assert_not_called();builder.assert_not_called()
    def test_firefox_rejects_other_id(self):
        with contextlib.redirect_stderr(io.StringIO()),self.assertRaises(SystemExit):self.resolve('firefox','a'*32)
    def test_cancelled_prompt(self):
        with patch.object(setup.sys.stdin,'isatty',return_value=True),patch('builtins.input',side_effect=EOFError),contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()) as errors,self.assertRaises(SystemExit):self.resolve()
        self.assertIn('cancelled before making changes',errors.getvalue())
if __name__=='__main__':unittest.main()
