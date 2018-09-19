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

**TODO** Does this fit here or redirect to another file in the repo (like doc)

## Repository Structure

**TODO** This is an elementry structure for the repository, and is not yet
created as such. It would be done once we have some elements for each and the
workflow is sane enough to carry this structure.

```
.
├── bench-tests
│   ├── bt-###
│   ├── bt-001
│   │   ├── README.md
│   │   └── test.py
│   └── bt-002
├── gluster-sources
│   ├── gs-###
│   ├── gs-001
│   └── gs-002
├── monitors
├── setup-profiles
│   ├── sp-###
│   ├── sp-001
│   │   ├── profile.yaml
│   │   └── README.md
│   └── sp-002
├── test-results
│   ├── sp-###
│   └── sp-001
│       ├── gs-001
│       └── gs-002
│           └── vc-002
│               └── bt-001
│                   ├── tr-###
│                   ├── tr-001
│                   └── tr-002
└── volume-configurations
    ├── vc-###
    ├── vc-001
    │   ├── README.md
    │   └── volume-configuration.yaml
    └── vc-002
```


## Submitting results back to the repository

**TODO** Pull requests to this repo?

## How to submit a new SP/GS/VC/BT (or the development details)

**TODO** Does this fit here or redirect to devl doc?

## Reaching out for questions, improvements, participation or anything

**TODO** Thoughts are gluster-devel and github itself as forums.
