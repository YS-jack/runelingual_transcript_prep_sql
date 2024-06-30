# RuneLingual transcript provider
Follow these steps to create or update the Database needed to run RuneLingual.

## Steps
1. Clone this repository. Make sure the translations on the sql folders are all upto date.
2. Obtain data from Abex's Cache Viewer, save it inside "cache_viewer_files" folder (see [Cache Viewer Data Extraction](#cache-viewer-data-extraction))
3. Run [main.py](main.py). This code will automatically do the following:
    1. reformat data in "cache_viewer_files/cacheData.txt" to json format, and save as "cache_viewer_files/cacheData_formatted.txt"
    2. open "cacheData_formatted.txt", and read it as a json variable. This contains
        - names of items, NPCs, objects
        - examine text of items
        - menu option of items, NPCs, objects
    3. format them into SQL table
    4. fetch missing data from the osrs wiki. This will be 
        - examines for npcs, objects
        - dialogues with NPCs
    2. update the existing SQL data of each language
        - this will only add new items, npcs, e.t.c. to the table, and will not touch any of the exisiting values
4. Open/download the transcript of your language, and start translating! For information on how, ask chatGPT, it always (on topics that have many answers on the Internet) gives good and quick answers, trust me!
5. To publish your changes, reach out to one of the developers, they will do the following.
    1. review the submitted changes, especially if the **number of columns** are correct.
    2. add the files to its language's folder in the **"publish"** directory.
6. By restarting RuneLite, the data should be updated.

## Cache Viewer Data Extraction

This folder contains scripts for extracting item, NPC, and object information from Abex's Cache Viewer 2.

The file "cacheData.txt" will be used for other script, to get the sql table of all data RuneLingaul needs.

### Steps
1. Open and copy the whole code in the file, named [Code to paste to cacheViewer2.txt](cache_viewer_files/code%20to%20paste%20to%20cacheViewer2.txt)

2. Visit [Abex's Cache Viewer 2](https://abextm.github.io/cache2/#/editor).
3. Delete all the code on the left side editor.
4. Paste the code into the left side of the editor tab
5. Press the "run" button and wait for few seconds. The right side of should get filled with lots of words (json like strings).
5. Press "Ctrl + s" (or "save" the file from a button somewhere).
6. Name it "Cache Viewer.html" (this should be the default value) and save it to your local computer.
7. Move the file to [cache_viewer_file](cache_viewer_files/) folder.