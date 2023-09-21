import os
import logging
import shutil
import random
import filecmp


class FileCreation:
    def setup_method(self, log_file):
        """

        :param log_file: log file name
        :return:
        This method creates log file
        """
        self.log_file = log_file
        logging.basicConfig(filename=self.log_file,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filemode='a')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def dir_creation(self, directory):
        """

        :param directory: directory name
        :return: returns created directory name and path
        This method creates directory by metioned name in curr path
        """
        if not os.path.isdir(directory):
            os.mkdir(directory)
            self.logger.info('Creating directory {}...'.format(directory))
            print('Creating directory {}...'.format(directory))
            dir_created = directory
        else:
            self.logger.debug('Folder "{}" is already present....'.format(directory))
            print('Folder "{}" is already present....'.format(directory))
            dir_created = directory
        path = os.getcwd()
        print(path)

        return dir_created, path

    def file_creation(self, directory, file_name):
        """

        :param directory: directory name
        :param file_name: name of file to be created
        :return: returns created file path
        This method created file in specified path
        """
        file_created = directory + '/' + file_name
        if not os.path.isfile(file_created):
            f = open(file_created, 'w+')
            self.logger.info('Creating file {}...'.format(file_created))
            print('Creating file {}...'.format(file_created))
            return file_created
        else:
            self.logger.debug('File "{}" is already present....'.format(file_created))
            print('File "{}" is already present....'.format(file_created))
            return file_created

    def ingest_data_in_file(self, file_name, dummy_data_file=None):
        """

        :param file_name: name of file
        :param dummy_data_file: dummy data to be ingested
        :return:
        This method ingests dummy data from the dumm_data_file mentioned to file
        """
        if dummy_data_file is None:
            dummy_data_file = 'dummy_data.txt'
        dummy_file = open(dummy_data_file, 'r')

        self.logger.info("Ingesting data from {} to {}".format(dummy_data_file, file_name))
        print("Ingesting data from {} to {}".format(dummy_data_file, file_name))

        f = open(file_name, 'a+')
        for line in dummy_file:
            f.write(line)

        f.close()

    def sync(self, path_a, path_b):
        """

        :param path_a: source path
        :param path_b: destination path
        :return:
        This method syncs 2 folders
        """
        if not path_a or not path_b:
            raise NameError('Required path to both dirs')
        curr_dir = os.getcwd()
        source_path = curr_dir + "\{}".format(path_a)
        replica_path = curr_dir + "\{}".format(path_b)
        os.chmod(source_path, 777)
        os.chmod(replica_path, 777)
        files_in_a = os.listdir(source_path)
        files_in_b = os.listdir(replica_path)

        for file in files_in_b:
            if file not in files_in_a:
                os.remove(replica_path + "\{}".format(file))

        for file_a in files_in_a:
            if len(files_in_b) != 0:
                source = source_path + "\{}".format(file_a)
                replica = replica_path + "\{}".format(file_a)
                if os.path.isfile(source):
                    shutil.copy(source, replica)
                self.logger.info('synchronizing both folders "{}" and "{}"'.format(source_path, replica_path))
                print('synchronizing both folders "{}" and "{}"'.format(source_path, replica_path))
            else:
                f = open(replica_path + '/' + file_a, 'a+')
                source = source_path + "\{}".format(file_a)
                replica = replica_path + "\{}".format(file_a)
                shutil.copy(source, replica)
                self.logger.info('synchronizing both folders "{}" and "{}"'.format(source_path, replica_path))
                print('synchronizing both folders "{}" and "{}"'.format(source_path, replica_path))

    def remove_random_file(self, dir_path):
        """

        :param dir_path: dir path
        :return: retuns name of removed file
        This method removes random file from specified folder
        """
        file_d = random.choice(os.listdir(dir_path))
        os.remove(dir_path + '\{}'.format(file_d))

        print("removing file {}...".format(file_d))
        self.logger.info("removing file {}...".format(file_d))

        return file_d

    def modify_random_file(self, dir_path):
        """

        :param dir_path: directory path
        :return: modified file and path
        This method modifies random file in specified folder
        """
        file_r = random.choice(os.listdir(dir_path))
        file_m = dir_path + '\{}'.format(file_r)
        self.ingest_data_in_file(file_m)

        print("modifying file {} by ingest dummy data...".format(file_m))
        self.logger.info("modifying file {} by ingest dummy data...".format(file_m))

        return file_m, file_r

    def file_comparision(self, s_file, r_file):
        """

        :param s_file: file 1
        :param r_file:  file 2
        :return: boolean
        """
        result = filecmp.cmp(s_file, r_file)
        print("comparing 2 files...")
        self.logger.info("comparing 2 files...")

        return result

    def step(self, comment):
        """

        :param comment: string
        :return:
        This method is to indicate the start of every step
        """
        print("\n")
        print("==================================================================================")
        print("                 STEP '{}'       ".format(comment))
        print("==================================================================================")
        print("\n")
        self.logger.info("\n====================================================================== \n"
                         "           STEP '{}'         \n"
                         "====================================================================== \n".format(comment))

