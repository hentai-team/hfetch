import platform
import os
import datetime
import socket
from typing import List, Dict
from colorama import Fore, Style

# Глобальные константы

def hex_to_rgb(hex_color: str) -> tuple:
    """Конвертирует HEX цвет в RGB"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Определяем кастомный цвет для логотипа
LOGO_COLOR = '#50FFA0'
r, g, b = hex_to_rgb(LOGO_COLOR)
TERMINAL_LOGO = f"""
\x1b[38;2;{r};{g};{b}m              ..             ..         
\x1b[38;2;{r};{g};{b}m           .lOKKk;        .lOKKk:.      
\x1b[38;2;{r};{g};{b}m         .l0WMMMMO.       oWMMMMNl      
\x1b[38;2;{r};{g};{b}m       .l0WMMMMWKc        lNMMMMM0,     
\x1b[38;2;{r};{g};{b}m     .l0WMMMMWKo.         .OMMMMMWd.    
\x1b[38;2;{r};{g};{b}m   .l0WMMMMWKo.            :XMMMMMX;    
\x1b[38;2;{r};{g};{b}m .c0WMMMMWKl.              .xWMMMMMk.   
\x1b[38;2;{r};{g};{b}mc0WMMMMWKl.                 ,KMMMMMNc   
\x1b[38;2;{r};{g};{b}mNMMMMMWk'                    oWMMMMMO'  
\x1b[38;2;{r};{g};{b}mOWMMMMWKl.                   'OMMMMMWo  
\x1b[38;2;{r};{g};{b}m.c0WMMMMWKl.                  cNMMMMMK; 
\x1b[38;2;{r};{g};{b}m  .c0WMMMMWKl.                .kWMMMMWx.
\x1b[38;2;{r};{g};{b}m    .c0WMMMMWKo.               ;KMMMMMXc
\x1b[38;2;{r};{g};{b}m      .l0WMMMMWKo.             .dWMMMMM0
\x1b[38;2;{r};{g};{b}m        .l0WMMMMWk.             '0MMMMMW
\x1b[38;2;{r};{g};{b}m          .l0WMMWd.              :KWMMWO
\x1b[38;2;{r};{g};{b}m            .;ll;.                .:ll;.{Style.RESET_ALL}"""

class SystemInfo:
    def __init__(self):
        self.os_info = self._get_os_info()
        self.hw_info = self._get_hardware_info()
        self.user_info = self._get_user_info()
        self.uptime = self._get_uptime()
        
    def _get_os_info(self) -> Dict[str, str]:
        """Получает информацию об операционной системе"""
        info = {
            "name": platform.system(),
            "version": platform.version(),
            "arch": platform.machine()
        }
        
        system = platform.system().lower()
        if system == "windows":
            info["name"] = f"Microsoft Windows {platform.release()}"
            info["build"] = platform.version()
        elif system == "linux":
            try:
                import distro
                info["name"] = distro.name(pretty=True)
                info["version"] = distro.version(pretty=True)
            except ImportError:
                pass
        elif system == "darwin":
            info["name"] = "macOS"
            info["version"] = platform.mac_ver()[0]
            
        return info
        
    def _get_hardware_info(self) -> Dict[str, str]:
        """Получает информацию об аппаратном обеспечении"""
        info = {}
        
        try:
            import psutil
            
            # CPU информация - делаем более компактной
            cpu_name = platform.processor()
            if platform.system() == "Windows":
                # Для Windows убираем лишнюю информацию из имени процессора
                cpu_name = cpu_name.split(',')[0].rstrip()
            
            # Получаем частоту
            cpu_freq = psutil.cpu_freq()
            cpu_freq_str = f" @ {cpu_freq.current/1000:.1f}GHz" if cpu_freq else ""
            
            info["cpu"] = f"{cpu_name}{cpu_freq_str}"
            info["cpu_cores"] = psutil.cpu_count(logical=False)
            info["cpu_threads"] = psutil.cpu_count()
            info["cpu_usage"] = f"{psutil.cpu_percent()}%"
            
            # RAM
            mem = psutil.virtual_memory()
            info["ram_total"] = self._format_bytes(mem.total)
            info["ram_used"] = self._format_bytes(mem.used)
            info["ram_free"] = self._format_bytes(mem.free)
            info["ram_percent"] = f"{mem.percent}%"
            
            # Disk - используем корневой диск для текущей ОС
            root = '/' if platform.system() != 'Windows' else 'C:\\'
            disk = psutil.disk_usage(root)
            info["disk_total"] = self._format_bytes(disk.total)
            info["disk_used"] = self._format_bytes(disk.used)
            info["disk_free"] = self._format_bytes(disk.free)
            info["disk_percent"] = f"{disk.percent}%"
            
        except ImportError:
            # Fallback значения
            info.update({
                "cpu": platform.processor() or "Unknown CPU",
                "cpu_cores": "N/A", "cpu_threads": "N/A",
                "cpu_usage": "N/A", "ram_total": "N/A",
                "ram_used": "N/A", "ram_free": "N/A",
                "ram_percent": "N/A", "disk_total": "N/A",
                "disk_used": "N/A", "disk_free": "N/A",
                "disk_percent": "N/A"
            })

        # GPU детекция для всех платформ
        try:
            if platform.system() == "Windows":
                import GPUtil
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    info["gpu"] = f"{gpu.name} ({gpu.memoryTotal}MB)"
                else:
                    info["gpu"] = "No GPU detected"
            else:
                # Для Linux можно добавить lspci
                info["gpu"] = "GPU detection not supported on this platform"
        except:
            info["gpu"] = "GPU detection failed"
            
        return info
        
    def _get_user_info(self) -> Dict[str, str]:
        """Получает информацию о пользователе и системе"""
        import getpass
        
        info = {
            "hostname": socket.gethostname(),
            "username": getpass.getuser(),
            # Убираем привязку к hbash
            "shell": os.environ.get("SHELL", os.environ.get("COMSPEC", "unknown")),
            "terminal": os.environ.get("TERM", os.environ.get("TERMINAL", "unknown"))
        }
        
        try:
            # Получаем основной IP-адрес
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            info["local_ip"] = s.getsockname()[0]
            s.close()
        except:
            info["local_ip"] = "127.0.0.1"
            
        return info
        
    def _get_uptime(self) -> str:
        """Получает время работы системы"""
        try:
            import psutil
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.datetime.now() - boot_time
            return str(uptime).split('.')[0]
        except:
            return "N/A"
                
    def _format_bytes(self, bytes: int) -> str:
        """Форматирует байты в человекочитаемый вид"""
        try:
            for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                if bytes < 1024:
                    return f"{bytes:.1f}{unit}"
                bytes /= 1024
            return f"{bytes:.1f}PB"
        except:
            return "N/A"
        
    def display(self):
        """Displays system information"""
        os_color = Fore.CYAN
        hw_color = Fore.GREEN
        user_color = Fore.YELLOW
        reset = Style.RESET_ALL
        
        # Разделяем лого на строки
        logo_lines = TERMINAL_LOGO.split('\n')
        info_lines = []
        
        # Формируем строки информации с новым форматированием
        info_lines.extend([
            f"{user_color}{self.user_info['username']}{reset}@{user_color}{self.user_info['hostname']}{reset}",
            f"{Fore.BLUE}════════════════{Style.RESET_ALL}",  # Горизонтальная линия вместо стрелок
            f"{os_color}OS:{reset} {self.os_info['name']}",
            f"{os_color}Kernel:{reset} {self.os_info['version']}",
            f"{os_color}Uptime:{reset} {self.uptime}",
            f"{os_color}Shell:{reset} {self.user_info['shell']}",
            f"{hw_color}CPU:{reset} {self.hw_info['cpu']}",
            f"{hw_color}Memory:{reset} {self.hw_info['ram_used']} / {self.hw_info['ram_total']} ({self.hw_info['ram_percent']})",
            f"{hw_color}Disk:{reset} {self.hw_info['disk_used']} / {self.hw_info['disk_total']} ({self.hw_info['disk_percent']})",
            "",
            f"{Fore.BLACK}███{Fore.RED}███{Fore.GREEN}███{Fore.YELLOW}███{Fore.BLUE}███{Fore.MAGENTA}███{Fore.CYAN}███{Fore.WHITE}███{Style.RESET_ALL}"
        ])

        # Убираем пустую первую строку логотипа
        if not logo_lines[0].strip():
            logo_lines = logo_lines[1:]
            
        # Объединяем лого и информацию, добавляя отступ между ними
        max_logo_length = max(len(line) for line in logo_lines)
        for i in range(max(len(logo_lines), len(info_lines))):
            logo = logo_lines[i] if i < len(logo_lines) else " " * max_logo_length
            info = info_lines[i] if i < len(info_lines) else ""
            print(f"{logo}    {info}")  # Увеличиваем отступ между лого и информацией

def main(args: List[str]) -> int:
    """
    Help about command line arguments for hfetch utility
    
    Usage: hfetch [options]
    -v, --version    Show version
    -h, --help       Show help
    """
    if args and args[0] in ['-v', '--version']:
        print("hfetch, version 1.0")
        return 0
        
    if args and args[0] in ['-h', '--help']:
        print(main.__doc__)
        return 0
        
    try:
        system_info = SystemInfo()
        system_info.display()
        return 0
    except Exception as e:
        print(f"{Fore.RED}Ошибка при получении информации о системе: {str(e)}{Style.RESET_ALL}")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv[1:]))