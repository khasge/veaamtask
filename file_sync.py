from sync_lib import *
from getopt import getopt

import sys
import time

"""
Author  : Akshata khasge
File    : file_sync.py
Command : python file_sync.py  --source_dir/-s <source dir name> --replica_dir/-r <replica dir name> --time_interval/-t <sync_int> --log_file/-l <log_file_name>
          Example: python file_sync.py  --source_file 'sourcedir' -r 'replicadir' -t 1 -l 'test_logs.log' 

Description : 
1. Create 2 folders (source and replica)
2. create files in source folder
3. ingest dummy data in all the files in source data
4. sync 2 folders
5. Perform different file operation like delete file, modify files and sync 2 folder
6. Periodically sync folder every given sync_interval time

"""


class FileSync(FileCreation):
    def setup_function(self):
        cli_opts, args = getopt(sys.argv[1:], 's:r:l:t:', ['source_dir=', 'replica_dir=', 'log_file=', 'time_interval='])
        print(cli_opts)
        for cli_option, argument in cli_opts:
            if cli_option == '-s' or cli_option == '--source_dir':
                self.source_dir = argument
            if cli_option == '-r' or cli_option == '--replica_dir':
                self.replica_dir = argument
            if cli_option == '-l' or cli_option == '--log_file':
                self.log_file = argument
            if cli_option == '-t' or cli_option == '--time_interval':
                self.sync_interval = int(argument)


        if not self.log_file:
            self.log_file = 'test_logs.log'
        if not self.sync_interval:
            self.sync_interval = 60
        if not self.source_dir:
            self.source_dir = 'source'
        if not self.replica_dir:
            self.replica_dir = 'replica'

        FileCreation.setup_method(self, self.log_file)
        self.dummy_data_file = 'dummy_data.txt'
        self.file_name = 'data.txt'
        self.no_of_files = random.choice(range(3, 10))

    def test_file_sync(self):
        self.step("1. Source Folder creation")
        self.source_dir, source_path = self.dir_creation(self.source_dir)

        self.step("2. Source File creation")
        self.source_files = []
        for n in range(self.no_of_files):
            self.file_names = self.file_name + '_' + str(n)
            self.source_file = self.file_creation(self.source_dir, self.file_names)
            self.source_files.append(self.source_file)

        self.step("3. Ingest data in source file")
        for self.source_file in self.source_files:
            self.ingest_data_in_file(self.source_file)

        self.step("4. Replica Folder creation")
        self.replica_dir, replica_path = self.dir_creation(self.replica_dir)

        self.step("5. File Sync")
        self.sync(self.source_dir, self.replica_dir)

        self.step("6. remove file from source folder")
        folder_path = source_path + '\{}'.format(self.source_dir)
        file_deleted = self.remove_random_file(folder_path)
        print(file_deleted)

        self.step("7. sync folders")
        self.sync(self.source_dir, self.replica_dir)

        self.step("8. modify files in source folder")
        file_m_path, file_modified = self.modify_random_file(folder_path)

        self.step("9. compare  files")
        file_c_path = replica_path + '\{}\{}'.format(self.replica_dir, file_modified)
        result = self.file_comparision(file_m_path, file_c_path)
        if not result:
            self.logger.info("sync folders if files are not same")
            self.sync(self.source_dir, self.replica_dir)

        time.sleep(30)

        result = self.file_comparision(file_m_path, file_c_path)
        print(result)

        self.step("10. periodically sync the folders every 3 min")
        while True:
            self.sync(self.source_dir, self.replica_dir)
            time.sleep(180)


if __name__ == '__main__':
    filesync = FileSync()
    filesync.setup_function()
    filesync.test_file_sync()
