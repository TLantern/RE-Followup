"""
Run the SMS auto-responder in the background on Windows.
"""
import subprocess
import sys
import os
import time
import logging
from pathlib import Path

def run_in_background():
    """Run the Flask app in the background using subprocess"""
    
    # Get the current directory
    current_dir = Path(__file__).parent.absolute()
    
    # Path to main.py
    main_script = current_dir / "main.py"
    
    # Create logs directory if it doesn't exist
    logs_dir = current_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Log file paths
    log_file = logs_dir / "auto_responder.log"
    error_file = logs_dir / "auto_responder_error.log"
    
    print(f"🚀 Starting SMS Auto-Responder in background...")
    print(f"📁 Working directory: {current_dir}")
    print(f"📜 Logs will be saved to: {log_file}")
    print(f"❌ Errors will be saved to: {error_file}")
    
    try:
        # Start the process in the background
        with open(log_file, 'w') as stdout_file, open(error_file, 'w') as stderr_file:
            process = subprocess.Popen(
                [sys.executable, str(main_script)],
                stdout=stdout_file,
                stderr=stderr_file,
                cwd=str(current_dir),
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
            )
        
        print(f"✅ SMS Auto-Responder started successfully!")
        print(f"🔢 Process ID: {process.pid}")
        print(f"🌐 Server should be running on http://localhost:5000")
        print(f"🔍 Monitor logs with: tail -f {log_file}")
        print(f"❌ Check errors with: tail -f {error_file}")
        print("\n📝 To stop the service, run: python stop_background.py")
        
        # Save the PID for later stopping
        pid_file = current_dir / "auto_responder.pid"
        with open(pid_file, 'w') as f:
            f.write(str(process.pid))
        
        return process.pid
        
    except Exception as e:
        print(f"❌ Failed to start SMS Auto-Responder: {e}")
        return None

if __name__ == "__main__":
    run_in_background() 