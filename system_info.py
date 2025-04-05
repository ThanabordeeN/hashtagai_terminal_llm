"""
System Information Module for HashtagAI Terminal.

This module handles collection of system information.
"""
import platform
import distro

def get_system_info():
    """Get detailed system information."""
    os_info = platform.system() + " " + platform.release()
    
    if platform.system() == "Linux":
        try:
            os_info = distro.name(pretty=True)
        except ImportError:
            # Fallback if distro module not available
            try:
                with open("/etc/os-release") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME="):
                            os_info = line.split("=")[1].strip().strip('"')
                            break
            except:
                pass
    
    return os_info