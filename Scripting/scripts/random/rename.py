import os,glob

path = r"C:\Users\Y Javeed\Downloads\Una Brands\Script_test"
os.chdir(path)

cred_file_name = ["tsm_sg","tsm_my","juju_my","example"]

os.chdir(path)
for i in range(len(cred_file_name)):
    files = filter(os.path.isfile, os.listdir(path))
    files = [os.path.join(path, f) for f in files]  # add path to each file
    files.sort(key=lambda x: os.path.getmtime(x))
    newest_file = files[-1]
    os.rename(newest_file, cred_file_name[i])
    newest_file = files[-1]
    print(newest_file)  
    os.remove(path + '..\\geckodriver')

