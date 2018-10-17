# TASK 2 - Abdul Basit
# To Upload and Download Files on SFTP

import os
import paramiko
from datetime import datetime
from multiprocessing import dummy as multithreading

host = "demo.wftpserver.com"
port = 2222


def uploadfile(file_local_path, file_name, atempt, start_time):
    try:
        print("Start Uploading - " + file_name + " - Attempt # " + str(atempt))
        destination_remote_path = 'upload\\' + file_name

        transport = paramiko.Transport((host, port))
        transport.connect(username="demo-user", password="demo-user")
        sftp = paramiko.SFTPClient.from_transport(transport)

        sftp.put(file_local_path, destination_remote_path)
        sftp.close()
        end_time = datetime.now()
        time_taken = end_time - start_time

        print('File - ' + file_name + ' - Uploaded in attempt # ' + str(atempt) + ' - Took ' + str(time_taken.total_seconds()) + ' seconds')
    except Exception as ex:
        print(ex)
        uploadfile(file_local_path, file_name, atempt + 1)


def downloadfile(file_name, source_remote_path, atempt, start_time):
    try:
        print("Start Downloading - " + file_name + " - Attempt # " + str(atempt))
        target_local_path = os.path.basename(file_name)

        transport = paramiko.Transport((host, port))
        transport.connect(username="demo-user", password="demo-user")
        sftp = paramiko.SFTPClient.from_transport(transport)

        sftp.get(source_remote_path, target_local_path)
        sftp.close()

        end_time = datetime.now()
        time_taken = end_time - start_time

        print('File - ' + file_name + ' - Downloaded in attempt # ' + str(atempt) + ' - Took ' + str(time_taken.total_seconds()) + ' seconds')
    except Exception as ex:
        print(ex)
        downloadfile(file_name, atempt + 1, start_time)


def startuploading():
    files = [f for f in os.listdir('./ForUpload') if os.path.isfile(os.path.join('./ForUpload', f))]
    pool = multithreading.Pool(len(files))
    current_dir = os.path.dirname(os.path.realpath('__file__'))

    for file_name in files:
        file_local_path = os.path.join(current_dir, 'ForUpload\\' + file_name)
        pool.apply_async(uploadfile, args=(file_local_path, file_name, 1, datetime.now(), ))

    pool.close()
    pool.join()
    print("Uploading Done")


def startdownloading():
    transport = paramiko.Transport((host, port))
    transport.connect(username="demo-user", password="demo-user")
    sftp = paramiko.SFTPClient.from_transport(transport)

    files = sftp.listdir('download')
    sftp.chdir('download')
    curr_work_dir = sftp.getcwd()
    sftp.close()
    pool = multithreading.Pool(len(files))

    for file_name in files:
        pool.apply_async(downloadfile, args=(file_name, curr_work_dir + '/' + file_name, 1, datetime.now(), ))

    pool.close()
    pool.join()
    print("Downloading Done")


input_value = input("Press U for Uploading OR press D for Downloading files from SFTP?")
if input_value.lower() == "u":
    startuploading()
if input_value.lower() == "d":
    startdownloading()
