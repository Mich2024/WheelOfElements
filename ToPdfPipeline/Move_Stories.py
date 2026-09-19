import os

BATCH_SIZE = 3

# Resolve paths relative to the script, not the current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.join(script_dir, "out")
target_root = os.path.normpath(os.path.join(script_dir, "..", "Books", "Storybook"))

# Collect all Stories_XX.png files and sort them by their number
pictures = []
for filename in os.listdir(source_dir):
    name, ext = os.path.splitext(filename)
    if name.startswith("Stories_") and ext.lower() == ".png":
        number_part = name.split("_")[1]
        if number_part.isdigit():
            pictures.append((int(number_part), filename))
pictures.sort()

# Move each picture into its story folder (pictures 1-3 -> Story1, 4-6 -> Story2, ...)
for number, filename in pictures:
    story_number = (number - 1) // BATCH_SIZE + 1
    target_dir = os.path.join(target_root, f"Story{story_number}")

    os.rename(os.path.join(source_dir, filename), os.path.join(target_dir, filename))
    print(f"{filename} -> {target_dir}")

print(f"Moved {len(pictures)} pictures.")
