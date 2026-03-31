# Licensed under CC BY-NC-SA 4.0
import subprocess
import os
import re
import csv

def analyze_stl(stl_path, config_path):
    print(f"Analyzing {stl_path}...")
    
    # We use --info first to get volume and dimensions
    try:
        info_out = subprocess.check_output(["prusa-slicer", "--info", stl_path], stderr=subprocess.STDOUT).decode()
        volume = re.search(r"volume = ([\d\.]+)", info_out).group(1)
        size_x = re.search(r"size_x = ([\d\.]+)", info_out).group(1)
        size_y = re.search(r"size_y = ([\d\.]+)", info_out).group(1)
        size_z = re.search(r"size_z = ([\d\.]+)", info_out).group(1)
    except Exception as e:
        print(f"Error getting info for {stl_path}: {e}")
        return None

    # We attempt to slice to get time/weight, but we use a large bed to avoid volume errors
    # And we suppress stability warnings by redirecting stderr
    temp_gcode = "/tmp/temp_slice.gcode"
    try:
        # Note: If the slicer returns 1 due to warnings, we still try to read the gcode if it exists
        subprocess.run([
            "prusa-slicer", "--export-gcode", 
            "--load", config_path,
            "--center", "250,250",
            "--bed-shape", "0x0,500x0,500x500,0x500",
            "--output", temp_gcode,
            stl_path
        ], capture_output=True)
        
        with open(temp_gcode, 'r') as f:
            content = f.read()
            # PrusaSlicer embeds stats at the end of the file
            # Format: ; estimated printing time (normal mode) = 4h 22m 15s
            # Format: ; filament used [g] = 45.2
            time_match = re.search(r"estimated printing time .* = (.*)", content)
            weight_match = re.search(r"filament used \[g\] = ([\d\.]+)", content)
            
            print_time = time_match.group(1) if time_match else "Unknown"
            weight = weight_match.group(1) if weight_match else "Unknown"
    except Exception:
        print_time = "Analysis Error"
        weight = "Analysis Error"
    finally:
        if os.path.exists(temp_gcode):
            os.remove(temp_gcode)

    return {
        "Part": os.path.basename(stl_path),
        "Dimensions (mm)": f"{size_x}x{size_y}x{size_z}",
        "Volume (mm³)": volume,
        "Est. Weight (g)": weight,
        "Est. Print Time": print_time
    }

def main():
    config_path = "design/config/manufacturing_profile.ini"
    results = []
    
    stl_dirs = [
        "design/parts/common/stls",
        "design/parts/tw4/stls"
    ]
    
    for d in stl_dirs:
        if not os.path.exists(d): continue
        for f in os.listdir(d):
            if f.endswith(".stl"):
                res = analyze_stl(os.path.join(d, f), config_path)
                if res:
                    results.append(res)
    
    output_path = "design/MANUFACTURING_REPORT.csv"
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Part", "Dimensions (mm)", "Volume (mm³)", "Est. Weight (g)", "Est. Print Time"])
        writer.writeheader()
        writer.writerows(results)
    print(f"\nReport generated at {output_path}")

if __name__ == "__main__":
    main()
