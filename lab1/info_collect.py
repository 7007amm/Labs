import json, os, platform, sys


info = {
        "operating_system": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "platform": platform.platform(),
            "architecture": platform.architecture()[0],
            "linkage": platform.architecture()[1],
            "machine": platform.machine(),
            "node_name": platform.node(),
        },
        "hardware_summary": {
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
        },
        "python_environment": {
            "python_version": platform.python_version(),
            "python_compiler": platform.python_compiler(),
            "python_implementation": platform.python_implementation(),
            "executable_path": sys.executable,
        },
}

with open("system_info.json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=4)

print(f"За информацией о системе обращаться к файлу: system_info.json")
