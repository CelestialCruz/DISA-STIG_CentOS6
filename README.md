# DISA-STIG_CentOS6
Installation and deployment instructions for DISA_STIG playbook

#Notes for people wanting to use this playbook
  - Make sure you know your AWS secret keys and other AWS information as it will be necessary when making adjustment on the script.  
  - Anything in brackets in the README.md are values that depend on your setup.
  - The STIG_Config role is derived from the AnsibleLockdown repository created by Sam Doran. You can look at the original role here:
    https://github.com/ansible/ansible-lockdown
  - When for instructions about how to edit the STOG_Config role, please see the readme there.
  - There are several STIG rules that I need to adjust for CentOS6 as they will generate an error and fail the script if invoked. This is     a long process and will be updated as deemed necessary.

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

https://cloud.githubusercontent.com/assets/20823757/20454468/cc84eee2-ae0f-11e6-96ea-cb0198400353.png

- Edit the "main.yml" file located in /roles/OpenSCAP/tasks/ and adjust the email information to match who you want to recieve the report.   *Do is optional and the script will not fail, nor will it inhibit generating the report in anyway if you ignore that task.

- Finally, run the playbook

           ansible-playbook -vv -i localhost, -e "type=webservers" project.yml -v

#After running the playbook
