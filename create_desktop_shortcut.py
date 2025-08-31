import os
import sys
import platform

def create_desktop_shortcut():
    """Create a desktop shortcut for the automation system"""
    
    # Get the current working directory (project directory)
    project_dir = r"C:\Users\ciami\OneDrive\Área de Trabalho\projeto"
    
    # Get the desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Path to the batch file
    batch_file_path = os.path.join(project_dir, "run_system.bat")
    
    # Check if we're on Windows
    if platform.system() == "Windows":
        try:
            # Create .lnk shortcut using Windows Script Host
            import win32com.client
            
            # Create shortcut
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut_path = os.path.join(desktop_path, "Sistema Automação Inteligente.lnk")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = batch_file_path
            shortcut.WorkingDirectory = project_dir
            shortcut.IconLocation = "shell32.dll, 3"
            shortcut.save()
            
            print("Atalho criado com sucesso na área de trabalho!")
            print(f"Atalho: {shortcut_path}")
            
        except ImportError:
            # If win32com is not available, create a simple .bat shortcut on desktop
            desktop_batch_path = os.path.join(desktop_path, "Sistema Automação Inteligente.bat")
            with open(desktop_batch_path, 'w') as f:
                f.write(f'@echo off\n')
                f.write(f'cd /d "{project_dir}"\n')
                f.write(f'"{batch_file_path}"\n')
            
            print("Atalho criado com sucesso na área de trabalho!")
            print(f"Atalho: {desktop_batch_path}")
    else:
        print("Este script é otimizado para Windows.")
        print("Para criar um atalho no Linux/Mac, você pode copiar o arquivo run_system.bat para a área de trabalho.")

if __name__ == "__main__":
    create_desktop_shortcut()