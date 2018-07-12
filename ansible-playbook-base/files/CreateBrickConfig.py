#!/usr/bin/env python

"""Module to parse and generate storage and volume configuration.

This would be some python code that would take in the required arguments to
generate a storage configuration JSON file and also possibly a gdeploy
configuration file for use with other plays.
This python will also check (first) if the given volume(s) can be configured
in the given setup
"""

import json
import argparse
import yaml
from enum import Enum


class VolumeConfiguration:
    """Class for all volume configuration parsing and method needs."""

    def __init__(self, infile):
        """Iniitalized with a passed in file path."""
        # close infile_fp on exceptions
        self.infile = infile
        try:
            infile_fp = open(self.infile)
        except:
            raise

        try:
            self.vcdict = yaml.load(infile_fp)
        except:
            estr = "Unable to parse YAML data in volume"\
                   " configuration definition file " + infile
            raise ValueError(estr)

        # TODO: Check if only valid kwys are present in the dict

        self.distribute = self.vcdict.get("distribute")
        if self.distribute is None:
            raise ValueError("Missing 'distribute' count in volume definition")
        if (type(self.distribute) is not int) or (self.distribute <= 0):
            raise ValueError("'distribute' in volume definition is not a"
                             " valid integer")

        self.replica_count = self.vcdict.get("replica_count")
        if self.replica_count is None:
            self.replica_count = 0
        if (type(self.replica_count) is not int) or (self.replica_count < 0):
            raise ValueError("'replica_count' in volume definition is not a"
                             " valid integer")

        self.disperse_count = self.vcdict.get("disperse_count")
        if self.disperse_count is None:
            self.disperse_count = 0
            self.redundancy_count = 0
        else:
            self.redundancy_count = self.vcdict.get("redundancy_count")
            if self.redundancy_count is None:
                raise ValueError("'redundancy_count' in volume definition is"
                                 " not specified")

        if (type(self.disperse_count) is not int) or (self.disperse_count < 0):
            raise ValueError("'disperse_count' in volume definition is not a"
                             " valid integer")

        if (type(self.redundancy_count) is not int) or (self.redundancy_count < 0):
            raise ValueError("'redundancy_count' in volume definition is not a"
                             " valid integer")

        if (self.replica_count > 0) and (self.disperse_count > 0):
            raise ValueError("Invalid volume configuration, both replica and"
                             " disperse counts specified")

        infile_fp.close()

    def bricksneeded(self):
        """Function to determine number of bricks or mounts needed."""
        mounts_needed = (self.distribute *
                         (self.replica_count if (self.replica_count > 0)
                          else ((self.disperse_count + self.redundancy_count)
                                if (self.disperse_count > 0)
                                else 1)))

        return mounts_needed


class StorageConfiguration:
    """Class for all Storage configuration parsing and method needs."""

    supported_fstypes = {'xfs'}
    raidname_pattern = "/dev/md%d"
    vgname_pattern = "vggbench%04d"
    lvpname_pattern = "lvpoolgbench%04d"
    lvname_pattern = "lvgbench%04d"
    mount_pattern = "fsgbench%04d"

    def __init__(self, infile):
        """Initialized with a passed in file path."""
        # close infile_fp on exceptions
        self.infile = infile
        try:
            infile_fp = open(self.infile)
        except:
            raise

        try:
            self.scdict = yaml.load(infile_fp)
        except:
            estr = "Unable to parse YAML data in storage"\
                   " configuration definition file " + infile
            raise ValueError(estr)

        # TODO: Check if only valid keys are present in the dict

        try:
            self.disk_type = DiskType[self.scdict.get("disk_type")]
        except:
            raise ValueError("disk_type does not have a valid value")

        try:
            self.disk_grouping = DiskGrouping[self.scdict.get("disk_grouping")]
        except:
            raise ValueError("disk_grouping does not have a valid value")

        try:
            self.disk_size = SizeConstraint[self.scdict.get("disk_size")]
        except:
            raise ValueError("disk_size does not have a valid value")

        # TODO: All option strings may need some validation, else things may
        # fail elsewhere.
        self.group_options = self.scdict.get("group_options")
        if (self.group_options is None) or (self.group_options == "default"):
            self.group_options = ""

        self.pvoptions = self.scdict.get("pvoptions")
        if (self.pvoptions is None) or (self.pvoptions == "default"):
            self.pvoptions = ""

        self.vgoptions = self.scdict.get("vgoptions")
        if (self.vgoptions is None) or (self.vgoptions == "default"):
            self.vgoptions = ""

        self.usethinpools = self.scdict.get("lv_usethinpool")
        if (self.usethinpools is None):
            self.usethinpools = True
        if type(self.usethinpools) is not bool:
            raise ValueError("lv_usethinpool does not have a valid value")

        self.lvpooloptions = self.scdict.get("lvpooloptions")
        if (self.lvpooloptions is None) or (self.lvpooloptions == "default"):
            self.lvtpooloptions = ""

        self.lvoptions = self.scdict.get("lvoptions")
        if (self.lvoptions is None) or (self.lvoptions == "default"):
            self.lvoptions = ""

        self.fstype = self.scdict.get("fstype")
        if self.fstype not in StorageConfiguration.supported_fstypes:
            raise ValueError("fstype does not have a valid value")

        self.fsoptions = self.scdict.get("fsoptions")
        if (self.fsoptions is None) or (self.fsoptions == "default"):
            self.fsoptions = ""

        self.mountpoint_base = self.scdict.get("mountpoint_base")
        # TODO: check if this is in proper path format

        infile_fp.close()


