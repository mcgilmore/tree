# tree.py v0.2
# michael.gilmore@umu.se
import subprocess
import csv

def run_curl_command(curl_command):
    try:
        result = subprocess.check_output(
            curl_command, shell=True, stderr=subprocess.STDOUT
        )
        return result.decode("utf-8").split("\n", 3)[-1]
    except subprocess.CalledProcessError as e:
        print(f"Error executing curl command: {e.output.decode('utf-8')}")
        return None


def retrieve_organism_names(group_id):
    response = run_curl_command(
        f'curl -X GET "https://data.orthodb.org/current/tab?id={group_id}"')

    if response:
        # Remove initial lines
        tsv_data = response.split("\n", 3)[-1]

        # Parse TSV data
        reader = csv.reader(tsv_data.splitlines(), delimiter="\t")
        next(reader)  # Skip the header row

        organism_names = []
        for row in reader:
            if len(row) >= 5:
                organism_name = row[4]
                organism_name = organism_name.replace(" ", "_")
                organism_names.append(organism_name)

        # get rid of duplicates
        seen = set()
        organism_names_unique = []
        for organism in organism_names:
            if organism not in seen:
                organism_names_unique.append(organism)
                seen.add(organism)
        return organism_names_unique

def writeiTol(file_path, unique_names, group_id):
 with open(file_path, "w") as file:
    file.write("DATASET_GRADIENT\n")
    file.write("#Dataset created using tree.py\n\n")
    file.write("SEPARATOR TAB\n")
    file.write("DATASET_LABEL\t{}\n".format(group_id))
    file.write("COLOR\t#00ff00\n")
    file.write("COLOR_MIN\t#00ff00\n")
    file.write("COLOR_MAX\t#0000ff\n\n")
    file.write("DATA\n")
    for organism_name in unique_names:
        file.write(f"{organism_name}\t1\n")
