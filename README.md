# pyDataIP
Import resource files by selecting them one by one or in a batch with regex or with open dialog window
Associate these files or filesets to a key for an easy call
The residual keys (others than files, fileset and dialogs) are stored as it in datapak in the others section

An example of use of both classes is shown below:

    resources = DataFiles(datafiles_settings)
    datapack = resources.generateDataPack()
    files_as_dict = datapack.getFileDict()
    fileset_as_dict = datapack.getFilesetDict()
    all_files_as_list = datapack.getFileList()
    others = datapack.getOthers()


Where two examples of datafiles_settings given as a yml file are shown below:

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
        mykey1: myvalue1
        mykey2:
           - item1
           - item2
            
The resulting loaded resources due to the "files" section could be:

    files_as_dict = {'file1': 'path/to/file_1.txt', 'file2': 'path/to/myfile2.txt}
    fileset_as_dict = {'texts_set': ['mydoc.txt'], 'images_set2': ['image1.png', 'image2.jpg']}

The "others" section of databank in example 2 would be:
    others = {'mykey1' : 'myvalue1', 'mykey2': ['item1', 'item2']}

And the dialogs settings pops open a dialog box which creates a fileset for 'image' and a file dictionary for 'text'

## DataFiles class
The DataFiles class manages resource files thanks to 2 dictionaries (files and fileset), one is a key/value per file, 
the other one is a key/value per file set (a group of files)

The way resource files are retrieved is based on regex. It uses Finder class of [pyFileFinder](https://pypi.org/project/pyFileFinder/) module to do so.
It is also possible to request the pop up of an open dialog box to select files. 


generateDataPack method returns a DataPack object. DataPack will be discussed in the next section.

See more example in the [test class](https://github.com/20centcroak/pyDataBank/blob/main/tests/unit/test_datafiles.py)

## DataPack class
The DataPack class is a container for 2 types of data: file paths and fileset paths.
    It manages 2 dictionaries.
    The first one is {name: path} with name as a short name for the file and path the file path
    The second one is {name: [paths]} with name as a short name for the fileset and [paths] the list of file paths
    Then it allows calling files by their shortname or get a list of all files referenced in the 2 dictionaries.

It offers convenient methods to 
- add files or filesets with or without a short name for these resources. A unique short name is always given to added resources.
- get files, fileset or the list of all files either contained in files or in fileset