class DiskType(Enum):
    """Types of disks that we recognize."""

    rotational = 1
    nonrotational = 2


class DiskGrouping(Enum):
    """Types of disk grouping that we recognize."""

    jbod = 1


class SizeConstraint(Enum):
    """Types of size constraints that we recognize."""

    equal = 1
    ignore = 2


class HostsFacts:
    """Class to handle jason data of saved hosts facts."""

    key_host_dict_list = "host_data"
    key_host_device_list = "devices"

    def __init__(self, infile):
        """Initialize object with passed in JSON dict."""
        self.infile = infile
        try:
            infile_fp = open(self.infile)
        except:
            raise

        try:
            self.hostfacts = json.load(infile_fp)
        except:
            estr = "Unable to parse JSON data in from host fact file " + infile
            raise ValueError(estr)

    def gettotalhosts(self):
        """Return number of hosts in the object."""
        return len(self.hostfacts.get(HostsFacts.key_host_dict_list))

    def gethostdict(self, idx):
        """Helper to return a specific hosts dict."""
        host_list = self.hostfacts.get(HostsFacts.key_host_dict_list)
        host_dict = host_list[idx]
        return host_dict

    def finddeviceinpartition(self, devicename, ansible_devices):
        """Test."""
        ansible_partition = None
        ansible_device = None
        partfound = False
        partname = None

        for key, a_device in ansible_devices.items():
            ansible_device = a_device

            if (key == devicename):
                break
            else:
                partitions = a_device.get("partitions")
                if partitions is None:
                    continue

                for partkey, partition in partitions.items():
                    ansible_partition = partition
                    if (partkey == devicename):
                        partfound = True
                        partname = partkey
                        break
                    ansible_partition = None

            if partfound:
                break

        return ansible_device, ansible_partition, partname

    def deviceavailable(self, device, host_dict):
        """Return true if device is free for use"""
        ansible_lvm = host_dict.get("ansible_lvm")
        pvs = ansible_lvm.get("pvs")
        for pvname, pvattrs in pvs.items():
            if pvname != device:
                continue
            # Found a PV on this device
            if pvattrs.get("vg") is "":
                # No VG on PV we can use this device
                return True
            if host_dict.get("gbench_device_cleanup") is True:
                # We are allowed to cleanup, so we can use this device
                return True
            # It is in the PV list and has a VG and cleanup is not allowed
            return False

        # Did not find the device in pvs, assume it is available
        # TODO: Ideally we should check the partition and see if it is occupied
        # and if not use it.
        return True

    def gethostdisklist(self, idx):
        """Get a list of available disks and their properties.

        This returns a 2D list having the following structure,
            [[
                type = rotational|nonrotational,
                size = string,
                disk = device,
                host = hostname
            ],
            ...]
        """
        disklist = []
        host_dict = self.gethostdict(idx)
        inventory_host = host_dict.get("inventory_hostname")

        ansible_devices = host_dict.get("ansible_devices")
        if (ansible_devices is None):
            return disklist

        devices = host_dict.get(HostsFacts.key_host_device_list)
        for device in devices:
            if not self.deviceavailable(device, host_dict):
                continue
            devicename = device.rsplit("/", 1)[-1]
            (
                ansible_device,
                ansible_partition,
                part_name
            ) = self.finddeviceinpartition(
                                        devicename,
                                        ansible_devices)
            if (ansible_device is not None):
                currentdisk = []
                dtype = (DiskType.rotational
                         if (ansible_device.get("rotational") == "1")
                         else (DiskType.nonrotational))
                size = (ansible_device.get("size")
                        if (ansible_partition is None)
                        else ansible_partition.get("size"))
                currentdisk = [dtype, size, device, inventory_host]
                disklist.append(currentdisk)

        return disklist

    def gethostdiskcount(self, idx):
        """Return device count for given host index."""
        host_dict = self.gethostdict(idx)

        disks_dict = host_dict.get(HostsFacts.key_host_device_list)
        return len(disks_dict)

    def gettotaldiskcount(self, disk_type=DiskType.rotational,
                          size_constraint=SizeConstraint.ignore):
        """Get total disks available across all hosts."""
        totaldisks = 0

        # loop over devices and get their properties
        # Get a set of sizes (unique)

        for idx in range(self.gettotalhosts()):
            disks = self.gethostdiskcount(idx)
            totaldisks += disks

        return totaldisks

    def generatecleanupconfig(self):
        """Generate a variable file to cleanup provided devices.

        Generates the following dict,
        {
          <hostname>:
          {
            "umount": "yes"|"no",
            "devices": [<pv1>, ...]
          },
          ...
        }
        """
        cleanupdict = {}
        for idx in range(self.gettotalhosts()):
            host_dict = self.gethostdict(idx)
            inventory_host = host_dict.get("inventory_hostname")
            if not host_dict.get("gbench_device_cleanup"):
                continue
            devices = host_dict.get(HostsFacts.key_host_device_list)
            cleanupdict[inventory_host] = {}
            if devices is not None:
                cleanupdict[inventory_host]['unmount'] = "yes"
                cleanupdict[inventory_host]['devices'] = []
            else:
                cleanupdict[inventory_host]['unmount'] = "no"
            for device in devices:
                cleanupdict[inventory_host]['devices'].append(device)

        self.cleanupconf = cleanupdict
        return

    def dumpcleanupconfiguration(self, outfile):
        """Dump the generated cleanup configuration"""

        cleanup_conf_fp = open(outfile, "w")
        json.dump(self.cleanupconf, cleanup_conf_fp, indent=2)
        cleanup_conf_fp.close()

    def getavailabledisks(self):
        """Return a list of available disks and their attributes."""
        disklist = []
        for idx in range(self.gettotalhosts()):
            disklist.append(self.gethostdisklist(idx))

        return disklist


