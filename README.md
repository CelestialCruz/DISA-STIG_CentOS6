# DISA-STIG_CentOS6
Installation and deployment instructions for DISA_STIG playbook

#Notes for people wanting to use this playbook
  - Make sure you know your AWS secret keys and other AWS information as it will be necessary when making adjustment on the script.  
  - Anything in brackets in the README.md are values that depend on your setup.
  - The STIG_Config roles is derived from the AnsibleLockdown repository created by Sam Doran. You can look at the original role here:
    https://github.com/ansible/ansible-lockdown

#Ansible basics for CentOS7
- Install and update ansible;

           yum -y install epel-release

           yum -y update

           yum -y install ansible

- Verify the installation and version

           ansible --version
           
  https://cloud.githubusercontent.com/assets/20823757/17412055/c6f4fb7c-5a48-11e6-82b9-e1a6f6635c44.PNG
  
- Generate key on your Ansible machine.
  *Accept defaults and leave passphrase empty for now.

           ssh-keygen -t rsa

  https://cloud.githubusercontent.com/assets/20823757/17412058/c95e7ffa-5a48-11e6-801a-bf2ccac1e753.PNG

- Next we need to send out the key to every webhost and database  on the network.

           ssh-copy-id root@[10.10.2.112]
  
  https://cloud.githubusercontent.com/assets/20823757/17412056/c8019ba6-5a48-11e6-826a-a432ac4928af.PNG
  
# Install and use git to download playbook
- Install git on your Ansible machine

           yum -y install git

- Download git repository into local directory

           git clone https://github.com/CelestialCruz/DISA-STIG_CentOS6.git

# Use playbook
- Head into the "DISA-STIG_CentOS6" directory

- Edit the "aws_environment" file and fill in the AWS Access and Secret key that corresponds to your account.

- Edit the "webservers.yml" file and match each parameter to a value that corresponds to your AWS environment. This file is referenced in the Commission role.

https://cloud.githubusercontent.com/assets/20823757/17723147/b80f3bce-6405-11e6-8455-fe3dc015ea1e.png

- Finally, run the playbook

           ansible-playbook -i hosts project.yml

#After running the playbook
