import subprocess
import sys

def run_script(script_name, args):
    """Run a python script with given arguments."""
    cmd = ["python3", script_name] + args
    with subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr) as proc:
        proc.communicate()  # Wait for the subprocess to finish

    if proc.returncode == 0:
        print(f"{script_name} executed successfully.")
    else:
        print(f"Error in {script_name}: Return code {proc.returncode}")


def main(folders):
    if len(folders) < 2:
        print("Please provide at least two folders.")
        sys.exit(1)

    # Step 1: Run combine_data.py
    run_script("combine_data.py", folders)

    # get name of the combined data with "_vs_" in between each data
    new_folder_name = "_vs_".join(folders)

    # Step 2: Run tSNE.py
    run_script("tSNE.py", [new_folder_name])

    # Step 3: Run plotly2d.py
    run_script("plotly2d.py", [new_folder_name])

    # Step 4: Run plotly3d.py
    run_script("plotly3d.py", [new_folder_name])

if __name__ == "__main__":
    main(sys.argv[1:])  # Pass all command line arguments except the script name to main