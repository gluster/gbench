# All about setup profiles

## About

This directory holds various setups and their details.

## Details regarding what a setup profile should contain

- Refer to the file [inventory.ini](./template/inventory.ini) in the template directory for more information
- Further, refer to the [all](./template/group_vars/all) variables file for variable related information

## How to add a new setup profile

- Choose the next available index 'sp-xxxx-xxxx' (try and increment in 10's)
- Create the directory for your setup profile
- Recursively copy the template directory into your setup profile directory
- Create additional server<n>/client<m> directories as required by your setup
  profile (or remove the extras)
- Edit the following files as required,
  - inventory.ini
  - secret_inventory.ini
  - group_vars/all
  - group_vars/[server|client]<n>/public
  - group_vars/[server|client]<n>/secret
- To verify if your setup profile definition is complete. (TODO)
  - Run: ansible-playbook -i setup-profiles/sp-xxxx-xxxx/inventory.ini setup-profiles/ansible-playbook-test/test.yml
    OR
    Run: ansible-playbook -i setup-profiles/sp-xxxx-xxxx/secret_inventory.ini setup-profiles/ansible-playbook-test/test.yml
    (if your inventory host names are secret and you have a secret copy of the
    inventory with the real host names named secret_inventory.ini)
