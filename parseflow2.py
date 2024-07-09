import csv
import subprocess
import time

# Run the ovs-ofctl command and capture the output
bridge_name = "s1"

while True:
    # Generate a unique CSV file name based on the current timestamp
    timestamp = time.strftime("%Y%m%d%H%M%S")
    csv_file = "flows_{}.csv".format(timestamp)

    # Execute the ovs-ofctl command and capture the output
    command = "sudo ovs-ofctl dump-flows {}".format(bridge_name)
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    output = result.stdout

    # Extract the flow details from the output
    flows = []
    lines = output.strip().split("\n")
    for line in lines:
        if line.startswith(" cookie"):
            flow = line.split(",")
            flows.append(flow)

    # Write the flows to the CSV file
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(flows)

    print("Flow details have been written to {}.".format(csv_file))

    # Delay for 30 seconds
    time.sleep(30)

