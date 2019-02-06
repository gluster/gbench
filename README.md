# Gluster Performance Benchmarking

This git repository is aimed towards providing various Gluster benchmarking
tests and their resultant metrics, across runs, on different HW profiles.

The vision of this project is, to provide metrics and guidelines on Gluster
performance, across workloads and releases, on varying hardware stacks.

The current work is towards providing a set of Gluster performance
tests, that can be replicated on any hardware or Gluster configuration and, to
further provide means to publish test results from these hardware configurations
regularly.

The intention of starting as above, is to kick-off regular regression runs of
Gluster, across various supported release milestones, and to report any
performance regressions in Gluster as the release progresses.

## Using gbench for benchmarking
  - This is WIP code! has a lot of rough edges
  - If you have a setup write your own copy of ./setup-profiles/template/
    - Copy recursively the template directory into a sp-XXXX-XXXX directory
    - Edit each file as appropriate
  - Setup passwordless ssh from the host from where you will run ansible (IOW, gbench from) and the rest of the hosts in your inventory
  - Run from the ansible-playbook-base directory: ansible-playbook -i ../setup-profiles/sp-XXXX-XXXX/secret_inventory.ini ./site.yml -e server_repo="../gluster-sources/your_repo.yml" -e client_repo="../gluster-sources/your_repo.yml" -e vc_definition="../volume-configurations/vc-0000-0010.yml" -e sc_definition="../storage-configurations/sc-0000-0010.yml" -e bt_definition="../bench-tests/bt-0000-0010.yml"
    - secret_inventory.ini is either inventory.ini for your setup or if you have hostnames to keep a secret, then the file that has the hostnames defined
  - The whole ansible playbook currently only works for CentOS and clones!
  - At the end of the run, the following changes would have taken place,
    - IPoIB configuration, i.e if "confibipv4addr" variable is defined
    - Gluster server bits installed on hosts in the "server" group (including required repositories enabled on the box)
    - Gluster client bits installed on hosts in the "client" group (including required repositories enabled on the box)
    - Gluster trusted storage pool created across the hosts in the "servers" group
    - Provided disks to gbench cleaned up and made ready for volume configuration
    - Provided volume created as per configuration, on a set of disks provided
    - Specified tests run on the said volume and results available in /tmp

## Workflow details

NOTE: This is the current workflow, as we add/clone various aspects of the
workflow we would be able to tune it better. IOW, we learn as we go/grow.

### Elements in the workflow
  * Bench Test (BT)
    * This is a benchmark test, usually denoted as BT#, where # is the test
    number
  * Volume Configuration (VC)
    * This is a volume configuration definition, denoted as VC#
  * Storage Configuration (SC)
    * This defines how the storage on the nodes should be configured
  * Gluster Source (GS)
    * A GS is a defnition pointing to the needed gluster bits (RPMs or otherwise)
  * Setup Profile (SP)
    * This is a setup profile, that lists the hosts. The specification is
    expanded to include disks and other needed items (to be defined).
  * Test Results (TR)
    * These are the raw outputs of the test results, denoted as TR#
  * Monitors
    * This is currently a place holder for capturing monitoring information
    across any test
    * This is a TODO item and is mostly not discussed at the moment

### A typical workflow

A logical view of workflow progression is summarized as follows,

BT# =-(run against)--> VC# =-(created using)--> GS# =-(with storage)--> SC# =-(deployed on)---> SP#

The workflow, is the reverse of this selection, i.e it sets up the SP before
moving onto deploying the GS and so on, till finally executing the BT.

Once BT# is executed, the results are expected to be stashed and submitted
back to this repository as a TR#.

### Example (or, how to execute a workflow)

Assuming a setup is available for testing, and there is a client machine (ansible-client) that can execute the ansible for gbench, a typical workflow would look as follows.

All work is carried on in ansible-client host (assumed to be CentOS in this example)

