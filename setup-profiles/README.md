# All about setup profiles

## About

This directory holds various setups and their details. <add why it is used>

## How to add a new setup profile

- Choose the next avilable index 'sp-xxxx-xxxx' (try and increment in 10's)
- Create the directory for your setup profile
- Recursively copy the template directory into your setup profile directory
- Create additional server<n>/client<m> directories as required by your setup profile
- Edit all information that needs to be public or can be public in the copied template
- Stash all secret files as needed
- Run: ansible-playbook -i setup-profiles/sp-xxxx-xxxx/inventory.ini setup-profiles/ansible-playbook-test/test.yml
  OR
  Run: ansible-playbook -i setup-profiles/sp-xxxx-xxxx/secret_inventory.ini setup-profiles/ansible-playbook-test/test.yml
  (if your inventory hostnames are secret and you have a secret copy of the inventory with the real hostnames named secret_inventory.ini)
  To verify if your setup profile definition is complete.
