from paramiko import SSHClient, AutoAddPolicy
import os

wdir=r'C:\Users\varun\Documents\Capstone\Data'
rdir=r'/home/pi/Data/'

client = SSHClient()
#LOAD HOST KEYS
#client.load_host_keys('~/.ssh/known_hosts')
client.load_host_keys('C:/Users/varun/.ssh/known_hosts')
client.load_system_host_keys()

#Known_host policy
client.set_missing_host_key_policy(AutoAddPolicy())

#client.connect('10.1.1.92', username='root', password='password1')
client.connect('raspberrypi.local', username='pi',password='3953')

sftp=client.open_sftp()
remote_dir=sftp.listdir(rdir)

for index, file in enumerate(remote_dir):
    if not os.path.exists(file):
        file_name=remote_dir[index]
        if not os.path.exists(file):
            print(wdir)
            sftp.get(rdir+file_name,wdir+"\\"+file_name)

# Close the client itself
sftp.close()
client.close()