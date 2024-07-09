import csv
import subprocess

# Run the ovs-ofctl command and capture the output
bridge_name = "s1"
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

# Write the flows to a CSV file
csv_file = "flows8.csv"
with open(csv_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(flows)

print("Flow details have been written to {}.".format(csv_file))


