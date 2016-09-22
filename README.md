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

## Workflow details

NOTE: This is the current workflow, as we add/clone various aspects of the
workflow we would be able to tune it better. IOW, we learn as we go/grow.

### Elements in the workflow
  * Bench Test (BT)
    * This is a benchmark test, usually denoted as BT#, where # is the test
    number
  * Volume Configuration (VC)
    * This is a volume configuration definition, denoted as VC#
  * Gluster Source (GS)
    * A GS is a place to find the needed gluster bits (RPMs or otherwise)
  * Setup Profile (SP)
    * This is a setup profile, that encompasses the HW, and the OS. The HW
    specification is expanded to include disks and other needed items.
  * Test Results (TR)
    * These are the raw outputs of the test results, denoted as TR#
  * Monitors
    * This is currently a place holder for capturing monitoring information
    across any test
    * This is a TODO item and is mostly not discussed at the moment

### A typical workflow

A logical view of workflow progression is summarized as follows,

BT# =-(run against)--> VC# =-(created using)--> GS# =-(deployed on)--> SP#

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
