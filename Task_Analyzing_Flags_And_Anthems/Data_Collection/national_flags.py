import os
import subprocess
import shutil


WORKING_DIR = r"C:\Users\ASUS\country-flags"

IMPORT_DIR = os.path.join(WORKING_DIR, "flags")

def run_npm_script():
    num = input("Enter the image size (integer): ").strip()

    if not num.isdigit():
        print("Please enter a valid integer.")
        return
    
    num = int(num)
    output_dir = os.path.join(WORKING_DIR, f"png{num}px")
    target_dir = os.path.join(WORKING_DIR, f"{num}px")

    command = f"npm run build-pngs -- {num}:"

    try:
        process = subprocess.run(command, cwd=WORKING_DIR, shell=True, check=True, text=True, capture_output=True)
        print("Output:\n", process.stdout)

        if os.path.exists(output_dir):
            print(f"\nImages successfully generated in {output_dir}.\n")
            import_generated_images(output_dir, target_dir)
        else:
            print("Error: Image generation failed.")
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr)


def import_generated_images(source_dir, target_dir):
    os.makedirs(target_dir, exist_ok=True)

    files = [f for f in os.listdir(source_dir) if f.endswith(".png")]

    files = files[:150]
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    for file in files:
        shutil.copy2(os.path.join(source_dir, file), os.path.join(target_dir, file))
    
    print(f"Images successfully imported to {target_dir}.")


if __name__ == "__main__":
    run_npm_script()
