import getopt, sys, subprocess, socket, os, time

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:s:f:v", ["help", "output="])
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
        elif o in ("-s", "--size"):
            size = a
        elif o in ("-f", "--files"):
            files = a
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

    # Get hostnames
    try:
        clients = os.environ['CLIENTS']
    except KeyError:
        print "The environment variable CLIENTS must be set and contain a space separated list of IPs or hostnames"
        sys.exit(1)
    try:
        servers = os.environ['SERVERS']
    except KeyError:
        print "The environment variable SERVERS must be set and contain a space separated list of IPs or hostnames"
        sys.exit(1)

    # Check for iozone config file
    if os.path.isfile("/root/clients.ioz"):
        pass
    else:
        print "The iozone config file must be stored in /root/clients.ioz.  It also must have the same number of threads as defined with the -t --threads flag.  If -t is not defined it will use the you the default of 4 threads per client."
        config_iozone = input("Would you like to configure the IOZone config file?  Y/N")
        if config_iozone == "Y":
            print "Configuring IOZone config file -> /root/clients.ioz"
            print "The number of threads per client is " + str(thread_count)
            ioz_file = open("/root/clients.ioz", "w+")
            for client in clients:
                for line in range(1, thread_count)
                    ioz_file.write(client + " " + mount_point + " " + "/usr/bin/iozone\n"
        else:
            sys.exit(1)

    # Check for smallfile
    if os.path.isfile("/root/smallfile/smallfile_cli.py"):
        pass
    else:
        print "The smallfile application must be installed in /root/smallfile."
        config_smallfile = input("Would you like to configure smallfile?  NOTE: Git must be installed. Y/N")
        if config_smallfile == "Y"
            print "Git cloning the smallfile application in /root/smallfile/"
            for client in clients:
                run_command("ssh root@" + client " git clone https://github.com/bengland2/smallfile.git"
        else
            sys.exit(1)

    number_threads = 0
    client_list = ""
    for host in clients.split(" "):
        if number_threads == 0:
            client_list = host
        else:
            client_list = client_list + "," + host
        number_threads = number_threads + 1
    number_threads = number_threads * 4
    print "Number threads = " + str(number_threads)
    print "Client list = " + client_list
    print "Running IOZone with " + str(size) + "KB record size and " + str(number_threads) + " threads,  Creating an 8 GB file with every thread."
    print "Running smallfile with " + str(size) + "KB files, creating " + str(files) + " files."
    failed_test = False

    # IOZone seq writes
    print "Running squential IOZone tests, starting with sequential writes."
    (result1, result2) = get_samples(["iozone", "-+m", "/root/clients.ioz",
        "-+h", socket.gethostname(), "-C", "-w", "-c", "-e", "-i", "0", "-+n",
        "-r", str(size)+"k", "-s", "8g", "-t", str(number_threads)], "y",
        verbose, sample_size)
    print "The results for sequential writes are: "+ str(result1)
    average_seq_write = find_average(result1)
    all_seq_write = result1
    print "The average was for sequential writes was - " + str(average_seq_write)

    # IOZone seq reads
    (result1, result2) = get_samples(["iozone", "-+m", "/root/clients.ioz",
        "-+h", socket.gethostname(), "-C", "-w", "-c", "-e", "-i", "1",
        "-+n", "-r", str(size) + "k", "-s", "8g", "-t", str(number_threads)], "n",
        verbose, sample_size)
    print "The results for sequential reads are: "+ str(result1)
    average_seq_read = find_average(result1)
    all_seq_read = result1
    print "The average was for sequential reads was - " + str(average_seq_read)

    # IOZone rand read / write
    print "Running random IOZone tests."
    (result1, result2) = get_samples(["iozone", "-+m", "/root/clients.ioz",
        "-+h", socket.gethostname(), "-C", "-w", "-c", "-e", "-i", "2", "-J",
        "3", "-+n", "-r", str(size)+"k", "-s", "2g", "-t", str(number_threads)],
        "n", verbose, sample_size)
    print "The results for random reads are: " + str(result1)
    print "The results for random writes are: " + str(result2)
    average_rand_read = find_average(result1)
    print "The average was for random reads was - " + str(average_rand_read)
    average_rand_write = find_average(result2)
    print "The average was for random writes was - " + str(average_rand_write)

    # Smallfile create
    print "Running smallfile create test."
    (result1, result2) = get_samples(["python",
        "/root/smallfile/smallfile_cli.py", "--operation", "create",
        "--threads", "8", "--file-size", str(size), "--files", str(files),
        "--top", "/gluster-mount", "--host-set", client_list], "y",
        verbose, sample_size)
    print "The results for smallfile creates are: " + str(result1)
    average_smallfile_create = find_average(result1)

    # Smallfile read
    print "Running smallfile read test."
    (result1, result2) = get_samples(["python",
        "/root/smallfile/smallfile_cli.py", "--operation", "read",
        "--threads", "8", "--file-size", str(size), "--files", str(files),
        "--top", "/gluster-mount", "--host-set", client_list], "n",
        verbose, sample_size)
    print "The results for smallfile reads are: " + str(result1)
    average_smallfile_read = find_average(result1)

    # Smallfile ls -l
    print "Running smallfile ls -l test."
    (result1, result2) = get_samples(["python",
        "/root/smallfile/smallfile_cli.py", "--operation", "ls-l",
        "--threads", "8", "--file-size", str(size), "--files", str(files),
        "--top", "/gluster-mount", "--host-set", client_list], "n",
        verbose, sample_size)
    print "The results for smallfile reads are: " + str(result1)
    average_smallfile_ls = find_average(result1)

    # Print report
    make_report(size, average_seq_write, average_seq_read, average_rand_write, average_rand_read, average_smallfile_create, average_smallfile_read, average_smallfile_ls)

    if failed_test == True:
        sys.exit(1)
    else:
        sys.exit(0)

def usage():
    print "Gluster Benchmark Kit Options:"
    print "  -h --help           Print gbench options."
    print "  -v                  Verbose Output."
    print "  -s --size           Record size for large files, file size for small files."
    print "  -f --files          The nuber of files to create for smallfile tests."
    print "  -n --sample-size    The number of samples to collect for each test."
    print "Example: GlusterBench.py -s 64 -f 10000 -n 5 -v\n"

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

# extract result from iozone test in KB/sec
def extract_iozone_result(logfn):
    logfn = logfn.splitlines(True)
    result1 = None
    result2 = None
    for l in logfn:
        if l.__contains__('Children see throughput'):
            tokens = l.split()
            tokenct = len(tokens)
            assert str(tokens[tokenct-1]).upper() == 'KB/sec'  # line ends with 'KB/sec'
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

def get_samples(command_in, cleanup, verbose, sample_size):
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
        cmd = "sh /root/sync-drop-caches.sh"

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
            cmd = "rm -rf /gluster-mount/*"
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
