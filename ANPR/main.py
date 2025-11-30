import os
from ANPR import ANPR


def main():
    # Create engine once
    engine = ANPR()

    # Folder with test images
    input_folder = "./ANPR/img/test"

    # Where to save results
    output_folder = "./ANPR/outputs"
    os.makedirs(output_folder, exist_ok=True)

    # All image names you want to process
    images = ["car3.png", "car4.png"]

    print("\n=== Starting ANPR Batch Processing ===\n")

    for name in images:
        image_path = f"{input_folder}/{name}"
        print(f"Processing: {image_path}")

        # Run detection
        text = engine.detect(image_path)
        print(f" → Plate Detected: {text}")

        # Render result
        rendered = engine.render()

        # Save outputs
        prefix = name.split('.')[0]   # e.g. "image11"
        engine.save(output_folder, prefix)

    print("\n=== Finished Processing All Images ===\n")


if __name__ == "__main__":
    main()
