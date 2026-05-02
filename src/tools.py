"""Custom tools for the local Ollama assistant."""
from datetime import datetime
import platform
import subprocess
import json


class CustomTools:
    """Custom tool implementations for agent tasks."""

    @staticmethod
    def get_current_time() -> str:
        """Get the current date and time."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_system_info() -> str:
        """Get system information."""
        info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "python_version": platform.python_version(),
        }
        return json.dumps(info, indent=2)

    @staticmethod
    def execute_command(command: str) -> str:
        """
        Execute a shell command and return the output.
        
        Args:
            command: Shell command to execute
            
        Returns:
            Command output or error message
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
        except subprocess.TimeoutExpired:
            return "Error: Command timed out (30 seconds)"
        except Exception as e:
            return f"Error executing command: {str(e)}"

    @staticmethod
    def list_files(directory: str = ".") -> str:
        """
        List files and directories in a given path.
        
        Args:
            directory: Path to list (default: current directory)
            
        Returns:
            Formatted list of files and directories
        """
        try:
            import os
            items = os.listdir(directory)
            result = f"Contents of '{directory}':\n"
            for item in sorted(items):
                path = os.path.join(directory, item)
                if os.path.isdir(path):
                    result += f"  [DIR]  {item}/\n"
                else:
                    size = os.path.getsize(path)
                    result += f"  [FILE] {item} ({size} bytes)\n"
            return result
        except Exception as e:
            return f"Error listing directory: {str(e)}"

    @staticmethod
    def search_files(pattern: str, directory: str = ".") -> str:
        """
        Search for files matching a pattern.
        
        Args:
            pattern: File pattern to search for (e.g., "*.py")
            directory: Search directory (default: current directory)
            
        Returns:
            List of matching files
        """
        try:
            import glob
            matches = glob.glob(f"{directory}/**/{pattern}", recursive=True)
            if matches:
                return "Found files:\n" + "\n".join(matches)
            else:
                return f"No files matching '{pattern}' found"
        except Exception as e:
            return f"Error searching files: {str(e)}"

    @staticmethod
    def count_files(pattern: str, directory: str = ".") -> str:
        """
        Count files matching a pattern.
        
        Args:
            pattern: File pattern to search for (e.g., "*.py")
            directory: Search directory (default: current directory)
            
        Returns:
            Count of matching files and a short list of matches
        """
        try:
            import glob
            matches = glob.glob(f"{directory}/**/{pattern}", recursive=True)
            count = len(matches)
            if count == 0:
                return f"Found 0 files matching '{pattern}' in '{directory}'"
            sample = "\n".join(matches[:20])
            more = "" if count <= 20 else f"\n...and {count - 20} more"
            return (
                f"Found {count} files matching '{pattern}' in '{directory}':\n"
                f"{sample}{more}"
            )
        except Exception as e:
            return f"Error counting files: {str(e)}"


def get_custom_tools():
    """
    Get custom tool functions.
    
    Returns:
        Dictionary of custom tool functions
    """
    return {
        "get_current_time": CustomTools.get_current_time,
        "get_system_info": CustomTools.get_system_info,
        "execute_command": CustomTools.execute_command,
        "list_files": CustomTools.list_files,
        "search_files": CustomTools.search_files,
        "count_files": CustomTools.count_files,
    }
