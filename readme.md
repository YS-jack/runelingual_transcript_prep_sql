# RuneLingual English transcript provider
Follow these steps to create or update the Database needed to run RuneLingual.

## Steps
1. Clone this repository. 
2. If trying to add new data that is **not** included in the wiki/chisel database, create or add it to existing TSV (tab separated values) files in [./manual_data](./manual_data/), . The data included in the wiki/chisel are:
    - Name, exmaine, option of items, npcs, objects
    - Dialogues/Overhead texts with npcs and pets
    - Level up messages

    so anything else other than the ones above should be included in any TSV files in [manual_data](./manual_data/).
    - when creating a new TSV file, the first line should be column names, then from 2nd line write the data you wish to add. (see already existing TSV files, or reach out on discord)

3. Delete the existing [transcript.db](./transcript.db).
4. Run [main.py](main.py). This code will create 'transcript.db', and automatically add the following data to it.

    - Data from the osrs wiki and chisel, which content are listed above
    - All data inside all TSV files in './manual_data' folder

All data in English should have been added to [transcript.db](./transcript.db). To view its content, download SQL viewer such as [SQLite browser](https://sqlitebrowser.org).


## Cache Viewer Data Extraction

Some of the info not on the wiki/chisel exists on [Abex's Cache Viewer 2](https://abextm.github.io/cache2/#/viewer).

It might be a good idea to look here before writing them up manually.

Some useful info includes:
- location names (enum 252, 595, 1264, 2096, dbtable 64, 13)
- slayer mobs (enum 693, different from npc names)
- slayer rewards (enum 834, 835)
- activity (enum 848)
- emote (enum 1000)
- varrock museum (1741, 1743, 1744)
- task names (enum 3497)
- quest names, rewards (dbtable 0)
- hair style (dbtable 37)
- beard style (dbtable 38)
- music, its unlock location (dbtable 44)