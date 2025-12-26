"""Test cases for install.py security features."""
from src.commands.install import (
    validate_version_format,
)


def test_validate_version_format():
    """Test version format validation."""
    # Valid versions
    assert validate_version_format("3.11.0") == True
    assert validate_version_format("3.12.5") == True
    assert validate_version_format("2.7.18") == True
    assert validate_version_format("3.10.0") == True
    
    # Invalid versions
    assert validate_version_format("3.11") == False
    assert validate_version_format("3.11.0.1") == False
    assert validate_version_format("3.11.0a1") == False
    assert validate_version_format("v3.11.0") == False
    assert validate_version_format("3.11.0-beta") == False
    assert validate_version_format("../../../etc/passwd") == False
    assert validate_version_format("3;11;0") == False
    assert validate_version_format("") == False
    assert validate_version_format("abc.def.ghi") == False
    
    print("✓ All version format validation tests passed")



if __name__ == "__main__":
    print("Running install security tests...\n")
    
    test_validate_version_format()

    
    print("\n✅ All install security tests passed!")
