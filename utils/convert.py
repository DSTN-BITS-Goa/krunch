import os
import zipfile
import tarfile
import tempfile
import shutil


def convert_zip_to_tgz(zip_path):
    dir_name = os.path.dirname(zip_path)
    base_name = os.path.splitext(os.path.basename(zip_path))[0]

    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract ZIP contents
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # Check if there's only one directory in the extracted content
        contents = os.listdir(temp_dir)
        if len(contents) == 1 and os.path.isdir(os.path.join(temp_dir, contents[0])):
            original_dir = os.path.join(temp_dir, contents[0])
            handin_dir = os.path.join(temp_dir, "handin")
            os.rename(original_dir, handin_dir)
        else:
            # If there's no single directory, create 'handin' and move everything into it
            handin_dir = os.path.join(temp_dir, "handin")
            os.mkdir(handin_dir)
            for item in contents:
                shutil.move(os.path.join(temp_dir, item), handin_dir)

        # Create TGZ file
        tgz_path = os.path.join(dir_name, f"{base_name}.tgz")
        with tarfile.open(tgz_path, "w:gz") as tar:
            tar.add(handin_dir, arcname="handin")


def find_zip_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".zip"):
                yield os.path.join(root, file)


def main():
    start_dir = "."  # Current directory
    for zip_file in find_zip_files(start_dir):
        print(f"Converting {zip_file} to TGZ...")
        convert_zip_to_tgz(zip_file)
        print(f"Converted {zip_file} to TGZ successfully.")


if __name__ == "__main__":
    main()
