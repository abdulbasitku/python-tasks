# TASK 1 - Abdul Basit
# To Upload and Download Files on FTP

import os
import ftplib
from datetime import datetime
from multiprocessing import dummy as multithreading


def uploadfile(file_name, file_local_path, atempt, start_time):
    try:
        print("Start Uploading - " + file_name + " - Attempt # " + str(atempt))

        ftp = ftplib.FTP( host='speedtest.tele2.net', user='anonymous', passwd='anonymous@domain.com')
        ftp.cwd("/upload")
    
        file_handle = open(file_local_path,'rb')
    
        ftp.storbinary('STOR %s'%file_local_path, fp = file_handle)

        file_handle.close()
        ftp.quit()
        end_time = datetime.now()
        time_taken = end_time - start_time

        print('File - ' + file_name + ' - Uploaded in attempt # ' + str(atempt) + ' - Took ' + str(time_taken.total_seconds()) + ' seconds')
    except Exception as ex:
        print(ex)
        uploadfile(file_name, file_local_path, atempt+1, start_time)


def downloadfile(file_name, atempt, start_time):
    try:
        print("Start Downloading - " + file_name + " - Attempt # " + str(atempt))
        ftp = ftplib.FTP( host='speedtest.tele2.net', user='anonymous', passwd='anonymous@domain.com')
        ftp.cwd("/")
        target_local_path = os.path.basename(file_name)

        file_handle = open(target_local_path,'wb')
        ftp.retrbinary('RETR %s'%file_name, file_handle.write)

        file_handle.close()
        ftp.quit()

        end_time = datetime.now()
        time_taken = end_time - start_time

        print('File - ' + file_name + ' - Downloaded in attempt # ' + str(atempt) + ' - Took ' + str(time_taken.total_seconds()) + ' seconds')
    except Exception as ex:
        print(ex)
        downloadfile(file_name, atempt + 1, start_time)


def startuploading():
    files = [f for f in os.listdir('./ForUpload') if os.path.isfile(os.path.join('./ForUpload', f))]
    pool = multithreading.Pool(len(files))
    curr_dir = os.path.dirname(os.path.realpath('__file__'))

    for file_name in files:
        file_local_path = os.path.join(curr_dir, 'ForUpload\\' + file_name)
        pool.apply_async(uploadfile, args=(file_name, file_local_path, 1, datetime.now(), ))

    pool.close()
    pool.join()
    print("Uploading Done")


def startdownloading():
    ftp = ftplib.FTP( host='speedtest.tele2.net', user='anonymous', passwd='anonymous@domain.com')
    ftp.cwd("/")
    file_match = '*KB.zip'
    files = ftp.nlst(file_match)
    #files = ftp.nlst()
    
    pool = multithreading.Pool(len(files))

    for file_name in files:
        pool.apply_async(downloadfile, args=(file_name, 1, datetime.now(), ))

    pool.close()
    pool.join()
    print("Downloading Done")


input_value = input("Press U for Uploading OR press D for Downloading FTP Files?")
if input_value.lower() == "u":
    startuploading()
if input_value.lower() == "d":
    startdownloading()