1) Prepare sources and dependencies for Ansible
    - `cd <workdir>`
    - `git clone https://github.com/gluster/gbench.git`
    - `git clone https://github.com/gluster/gdeploy.git`
    - `ln -s ../../gdeploy/modules ./gbench/ansible-playbook-base/`
    - `yum install epel-release`
    - `yum install ansible` (2.5 or greater) (epel on CentOS7 brings in > 2.6)

2) Setting up SSH key trust for inventory hosts:
    - Remove any older keys to inventory hosts under test: `ssh-keygen -R <hostnam/IP>` (optional)
    - Fetch and add current keys of inventory hosts to known_hosts: `ssh-keyscan <hostname/IP> >> ~/.ssh/known_hosts`

3) Setting up passwordless SSH from ansible-client to all hosts in the inventory:
    - `ssh-keygen`
    - Add/Append generated public key to authorized keys on all hosts in the inventory

4) Running the tests
    i. `cd <workdir>/gbench/ansible-playbook-base/`

    ii. Setup the hosts: `ansible-playbook -i ../setup-profiles/sp-0000-0010/secret_inventory.ini ./site.yml --tags "preparehosts"`

    iii. Install gluster bits: `ansible-playbook -i ../setup-profiles/sp-0000-0010/secret_inventory.ini ./site.yml --tags "glinstall" -e server_repo="../gluster-sources/nightly.yml" -e client_repo="../gluster-sources/nightly.yml"`

    iv. Create a volume: `ansible-playbook -i ../setup-profiles/sp-0000-0010/secret_inventory.ini ./site.yml --tags "createvolume" -e vc_definition="../volume-configurations/vc-dist-arbiter-2-3.yml" -e sc_definition="../storage-configurations/sc-0000-0010.yml"`
    NOTE: Will delete older volume and create a new one for test

    v. Run a test: `ansible-playbook -i ../setup-profiles/sp-0000-0010/secret_inventory.ini ./site.yml --tags "runtests" -e bt_definition="../bench-tests/bt-0000-0002-smallfile.yml"`
  NOTE: Tests store their results in /tmp/ on the ansible-client host and should be collected post the test run is completed, for analysis

5) Looping over tests across configurations
    - To repeat a different test on the same volume, run step (v) above with a different bench-test
    - To create a different volume type on the same setup and gluster bits, repeat step (iv) above, and usually step (v) to repeat the tests as well on the new volume
    - Ideally to repeat a test on new gluster sources, step (iii) should be repeated, but this is not supported yet

6) Parsing test results
    - A simple JSON output parser for smallfile and fio output is present in parsers/SimpleParser.py that can help generate a simple IOPS or files/sec and time of test output in CSV format
    - A script to look at each test output and pass it to the above parser can help generate a CSV output for each test

## Repository Structure

**TODO** This is an initial structure for the repository, and is not yet
created as such. It would be done once we have some elements for each and the
workflow is sane enough to carry this structure.

```
.
├── bench-tests
│   ├── bt-###
│   ├── bt-001
│   │   ├── README.md
│   │   └── test.py
│   └── bt-002
├── gluster-sources
│   ├── gs-###
│   ├── gs-001
│   └── gs-002
├── monitors
├── setup-profiles
│   ├── sp-###
│   ├── sp-001
│   │   ├── profile.yaml
│   │   └── README.md
│   └── sp-002
├── test-results
│   ├── sp-###
│   └── sp-001
│       ├── gs-001
│       └── gs-002
│           └── vc-002
│               └── bt-001
│                   ├── tr-###
│                   ├── tr-001
│                   └── tr-002
└── volume-configurations
    ├── vc-###
    ├── vc-001
    │   ├── README.md
    │   └── volume-configuration.yaml
    └── vc-002
```


## Submitting results back to the repository

**TODO** Pull requests to this repo?

## How to submit a new SP/GS/VC/BT (or the development details)

**TODO** Does this fit here or redirect to devl doc?

## Reaching out for questions, improvements, participation or anything

**TODO** Thoughts are gluster-devel and github itself as forums.
