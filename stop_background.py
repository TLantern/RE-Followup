"""
Stop the SMS auto-responder background service.
"""
import os
import signal
import subprocess
from pathlib import Path

def stop_background_service():
    """Stop the background SMS auto-responder service"""
    
    current_dir = Path(__file__).parent.absolute()
    pid_file = current_dir / "auto_responder.pid"
    
    if not pid_file.exists():
        print("❌ No background service found (PID file missing)")
        return False
    
    try:
        # Read the PID
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        print(f"🔍 Found background service with PID: {pid}")
        
        # Try to terminate the process
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/F', '/PID', str(pid)], 
                         capture_output=True, check=True)
        else:  # Unix/Linux/Mac
            os.kill(pid, signal.SIGTERM)
        
        # Remove the PID file
        pid_file.unlink()
        
        print("✅ SMS Auto-Responder background service stopped successfully!")
        return True
        
    except (ValueError, OSError, subprocess.CalledProcessError) as e:
        print(f"❌ Failed to stop background service: {e}")
        # Clean up PID file if process doesn't exist
        if pid_file.exists():
            pid_file.unlink()
        return False

def check_service_status():
    """Check if the background service is running"""
    
    current_dir = Path(__file__).parent.absolute()
    pid_file = current_dir / "auto_responder.pid"
    
    if not pid_file.exists():
        print("📴 SMS Auto-Responder is not running")
        return False
    
    try:
        with open(pid_file, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process is still running
        if os.name == 'nt':  # Windows
            result = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'], 
                                  capture_output=True, text=True)
            is_running = str(pid) in result.stdout
        else:  # Unix/Linux/Mac
            try:
                os.kill(pid, 0)  # Doesn't actually kill, just checks if process exists
                is_running = True
            except OSError:
                is_running = False
        
        if is_running:
            print(f"✅ SMS Auto-Responder is running (PID: {pid})")
            print(f"🌐 Server should be accessible at http://localhost:5000")
            return True
        else:
            print(f"❌ Process {pid} is not running (cleaning up PID file)")
            pid_file.unlink()
            return False
            
    except (ValueError, OSError) as e:
        print(f"❌ Error checking service status: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        check_service_status()
    else:
        stop_background_service() 