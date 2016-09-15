import os
import loadDictionary

#loadDictionary.load_dictionary_files()
for path in os.listdir(loadDictionary.DATA_FILES_DIR):

    print(path)
    f = open(loadDictionary.DATA_FILES_DIR + path)
    loadDictionary.load_file_to_database(loadDictionary.DATA_FILES_DIR + path)
    print(f.readline())
    f.close()