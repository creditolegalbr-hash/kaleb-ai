import sys
import os

print("Testing YAML import...")
try:
    import yaml
    print("✓ PyYAML is installed")
    
    # Test loading a simple YAML
    test_yaml = """
    test:
      value: "success"
    """
    
    result = yaml.safe_load(test_yaml)
    print(f"✓ YAML parsing works: {result}")
    
except ImportError as e:
    print(f"✗ PyYAML is not installed: {e}")
    print("Installing PyYAML...")
    try:
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyYAML"])
        print("✓ PyYAML installed successfully")
    except Exception as install_error:
        print(f"✗ Failed to install PyYAML: {install_error}")

except Exception as e:
    print(f"✗ Error testing YAML: {e}")

print("\nTesting complete.")