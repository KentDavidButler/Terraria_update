'''
This Package relies on WMI being installed https://pypi.org/project/WMI/
All actions that may need to be taken envolving the Local Server Running Terraria
- get Version of Terraria server is running
- Check if Terraria is running
- stop Terraria
- start Terraria
- extract zip to correct location
'''
import re
import os
import subprocess
import wmi
import zipfile

path = r"C:\Terraria_update"
server_path = r"C:\Program Files\Terraria"


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def get_latest_installed_version():
    """Returns locally installed version of terraria as int"""
    subdirectories_str = get_immediate_subdirectories(server_path)
    installed_versions = []
    for folder in subdirectories_str:
        if folder.isnumeric():
            installed_versions.append(int(folder))
    return installed_versions[-1]


def get_server_log(server):
    while True:
        line = server.stdout.readline()
        break
    return line


def is_server_running():
    """
    Returns bool if server is running based on
    process running called TerrariaServer.exe
    """
    c = wmi.WMI()
    process_name_list = []

    for process in c.Win32_Process():
        process_name_list.append(process.Name)

    # Terraria should be running and everything should be perfecto!
    if "TerrariaServer.exe" in process_name_list:
        return True

    # Terraria is NOT running! DANGER DANGER!
    return False


def get_latest_downloaded_version():
    only_files = [f for f in os.listdir(path) if os.path.isfile(f)]
    server_files = [sf for sf in only_files if re.findall(r'terraria-server-\d{4}', sf)]
    return server_files[-1]


def extract_zip():
    current_version = get_latest_installed_version()

    zip_file = get_latest_downloaded_version()
    with zipfile.ZipFile(zip_file,"r") as z:
        z.extractall(server_path)
    extracted_version = get_latest_installed_version()
    return extracted_version > current_version


def start_ter_serv(version):
    """ Start running Terraria server by running subprocess.Popen and returns the server subprocess"""
    file_path = server_path + "\\" + str(version) + "\\Windows\\"
    file_name = "TerrariaServer.exe"
    full_file_path = file_path + file_name
    exe_switch = "-config"
    config_path = server_path + "\\config.txt"

    server = subprocess.Popen([full_file_path,
                               exe_switch,
                               config_path],
                              stdout=subprocess.PIPE,
                              stdin=subprocess.PIPE,
                              bufsize=1,
                              text=True,
                              shell=True)

    while server.stdout.readline():
        line = server.stdout.readline()
        print("This is:: %s", line)
        if ("started" or "port") in line:
            break

    return server


def stop_ter_serv(server):
    """using standard input to the subprocess send exit command to the passed in server subprocess"""
    # terminate the subprocess
    server.communicate(input="exit")