class SetupStorage:
    """Class to generate storage setup JSON based on given parameters."""

    def __init__(self, hf, sc, vc):
        """Initialize object."""
        self.hf = hf
        self.sc = sc
        self.vc = vc
        self.ss = []

    def adddisks(self, diskstoadd):
        """Add a disk to the setup list.

        diskstoadd is of the form,
        [[
                type = rotational|nonrotational,
                size = string,
                disk = device,
                host = hostname
            ],
        ...]

        Each device is added to object ss under its hostname as follows,
        [hostname, namingdict,
         [[devices], grouping, devicename, pvoptions, vgname, vgoptions,
           lvpoolname, lvpooloptions, lvname, lvoptions, fstype, fsoptions,
           mountpoint]]

        Where,
        namingdict {
            devnameidx,
            vgnameidx,
            lvpoolnameidx,
            lvnameidx,
            mountpointidx
        }

        namingdict holds data about last used name index, for autogeneration
        of names used in the setup.

        ss as a result has N rows, where N is the number of hosts.
        """
        try:
            hostname = diskstoadd[0][3]
        except:
            raise

        try:
            hostlist = None
            for iterhostlist in self.ss:
                if iterhostlist[0] == hostname:
                    hostlist = iterhostlist
                    break
            if hostlist is None:
                raise ValueError
        except ValueError:
            # if not found add the inital host entry to the ss list
            namingdict = {'devnameidx': 1, 'vgnameidx': 1, 'lvpoolnameidx': 1,
                          'lvnameidx': 1, 'mountpointidx': 1}
            hostlist = [hostname, namingdict, []]
            self.ss.append(hostlist)

        # generate the device list
        devicedefinition = []

        disks = []
        for disk in diskstoadd:
            disks.append(disk[2])
        devicedefinition.append(disks)

        # TODO: When we support RAID, the 2 items below need to change
        devicedefinition.append(DiskGrouping.jbod)
        devicedefinition.append("default")

        devicedefinition.append(self.sc.pvoptions)

        vgname = self.sc.vgname_pattern % hostlist[1]['vgnameidx']
        devicedefinition.append(vgname)
        devicedefinition.append(self.sc.vgoptions)

        lvpoolname = self.sc.lvpname_pattern % hostlist[1]['lvpoolnameidx']
        devicedefinition.append(lvpoolname)
        devicedefinition.append(self.sc.lvpooloptions)

        lvname = self.sc.lvname_pattern % hostlist[1]['lvnameidx']
        devicedefinition.append(lvname)
        devicedefinition.append(self.sc.lvoptions)

        devicedefinition.append(self.sc.fstype)
        devicedefinition.append(self.sc.fsoptions)

        mountpoint = ((self.sc.mountpoint_base) + "/" +
                      (self.sc.mount_pattern % hostlist[1]['mountpointidx']))
        devicedefinition.append(mountpoint)

        # add the sublist to the host list
        hostlist[2].append(devicedefinition)

        # update the host dict naming indices
        # tmp = hostlist[1]['devnameidx']
        hostlist[1]['devnameidx'] += 1
        hostlist[1]['vgnameidx'] += 1
        hostlist[1]['lvpoolnameidx'] += 1
        hostlist[1]['lvnameidx'] += 1
        hostlist[1]['mountpointidx'] += 1

    def generatestorageconfiguration(self):
        """Routine to check setup against passed in definitions.

        Determines feasibility of creating required definition on the setup.
        Returns number of total mounts needed based on the definition.
        """
        try:
            mounts_required = self.vc.bricksneeded()
        except:
            raise

        disksavailableacrosshosts = self.hf.getavailabledisks()

        host_idx = 0
        cnt = 0
        for i in range(mounts_required):
            founddisk = []
            hostssearched = 0
            # Search till all hosts are exhausted or a disk
            # found (hostssearched == -1)
            while ((hostssearched != len(disksavailableacrosshosts)) and
                   (hostssearched != -1)):
                hostdisklist = disksavailableacrosshosts[host_idx]

                # Sort this list as needed type, size for efficiency
                for disk in hostdisklist:
                    # Apply other constraints as needed!
                    if disk[0] == self.sc.disk_type:
                        workingdisk = hostdisklist.pop(hostdisklist.
                                                       index(disk))
                        founddisk.append(workingdisk)
                        break

                # Move to the next host, for the next inner or outer iteration
                host_idx += 1
                if (host_idx == len(disksavailableacrosshosts)):
                    host_idx = 0

                if (len(founddisk) != 0):
                    self.adddisks(founddisk)
                    cnt = cnt + 1
                    hostssearched = -1
                else:
                    hostssearched += 1

            if (hostssearched == len(disksavailableacrosshosts)):
                raise OverflowError("Cannot support volume configuration on"
                                    " setup, not enough disks")

        return

    def dumpstorageconfiguration(self, outfile):
        """Dump the generated storage configuration.

        This is currently dumb, and just dumps all lines as is, better ways
        to do the same would be to merge PV creation and device creation.

        Dump format:
        {
          <inventory_hostname>:
          {
            <generated host dict>
          },...
        }
        """
        outdict = {}

        for hostlist in self.ss:
            hostdict = self.generatehostdict(hostlist)
            outdict[hostlist[0]] = hostdict
        # print outdict
        # print json.dumps(outdict, indent=2)

        storage_conf_fp = open(outfile, "w")
        json.dump(outdict, storage_conf_fp, indent=2)
        storage_conf_fp.close()

        return

    def generatehostdict(self, hostlist):
        """Dump the generate host storage configuration.

        Dump format:
        {
            'devices': <generateddevicessection>,
            'pvs': <generatedpvssection>,
            'vgs': ...,
            'lvpools': ...,
            'lvs': ...,
            'mounts': ...
        }
        """
        outdict = {}

        outdict['devices'] = self.generatedevicesection(hostlist)
        outdict['pvs'] = self.generatepvssection(hostlist)
        outdict['vgs'] = self.genereatevgssection(hostlist)
        outdict['lvpools'] = self.generatelvpoolssection(hostlist)
        outdict['lvs'] = self.generatelvssection(hostlist)
        outdict['mounts'] = self.generatemountsection(hostlist)

        return outdict

    def generatedevicesection(self, hostlist):
        """Generate the following list.

        [
          {
            "grouping": <grouping>,
            "disks": [<devices>],
          }, ...]
        """
        outlist = []

        for device in hostlist[2]:
            devdict = {}
            devdict['disks'] = device[0]
            devdict['grouping'] = DiskGrouping(device[1]).name
            outlist.append(devdict)

        return outlist

    def generatepvssection(self, hostlist):
        """Generate the following list.

        [
          {
            "devices": [<devices>],
            "options": <pvoptions>
          }, ...]
        """
        outlist = []

        for device in hostlist[2]:
            devdict = {}
            devdict['devices'] = device[0]
            devdict['options'] = device[3]
            outlist.append(devdict)

        return outlist

    def genereatevgssection(self, hostlist):
        """Generate the following list.

        [
          {
            "vgname": <vgname>,
            "pv": [<devices>],
            "options": <vgoptions>
          },...]
        """
        outlist = []

        for device in hostlist[2]:
            devdict = {}
            devdict['vgname'] = device[4]
            devdict['pv'] = device[0]
            devdict['options'] = device[5]
            outlist.append(devdict)

        return outlist

    def generatelvpoolssection(self, hostlist):
        """Generate the following list.

        [
          {
            "lvname": <lvpoolname>,
            "options": <lvpooloptions>,
            "vg": <vgname>
          },...]
        """
        outlist = []

        for device in hostlist[2]:
            devdict = {}
            devdict['lvname'] = device[6]
            devdict['vg'] = device[4]
            devdict['options'] = device[7]
            outlist.append(devdict)

        return outlist

    def generatelvssection(self, hostlist):
        """Generate the following list.

        [
          {
            "lvname": <lvname>,
            "options": <lvoptions>,
            "vg": <vgname>
            "lvpool": <lvpoolname>
          },...]
        """
        outlist = []

        for device in hostlist[2]:
            devdict = {}
            devdict['lvname'] = device[8]
            devdict['vg'] = device[4]
            devdict['lvpool'] = device[6]
            devdict['options'] = device[9]
            outlist.append(devdict)

        return outlist

    def generatemountsection(self, hostlist):
        """Generate the following list.

        [
          {
            "fstype": <fstype>,
            "options": <fsoptions>,
            "mountpoint": <mountpoint>,
            "lvpath": /dev/mapper/<vgname>-<lvname>
          },...]
        """
        outlist = []

        for device in hostlist[2]:
            devdict = {}
            devdict['fstype'] = device[10]
            devdict['mountpoint'] = device[12]
            devdict['options'] = device[11]
            devdict['lvpath'] = "/dev/mapper/" + device[4] + "-" + device[8]
            outlist.append(devdict)

        return outlist


def main():
    """Main function."""
    parser = argparse.ArgumentParser()
    parser.add_argument("vc_definition",
                        help="Volume configuration definition file")
    parser.add_argument("sc_definition",
                        help="Storage setup definition file")
    parser.add_argument("hosts_facts",
                        help="Host facts in JSON from server hosts")
    args = parser.parse_args()

    vc = VolumeConfiguration(args.vc_definition)
    sc = StorageConfiguration(args.sc_definition)
    hf = HostsFacts(args.hosts_facts)

    hf.generatecleanupconfig()
    hf.dumpcleanupconfiguration("./cleanupconfiguration.json")

    ss = SetupStorage(hf, sc, vc)
    ss.generatestorageconfiguration()
    ss.dumpstorageconfiguration("./storageconfiguration.json")


if __name__ == "__main__":
    main()
