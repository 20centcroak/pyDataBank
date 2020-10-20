import os
import logging


class DataPack:
    """DataPack is a container for 2 types of data: file paths and fileset paths.
    It manages 2 dictionaries.
    The first one is {name: path} with name as a short name for the file and path the file path
    The second one is {name: [paths]} with name as a short name for the fileset and [paths] the list of file paths
    Then it allows calling files by their shortname or get a list of all files referenced in the 2 dictionaries."""

    def __init__(self, files: dict = None, fileset: dict = None, others: dict = None):
        self._files = files if files else dict()
        self._fileset = fileset if fileset else dict()
        self._others = others if others else dict()

    def addFiles(self, files):
        """add files in DataPack.
        ----------
        parameters
        - files: either a single path to the file or a dictionary {name: path} or a list of path
        when not a dictionary, then the key is the file basename without extension
        if a key already exist in the files dictioanry, a subscript is applied
        """

        if type(files) is dict:
            for name in files:
                self._files[self._getUniqueName(
                    name, self._files)] = files[name]
            return

        files = [files] if type(files) is not list else files
        for file in files:
            name = os.path.splitext(os.path.basename(file))[0]
            self._files[self._getUniqueName(name, self._files)] = files[name]

    def addFileSet(self, fileset):
        """add fileset in DataPack.
        ----------
        parameters
        - fileset: either a list of file paths or a dictionary {name: list of file paths} 
        when not a dictionary, then the key is "fileset" or "fileset_n" with n as increment to avoid overwriting
        """
        if type(fileset) is dict:
            for name in fileset:
                self._fileset[self._getUniqueName(
                    name, self._fileset)] = fileset[name]
            return

        self._fileset[self._getUniqueName('fileset', self._fileset)] = fileset

    def addOtherSettings(self, others: dict):
        self._others = {**self._others, **others}

    def getFileDict(self):
        """ return the files dictionary"""
        return self._files

    def getFilesetDict(self):
        """return the fileset dictionnary"""
        return self._fileset

    def getOthers(self):
        """ return the others dictionary"""
        return self._others

    def getFileList(self):
        """"return the list of all files (files and fileset)"""
        return [*self._files.values()] + [items for fileset in self._fileset.values() for items in fileset]

    def _getUniqueName(self, name, filedict):
        return name if name not in self._files else self._findName(name, filedict)

    def _findName(self, name, filedict):
        index = 0
        unique_name = '{}_{}'.format(name, index)
        while unique_name in filedict:
            index += 1
            unique_name = '{}_{}'.format(name, index)
        return unique_name
