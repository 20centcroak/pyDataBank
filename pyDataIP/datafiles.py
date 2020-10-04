from dddd.files import Finder
from pyDataIP.datapack import DataPack
from tkinter import Tk, filedialog
import logging


class DataFiles:
    """The DataFiles class manages resource files thanks to 2 dictionaries (files and fileset), one is a key/value per file
    the other one is a key/value per file set (a list of files)
    The way resource files are retrieved is based on regex. It uses Finder class to do so.
    """

    def __init__(self, parent: str, settings: dict, depth=0, caseSensitive=False):
        """
        constructor: it defines the parent folder where resource files should be searched (except ofr external files).
        and the it associates key/value pair for resources.
        Parameters
        ----------
        parent: parent folder path where resource files should be searched
        settings: a dictionary with optional keys :
            'files': list of name: regex, each regex defining a pattern to search for 1 file to be associated with the given name in the resulting files dictionary
            'fileset': list of name: regex, each regex defining a pattern to search for multiple files to be associated with the given name in the resulting fileset dictionary
            'externalfiles': list of name: parameters to search for files outside the parent folder. The files are added to the 'files' dictionary. The parameters may contain either:
                - 'ref': regex = regex to defining a pattern to search for 1 file to be associated with the given name in the resulting files dictionary
                - 'in': the parent folder where to search for a file
                or
                - 'tip': title of the dialog that will pop open to select the file
                - 'type': file extension of the searched file to bu used in this dialog
         """

        finder_settings = {'parent': parent,
                           'depth': depth, 'caseSensitive': caseSensitive}

        self.files = dict()
        if 'files' in settings:
            for name in settings['files']:
                finder_settings['regex'] = settings['files'][name]
                self.files[name] = self._getFile(finder_settings)
                logging.info('file {} found'.format(self.files[name]))

        self.fileset = dict()
        if 'fileset' in settings:
            for name in settings['fileset']:
                finder_settings['regex'] = settings['fileset'][name]
                self.fileset[name] = self._getFiles(finder_settings)
                logging.info('fileset: {}'.format(self.fileset[name]))

        if 'externalfiles' in settings:
            for name in settings['externalfiles']:
                parameters = settings['externalfiles'][name]
                if 'ref' not in parameters:
                    tip = parameters['tip'] if 'tip' in parameters else 'open'
                    filetypes = [
                        ('searched files', parameters['type']), ('all files', '.*')]
                    self.files[name] = self._openDialog(
                        filetypes=filetypes, title=tip)
                    logging.info('file {} selected'.format(self.files[name]))
                else:
                    finder_settings['parent'] = ['in']
                    finder_settings['regex'] = parameters['ref']
                    self.files[name] = self._getFile(finder_settings)
                    logging.info('file {} found'.format(self.files[name]))

    def _openDialog(self, title='open', filetypes=None):
        root = Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename(title=title, filetypes=filetypes)
        root.destroy()
        return filepath

    def _getFiles(self, finder_settings):
        foundfiles = Finder(finder_settings).findFiles()
        if not foundfiles:
            raise ValueError('no file found in {} with regex {}'.format(
                finder_settings['parent'], finder_settings['regex']))
        return foundfiles

    def _getFile(self, finder_settings):
        return self._getFiles(finder_settings)[0]

    def generateDataPack(self, dataprocessing: dict):
        """
        generate a DataPack thanks to these file resources and the processing to be played on them.
        Parameters
        --------------------
        dataprocessing: description of the processings to be applied to the resource files.
        """
        count = 0
        files = dict()
        for key, value in self.fileset.items():
            self.files[key+str(count)] = value
            count += 1
        return DataPack(dict(self.files, **files), dataprocessing)
