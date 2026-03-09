import os

path = "data/raw/India_Air_Quality_2024_Raw"

print(f"Checking contents of: {path}")
try:
    if os.path.exists(path):
        print("✅ Folder exists.")
        contents = os.listdir(path)
        print(f"📂 Contents: {contents}")
        
        # Check one level deeper if there is a subfolder
        for item in contents:
            subpath = os.path.join(path, item)
            if os.path.isdir(subpath):
                print(f"   ➡️ Inside '{item}': {os.listdir(subpath)[:5]} ...")
    else:
        print("❌ Folder NOT found. Check your spelling.")
except Exception as e:
    print(f"Error: {e}")