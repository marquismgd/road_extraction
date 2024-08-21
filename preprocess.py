import os

def delete_files_except_extensions(path, extensions_to_keep):
    """
    Deletes all files in the specified path that do not have the given extensions.

    Parameters:
        path (str): The path to the directory containing the files.
        extensions_to_keep (list): A list of file extensions (e.g., ['.txt', '.jpg']) that should not be deleted.

    Returns:
        None
    """
    if not os.path.isdir(path):
        print(f"Error: '{path}' is not a valid directory.")
        return

    for root, _, files in os.walk(path):
        for file_name in files:
            _, ext = os.path.splitext(file_name)
            if ext not in extensions_to_keep:
                file_path = os.path.join(root, file_name)
                os.remove(file_path)
                print(f"Deleted file: {file_path}")

if __name__ == "__main__":
    # Example usage:
    target_directory1 = "F:\Columbus\mosaic\gis\label"  # Replace this with your desired directory path.
    target_directory2 = "F:\Columbus\mosaic\gis\image"
    extensions_to_keep = ['.tif']  # Add any file extensions you want to keep.

    delete_files_except_extensions(target_directory1, extensions_to_keep)
    delete_files_except_extensions(target_directory2, extensions_to_keep)
