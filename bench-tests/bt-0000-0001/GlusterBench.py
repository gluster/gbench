import getopt, sys, subprocess, socket, os, time

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vr:s:f:l:n:t:m:", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print err # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-r", "--record-size"):
            record_size = a
        elif o in ("-s", "--seq-file-size"):
            seq_file_size = a
        elif o in ("-f", "--files"):
            files = a
        elif o in ("-l", "--sm-file-size"):
            sm_file_size = a
        elif o in ("-n", "--sample-size"):
            sample_size = a
        elif o in ("-t", "--threads"):
            thread_count = a
        elif o in ("-m", "--mount-point"):
            mount_point = a
        else:
            assert False, "unhandled option"

    # Use default of 4 for thread count
    try:
        thread_count
    except NameError:
        thread_count = 4

    # Set ENV var for IOZone to use SSH
    try:
        os.environ["RSH"] = "ssh"
    except KeyError:
        print "Unable to set env var RSH=ssh that IOZone needs to run"
        sys.exit(1)

    # Get hostnames
    try:
        clients = os.environ['CLIENT_LIST']
    except KeyError:
        print "The environment variable CLIENTS_LIST must be set and contain a space separated list of IPs or hostnames"
        sys.exit(1)
    try:
        servers = os.environ['SERVER_LIST']
    except KeyError:
        print "The environment variable SERVERS_LIST must be set and contain a space separated list of IPs or hostnames"
        sys.exit(1)

    # Create working directory in /tmp
    try:
        os.stat("/tmp/gbench")
    except:
        os.mkdir("/tmp/gbench")

    # Check for iozone config file
    if os.path.isfile("/tmp/gbench/clients.ioz"):
        # Clean up old file if it exists
        os.remove("/tmp/gbench/clients.ioz")
        print "Deleting existing clients.ioz file\n"

    # Check for iozone bin
    if os.path.isfile("/usr/bin/iozone"):
        print "IOZone check succesfull, bin found at /usr/bin/iozone.\n"

        # Ask the user if they want to create the file
        print "IOZone requires a config file when running multi host, gbench would like to create this file in /tmp/gbench/clients.ioz.  Gbench will create this file with the same number of threads as defined by the -t --threads flag.  If -t is not defined it will use the you the default of 4 threads per client.\n"
        config_iozone = raw_input("\nWould you like to configure the IOZone config file?  Y/N\n")

        # Create the clients.ioz file
        if str(config_iozone.upper()) == "Y":
            print "Configuring IOZone config file -> /tmp/gbench/clients.ioz"
            print "The number of threads per client is " + str(thread_count)
            print "The client mount point is " + str(mount_point)
            ioz_file = open("/tmp/gbench/clients.ioz", "w+")
            length = len(clients.split(" "))
            if int(length) == 1:
                for line in range(0, int(thread_count) // int(length)):
                    ioz_file.write(str(clients) + " " + str(mount_point) + " " + "/usr/bin/iozone\n")
            else:
                for client in clients.split(" "):
                    for line in range(0, int(thread_count) // int(length)):
                        ioz_file.write(str(client) + " " + str(mount_point) + " " + "/usr/bin/iozone\n")
            ioz_file.close()
        else:
            print "The clients.ioz file is required for IOZone to run, exiting.\n"
            sys.exit(1)
    else:
        print "IOZone is not installed or the bin is not located at /usr/bin/iozone.  Check that IOZone is installed and the bin is located at /usr/bin/iozone"
        sys.exit(1)

    # Check for smallfile
    if os.path.isfile("/tmp/gbench/smallfile/smallfile_cli.py"):
        pass
    else:
        # Install smallfile if not found
        print "The smallfile application must be installed in /tmp/gbench/smallfile.\n"
        config_smallfile = raw_input("Would you like to configure smallfile?  NOTE: Git must be installed. Y/N\n")
        if str(config_smallfile.upper()) == 'Y':
            print "Git cloning the smallfile application in /tmp/gbench/smallfile/"
            length = len(clients.split(" "))
            if int(length) == 1:
                subprocess.call(["ssh", "root@" + str(clients), "mkdir", "-p", "/tmp/gbench/smallfile"])
                subprocess.call(["ssh", "root@" + str(clients), "git", "clone", "https://github.com/bengland2/smallfile.git", "/tmp/gbench/smallfile"])
            else:
                print "Git cloning on the following clients -> " + str(clients)
                for client in clients.split(" "):
                    subprocess.call(["ssh", "root@" + str(client), "mkdir", "-p", "/tmp/gbench/smallfile"])
                    subprocess.call(["ssh", "root@" + str(client), "git", "clone", "https://github.com/bengland2/smallfile.git", "/tmp/gbench/smallfile"])
        else:
            sys.exit(1)

    print "Number threads = " + str(thread_count)
    print "Client list = " + str(clients)
    print "Running IOZone with " + str(record_size) + "KB record size and " + str(thread_count) + " threads,  Creating an " + seq_file_size + " GB file with every thread."
    print "Running smallfile with " + str(sm_file_size) + "KB files, creating " + str(files) + " files."
    failed_test = False

    # IOZone seq writes
    print "Running squential IOZone tests, starting with sequential writes."
    (result1, result2) = get_samples(["iozone", "-+m", "/tmp/gbench/clients.ioz",
        "-+h", socket.gethostname(), "-C", "-w", "-c", "-e", "-i", "0", "-+n",
        "-r", str(record_size)+"k", "-s", str(seq_file_size)+"g", "-t", str(thread_count)], "y",
        verbose, sample_size, mount_point)
    print "The results for sequential writes are: "+ str(result1)
    average_seq_write = find_average(result1)
    all_seq_write = result1
    print "The average was for sequential writes was - " + str(average_seq_write)

    # IOZone seq reads
    (result1, result2) = get_samples(["iozone", "-+m", "/tmp/gbench/clients.ioz",
        "-+h", socket.gethostname(), "-C", "-w", "-c", "-e", "-i", "1",
        "-+n", "-r", str(record_size)+"k", "-s", str(seq_file_size)+"g", "-t", str(thread_count)], "n",
        verbose, sample_size, mount_point)
    print "The results for sequential reads are: "+ str(result1)
    average_seq_read = find_average(result1)
    all_seq_read = result1
    print "The average was for sequential reads was - " + str(average_seq_read)

    # IOZone rand read / write
    print "Running random IOZone tests."
    (result1, result2) = get_samples(["iozone", "-+m", "/tmp/gbench/clients.ioz",
        "-+h", socket.gethostname(), "-C", "-w", "-c", "-e", "-i", "2",
        "-+n", "-r", str(record_size)+"k", "-s", str(seq_file_size)+"g", "-t", str(thread_count)],
        "n", verbose, sample_size, mount_point)
    print "The results for random reads are: " + str(result1)
    print "The results for random writes are: " + str(result2)
    average_rand_read = find_average(result1)
    print "The average was for random reads was - " + str(average_rand_read)
    average_rand_write = find_average(result2)
    print "The average was for random writes was - " + str(average_rand_write)

    # Change the space seperated ist to a comma seperated list
    client_list = ""
    first_run = 0
    length_clients = len(clients.split(" "))
    if int(length_clients) == 1:
        client_list = str(clients)
    else:
        for client in clients.split(" "):
            if int(first_run) == 0:
                client_list = str(client)
                first_run = 1
            else:
                client_list = str(client_list) + "," + str(client)

    print "Client list for smallfile is: " + str(client_list) 
    # Smallfile create
    print "Running smallfile create test."
    (result1, result2) = get_samples(["python",
        "/tmp/gbench/smallfile/smallfile_cli.py", "--operation", "create",
        "--threads", "8", "--file-size", str(sm_file_size), "--files", str(files),
        "--top", str(mount_point), "--remote-pgm-dir", "/tmp/gbench/smallfile/", "--host-set", client_list], "y",
        verbose, sample_size, mount_point)
    print "The results for smallfile creates are: " + str(result1)
    average_smallfile_create = find_average(result1)

    # Smallfile read
    print "Running smallfile read test."
    (result1, result2) = get_samples(["python",
        "/tmp/gbench/smallfile/smallfile_cli.py", "--operation", "read",
        "--threads", "8", "--file-size", str(sm_file_size), "--files", str(files),
        "--top", str(mount_point), "--remote-pgm-dir", "/tmp/gbench/smallfile/", "--host-set", client_list], "n",
        verbose, sample_size, mount_point)
    print "The results for smallfile reads are: " + str(result1)
    average_smallfile_read = find_average(result1)

    # Smallfile ls -l
    print "Running smallfile ls -l test."
    (result1, result2) = get_samples(["python",
        "/tmp/gbench/smallfile/smallfile_cli.py", "--operation", "ls-l",
        "--threads", "8", "--file-size", str(sm_file_size), "--files", str(files),
        "--top", str(mount_point), "--remote-pgm-dir", "/tmp/gbench/smallfile/", "--host-set", client_list], "n",
        verbose, sample_size, mount_point)
    print "The results for smallfile reads are: " + str(result1)
    average_smallfile_ls = find_average(result1)

    # Print report
    make_report(sm_file_size, average_seq_write, average_seq_read, average_rand_write, average_rand_read, average_smallfile_create, average_smallfile_read, average_smallfile_ls)

    if failed_test == True:
        sys.exit(1)
    else:
        sys.exit(0)

def usage():
    print "Gluster Benchmark Kit Options:"
    print "  -h --help           Print gbench options."
    print "  -v                  Verbose Output."
    print "  -r --record-size    Record size to write in for large files in KB"
    print "  -s --seq-file-size  The size of file each IOZone thread creates in GB"
    print "  -f --files          The nuber of files to create for smallfile tests in KB"
    print "  -l --sm-file-size   The size of files to create for smallfile tests in KB"
    print "  -n --sample-size    The number of samples to collect for each test"
    print "  -t --threads        The number of threads ro run applications with"
    print "  -m --mount-point    The mount point gbench runs against"
    print "Example: GlusterBench.py -r 1024 -s 8 -f 10000 -l 1024 -n 3 -t 4 -m /gluster-mount -v\n"

def make_report(size, average_seq_write, average_seq_read, average_rand_write, average_rand_read, average_smallfile_create, average_smallfile_read, average_smallfile_ls):
    print "Gluster Benchmark Kit report for " + time.strftime("%I:%M:%S")
    print "Sequential Writes " + str(size) + " record size: " + str(average_seq_write)
    print "Sequential Reads  " + str(size) + " record size: " + str(average_seq_read)
    print "Random Writes     " + str(size) + " record size: " + str(average_rand_write)
    print "Random Reads      " + str(size) + " record size: " + str(average_rand_read)
    print "Smallfile Creates " + str(size) + "   file size: " + str(average_smallfile_create)
    print "Smallfile Reads   " + str(size) + "   file size: " + str(average_smallfile_read)
    print "Smallfile ls -l   " + str(size) + "   file size: " + str(average_smallfile_ls)

def run_command(command_in):
    p = subprocess.Popen(command_in, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while(True):
        retcode = p.poll() #returns None while subprocess is running
        line = p.stdout.readline()
        yield line
        if(retcode is not None):
            break
    print str(line)

# extract result from iozone test in KB/sec
def extract_iozone_result(logfn):
    logfn = logfn.splitlines(True)
    result1 = None
    result2 = None
    for l in logfn:
        if l.__contains__('Children see throughput'):
            tokens = l.split()
            tokenct = len(tokens)
            assert str(tokens[tokenct-1]).upper() == 'KB/SEC'  # line ends with 'KB/sec'
            result = float(tokens[tokenct-2].strip())
            if not result1: result1 = result
            elif not result2: result2 = result
    return (result1, result2)

def run_iozone(iozone_in):
    output = ""
    for line in run_command(iozone_in):
        output = output + line
    return output

# extract result from smallfile in file/sec
def extract_smallfile_result(logfn):
    logfn = logfn.splitlines(True)
    for l in logfn:
        if l.__contains__('files/sec'):
            tokens = l.split()
            tokenct = len(tokens)
            result = float(tokens[0].strip())
            return result

def get_samples(command_in, cleanup, verbose, sample_size, mount_point):
    my_samples = []
    my_samples2 = []
    sample_number = int(sample_size)
    for x in range(0, sample_number):
        print "About to gather sample --> " + str(x)
        current_sample = run_iozone(command_in)
        if "iozone" in command_in:
            (result1, result2) = extract_iozone_result(current_sample)
        else:
            result1 = extract_smallfile_result(current_sample)
            result2 = ""
        if verbose == True:
            print current_sample
        print "Adding the current sample to the list: " + str(result1)
        my_samples.append(result1)
        my_samples2.append(result2)
        cmd = "sh " + str(os.getcwd()) + "/sync-drop-caches.sh"

        p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        print "Dropping cache"
        while True:
            out = p.stderr.read(1)
            if out == '' and p.poll() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()

        if x == (sample_number - 1):
            print "No cleanup on " + str(x) + " iteration."
        elif cleanup == "y":
            cmd = "rm -rf " + str(mount_point) + "/*"
            p = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
            print "Cleaning up files."
            while True:
                out = p.stderr.read(1)
                if out == '' and p.poll() != None:
                    break
                if out != '':
                    sys.stdout.write(out)
                    sys.stdout.flush()
        else:
            pass
    return (my_samples, my_samples2)

def find_average(samples_in):
    length_in = len(samples_in)
    total = 0
    for x in range(0, length_in):
        total = total + int(samples_in[x])
    average = total / length_in
    return average

if __name__ == "__main__":
    main()
