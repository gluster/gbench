# Ansible setup-profile
Ansible playbook to generate setup-profile for [gbench](https://github.com/gluster/gbench/) using jinja2 template.

## How to run?

Run the playbook `configure.yml` with additional parameters for servers, clients and devices. Where servers are list of coma seperated hosts(IP addresses/hostnames) that are going to be glusterfs server, clients are coma seperated clients(IP addresses/hosts) that are going to be gluster clients and devices are the list of coma seperated drives(currently same devices names are considered) that are attached to the servers.

```console
ansible-playbook configure.yml -e 'servers=host1,host2,...hostn clients=client1,client2,...clientn devices=sda,sdb'
```

## What `configure.yml` does?
`configure.yml` takes the aditional facts and use it to generate another yaml file `exportenv.yml` using jinja template and `systems.yml` which stores server and client IP/hostname and then it includes the generated `exportenv.yml` and runs its tasks.

`exportenv.yml` creates directories for server and client and adds public files in those created directories.

For example there are three servers whose IP addresses are `10.0.0.1`, `10.0.0.2` and `10.0.0.3` and two clients `10.0.0.4` and `10.0.0.5` the generated directory structure will look like the following which is according to the desired setup-profile
```console
ansible-playbook configure.yml -e 'servers=10.0.0.1,10.0.0.2,10.0.0.3 clients=10.0.0.4,10.0.0.5 devices=sda,sdb,sdc'
```

```
setup-profile
├── group_vars
│   ├── all
│   ├── client1
│   │   └── public
│   ├── client2
│   │   └── public
│   ├── server1
│   │   └── public
│   ├── server2
│   │   └── public
│   └── server3
│       └── public
└── inventory.ini
```
