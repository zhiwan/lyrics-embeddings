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


def main(artist_name, top_hits_count):
    # Step 1: Run geniusExportLyrics.py
    genius_export_args = [artist_name, str(top_hits_count)]
    run_script("geniusExportLyrics.py", genius_export_args)

    # Assuming the JSON filename is formatted as "<artist_name>_top_<top_hits_count>.json"
    json_filename = f"{artist_name.replace(' ', '_')}"

    # # Step 2: Run embeddings.py
    embeddings_args = [json_filename]
    run_script("embeddings.py", embeddings_args)

    # Step 3: Run tSNE.py
    # tsne_args = [json_filename]
    # run_script("tSNE.py", tsne_args)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <artist_name> <song_number>")
        sys.exit(1)

    artist_name = sys.argv[1]
    song_number = sys.argv[2]  # Convert song number argument to an integer
    main(artist_name, song_number)