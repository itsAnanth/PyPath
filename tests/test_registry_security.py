"""Comprehensive test cases for registry security validation."""
from src.utils.registry import validate_path_entry, validate_path_value


def test_validate_path_entry_valid_paths():
    """Test validation of valid PATH entries."""
    valid_paths = [
        "C:\\Python311",
        "C:\\Program Files\\Python311",
        "C:\\Users\\Admin\\AppData\\Local\\Programs\\Python",
        "E:\\tools\\python",
        "C:\\Windows\\System32",
        "%USERPROFILE%\\AppData\\Local\\Programs",
        "D:\\Dev\\Python312\\Scripts",
    ]
    
    for path in valid_paths:
        assert validate_path_entry(path) == True, f"Failed for valid path: {path}"
    
    print(f"✓ All {len(valid_paths)} valid paths passed")


def test_validate_path_entry_invalid_paths():
    """Test detection of invalid/malicious PATH entries."""
    invalid_paths = [
        "C:\\Program Files\\..\\Windows\\System32",  # Path traversal
        "C:\\Users\\..\\..\\etc\\passwd",  # Path traversal
        "C:\\Valid<Script>",  # Suspicious character
        "C:\\Valid>output.txt",  # Redirection character
        "C:\\Valid|pipe",  # Pipe character
        'C:\\Valid"quote',  # Quote character
        "C:\\Valid?wildcard",  # Wildcard
        "C:\\Valid*pattern",  # Wildcard
        "C:\\Path\x00null",  # Null byte
        "",  # Empty string
        "   ",  # Only whitespace
        "../../../etc/passwd",  # Unix-style path traversal
        "C:/Path/../Traversal",  # Forward slash with traversal
    ]
    
    for path in invalid_paths:
        assert validate_path_entry(path) == False, f"Failed to detect invalid path: {repr(path)}"
    
    print(f"✓ All {len(invalid_paths)} invalid paths detected")


def test_validate_path_value_valid():
    """Test validation of complete valid PATH values."""
    valid_paths = [
        "C:\\Python311",
        "C:\\Python311;C:\\Python311\\Scripts",
        "C:\\Windows\\System32;C:\\Windows;C:\\Windows\\System32\\Wbem",
        ";".join([
            "C:\\Python311",
            "C:\\Python311\\Scripts",
            "%USERPROFILE%\\AppData\\Local\\Programs",
            "C:\\Windows\\System32"
        ]),
    ]
    
    for path_value in valid_paths:
        assert validate_path_value(path_value) == True, f"Failed for valid PATH: {path_value}"
    
    print(f"✓ All {len(valid_paths)} valid PATH values passed")


def test_validate_path_value_invalid():
    """Test detection of invalid PATH values."""
    # Single entry with traversal
    assert validate_path_value("C:\\Windows\\..\\..\\etc\\passwd") == False
    print("✓ Single entry with traversal detected")
    
    # Valid entry followed by invalid entry
    assert validate_path_value("C:\\Python311;C:\\Windows\\..\\System32") == False
    print("✓ Mixed valid/invalid entries detected")
    
    # Null byte in path
    assert validate_path_value("C:\\Python311\x00;C:\\Windows") == False
    print("✓ Null byte in PATH detected")
    
    # Empty PATH value
    assert validate_path_value("") == False
    print("✓ Empty PATH value rejected")


def test_validate_path_value_length_limit():
    """Test PATH value length limitations."""
    # Create a PATH value just under the limit (2047 characters)
    short_entry = "C:\\Python311\\Scripts;"
    num_entries = 2000 // len(short_entry)
    valid_long_path = short_entry * num_entries
    
    # Should pass if under limit
    if len(valid_long_path) <= 2047:
        assert validate_path_value(valid_long_path) == True
        print(f"✓ Long PATH value ({len(valid_long_path)} chars) accepted")
    
    # Create a PATH value exceeding the limit
    too_long_path = "C:\\Python311\\Scripts;" * 200  # Will exceed 2047
    assert validate_path_value(too_long_path) == False
    print(f"✓ Excessive PATH length ({len(too_long_path)} chars) rejected")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    # Single semicolon
    assert validate_path_value("C:\\Python311;") == True
    print("✓ Trailing semicolon handled")
    
    # Multiple consecutive semicolons (empty entries)
    assert validate_path_value("C:\\Python311;;C:\\Windows") == True
    print("✓ Consecutive semicolons handled")
    
    # Path with spaces
    assert validate_path_entry("C:\\Program Files\\Python 3.11") == True
    print("✓ Paths with spaces accepted")
    
    # Path with environment variables
    assert validate_path_entry("%SYSTEMROOT%\\System32") == True
    print("✓ Environment variables accepted")


def test_security_attack_vectors():
    """Test against known security attack patterns."""
    attack_vectors = [
        ("Path Traversal (Windows)", "C:\\Windows\\..\\..\\..\\etc"),
        ("Path Traversal (Mixed)", "C:/Windows/../../../etc"),
        ("Command Injection", "C:\\Python311 & del /f *.*"),
        ("Script Injection", "C:\\Path<script>alert('xss')</script>"),
        ("Null Byte Attack", "C:\\Python311\x00.exe"),
        ("Pipe Injection", "C:\\Python311 | powershell.exe"),
        ("Redirection Attack", "C:\\Python311 > C:\\output.txt"),
        ("Wildcard Expansion", "C:\\Windows\\System32\\*.dll"),
    ]
    
    for name, attack in attack_vectors:
        if '\x00' in attack or any(char in attack for char in ['..', '<', '>', '|', '?', '*']):
            result = validate_path_entry(attack)
            assert result == False, f"{name} attack not detected: {attack}"
            print(f"✓ {name} blocked")


def test_common_legitimate_paths():
    """Test that common legitimate Windows paths are accepted."""
    common_paths = [
        "C:\\Windows\\System32",
        "C:\\Program Files",
        "C:\\Program Files (x86)",
        "%SYSTEMROOT%\\System32\\WindowsPowerShell\\v1.0",
        "%USERPROFILE%\\AppData\\Local\\Programs\\Python\\Python311",
        "C:\\ProgramData\\chocolatey\\bin",
        "C:\\Users\\Public\\Documents",
        "%APPDATA%\\npm",
    ]
    
    for path in common_paths:
        assert validate_path_entry(path) == True, f"Legitimate path rejected: {path}"
    
    print(f"✓ All {len(common_paths)} common legitimate paths accepted")


if __name__ == "__main__":
    print("Running registry security tests...\n")
    
    test_validate_path_entry_valid_paths()
    test_validate_path_entry_invalid_paths()
    test_validate_path_value_valid()
    test_validate_path_value_invalid()
    test_validate_path_value_length_limit()
    test_edge_cases()
    test_security_attack_vectors()
    test_common_legitimate_paths()
    
    print("\n✅ All registry security tests passed!")
