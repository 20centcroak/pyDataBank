# pyDataIP
Import data and format it using a pipeline

## DataFiles class
The DataFiles class manages resource files thanks to 2 dictionaries (files and fileset), one is a key/value per file, 
the other one is a key/value per file set (a list of files)

The way resource files are retrieved is based on regex. It uses Finder class of [pyFileFinder](https://pypi.org/project/pyFileFinder/) module to do so.

It loads the file content into pandas DataFrames.

An example of use of this class is shown below:

    resources = DataFiles(parent_folder_path, datafiles_settings)
    resources.generateDataPack(dataprocessing)

an example of datafiles_settings in yml format is shown below:

    files:
        file1: ^.*_1_\.txt$
        file2: ^.*_2\.txt$
        file3: ^.*_3\.txt$
    externalfiles:
        my_ext_file: 
            type: '.xlsx'
            tip: open xls file
    fileset:
        globalpattern: global.*\.jp.*g$
            

The resulting loaded resources due to the "files" section will be:
- file1 (for example file_1.txt)
- file2 (for example myfile_2.txt)
- file3 (for example anotherFile_3.txt)

Concerning the external file an open dialog window will be displayed and only files with extension .xlsx will be shown inside.
When the user has chosen its file, then my_ext_file is defined.
If there is no need to display an open dialog box, we could replace the externalfiles section with:

    externalfiles:
        my_ext_file: 
          ref: myExcelFile.*\.xlsx$
          in: 'C:\work'

Finally the fileset section loads a list of files based on a regex (all files that comply and are part of the parent folder (with defined depth for subfolders)) will be loaded.
In the example, the following files could have been loaded:
- globalFile.jpg
- globalRendering.jpeg
- globalOutlook.jpg

generateDataPack method returns a DataPack object. DataPack and dataprocessing will be discussed in the next section.

## DataPack class
The DataPack class manages data to be used in the app by offering basic methods to manipulate and format data. It makes use of pandas to do so.
It defines a pipeline starting with the resource on which a sequence of processings are applied.
It is then possible to chain processings by applying an operation on output data

A DataPack object may be built either by calling :

    pack = Datapack(files, dataprocessing)

or by calling the generateDataPack method of the DataFiles class (see above), files are then the ones loaded when creating the DataFiles object

- "files" settings is a dictionary. Key is the file name used by dataprocessing to apply operation on the given file and value is the pathname of this file. The files are either csv or xls files
- "dataprocessing" is the operation name and parametersto apply to the resource file. 

dataprocessing examples: 

    # dataframe processing loads the resource file (file1 here) in a DataFrame taking into account the given parameters (see pandas for more information on parameters)
    # the result is sored in output variable (here data1)
    processing: dataframe
    output: data1
    parameters:
        sep: '\s+' 
        skip: 1 
        file: file1

    # split processing splits the data in n columns. The result is a DataFrame
    processing: split
    output: table1
    parameters:
        cols: 2
        data: data1

    # replaceValues processing searches a value ("search") and replace by another ("replace)
    processing: replaceValues
    output: data2
    parameters:
        data: data2
        search: "YES"
        replace: X

    # fillna processing replace NaN values with "fillwith"
    processing: fillna
    output: data2
    parameters:
        data: data2
        fillwith: ""

    # get filename (basename of resource file)
    processing: filename
    output: file1name
    parameters:
        file: file1

    processing: format
    output: data2
    parameters:
        data: data2
        regex: (^.+-[0-9]+)