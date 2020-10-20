from pyFileFinder import Finder
from pyDataBank.datapack import DataPack
from tkinter import Tk, filedialog
import logging


class DataFiles:
    """The DataFiles class manages resource files thanks to 2 dictionaries (files and fileset), one is a key/value per file
    the other one is a key/value per file set (a group of files).
    The way resource files are retrieved is based on regex. It uses Finder class of pyFileFinder module to do so.
    It is also possible to request the pop up of an open dialog box to select files.    
    """

    def __init__(self, settings: dict):
        r"""constructor: it defines the parent folder where resource files should be searched (except for external files)
        and the it associates key/value pair for resources.
        Parameters
        ----------
        settings: a dictionary with optional keys :
            'dialogs':
                dictionary of (name: dialog box definition), where dialog box definition is the dictionary 
                with the following key/value pairs that pops up  a dialog box to choose a file.
                    'tip': title of the dialog that will pop open to select the file
                    'type': file extension of the searched file to be used in this dialog:
            'files': dictionary with optional keys:
                'parent': parent folder path where resource files should be searched. If none supplied, then parent is the current directory. 
                'depth' : see pyFileFinder Finder class - depth of recursive search in subfolders. Default value is 0
                'caseSensitive': see pyFileFinder Finder class - defines is the file search is case sensitive or not
                'definitions':
                    dictionary of (name: regex), each regex defining a pattern to search for 1 file to be associated with the given name in the resulting files dictionary. 
                    If many files comply with the regex, only the first found file is returned
            'fileset': dictionary with optional keys:
                'parent': parent folder path where resource files should be searched. If none supplied, then parent is the current directory. 
                'depth' : see pyFileFinder Finder class - depth of recursive search in subfolders. Default value is 0
                'caseSensitive': see pyFileFinder Finder class - defines is the file search is case sensitive or not
                'definitions':
                    dictionary of (name: regex), each regex defining a pattern to search for multiple files to be associated with the given name in the resulting fileset dictionary

        the residual keys (others than files, fileset and dialogs) are storeD as it in datapak in the others section

        here are2 examples of settings given as a yml file:
        Example1 - 
        files:
            parent: "C:/folder"
            depth: -1
            caseSensitive: true
            file1: 'fi.*_1\.txt'
            file2: 'file2'
        fileset:
            parent: "C:/folder2"
            depth: 0
            caseSensitive: true
            texts_set: '.*\.txt'
            images_set2: .*\.(jpg|png|tif|tiff)

        Example2 - 
        dialogs:
            images:
                tip: 'provide image file'
                type: 'png'
                set: true           # default value is True
            text:
                tip: 'provide txt file'
                type: 'txt'
                set: false
         """

        self.datapack = DataPack()
        if 'files' in settings:
            self._findFiles(settings.pop('files'))

        if 'fileset' in settings:
            self._findFiles(settings.pop('fileset'), True)

        if 'dialogs' in settings:
            self._getDialogFiles(settings.pop('dialogs'))

        self.datapack.addOtherSettings(settings)

    def generatePack(self):
        """create a DataPack object to easily manipulate the found resource files"""
        return self.datapack

    def _getDialogFiles(self, dialog_settings):
        for name in dialog_settings:
            tip = dialog_settings[name]['tip'] if 'tip' in dialog_settings[name] else 'open'
            filetypes = [('searched files', dialog_settings[name]['type']), ('all files',
                                                                             '.*')] if 'type' in dialog_settings[name] else [('all files', '.*')]
            multiple = dialog_settings[name]['set'] if 'set' in dialog_settings[name] else True
            files = {name: self._openDialog(tip, filetypes, multiple)}
            print('\nfiles', files)
            if multiple:
                self.datapack.addFileSet(files)
            else:
                self.datapack.addFiles(files)

    def _openDialog(self, tip, filetypes, multiple):
        root = Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename(
            title=tip, filetypes=filetypes, multiple=multiple)
        root.destroy()
        return list(filepath) if multiple else filepath

    def _getFiles(self, finder_settings):
        foundfiles = Finder(finder_settings).findFiles()
        return foundfiles

    def _getFile(self, finder_settings):
        files = self._getFiles(finder_settings)
        return files[0] if files else None

    def _findFiles(self, settings, findfileset=False):
        finder_settings = dict()
        if 'parent' in settings:
            finder_settings['parent'] = settings['parent']
        finder_settings['depth'] = settings['depth'] if 'depth' in settings else 0
        finder_settings['caseSensitive'] = settings['caseSensitive'] if 'caseSensitive' in settings else False

        finder_settings['stopWhenFound'] = False if findfileset else True

        files = {}
        for name in settings['definitions']:
            finder_settings['regex'] = settings['definitions'][name]
            found = self._getFiles(
                finder_settings) if findfileset else self._getFile(finder_settings)
            if found is None:
                logging.warning('no file found for regex {}'.format(found))
                continue
            files[name] = found

        if findfileset:
            self.datapack.addFileSet(files)
        else:
            self.datapack.addFiles(files)
