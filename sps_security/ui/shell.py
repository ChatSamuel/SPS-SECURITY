from sps_security.ui.banner import show_banner
from sps_security.actions.cloud_action import run_cloud
from sps_security.actions.apk_action import run_apk
from sps_security.actions.monitor_action import run_monitor
from sps_security.actions.cleanup_action import cleanup_quarantine


def show_menu():
    print("""
=============================
        SPS MENU
=============================

[1] Cloud Scan
[2] APK Scan
[3] Real-time Monitor
[4] Cleanup Quarantine
[5] Help
[6] Exit

Type option number or command
""")


def start_shell():
    show_banner()

    while True:
        show_menu()
        command = input("sps › ").strip()

        if command == "1":
            file = input("Enter file path: ")
            run_cloud(file)

        elif command == "2":
            file = input("Enter APK path: ")
            run_apk(file)

        elif command == "3":
            path = input("Enter path to monitor (default '.'): ") or "."
            run_monitor(path)

        elif command == "4":
            cleanup_quarantine()

        elif command == "5":
            print("""
Commands:

cloud <file>
apk <file>
monitor <path>
cleanup
exit
""")

        elif command == "6":
            print("Exiting...")
            break

        elif command.startswith("cloud "):
            file = command.split(" ", 1)[1]
            run_cloud(file)

        elif command.startswith("apk "):
            file = command.split(" ", 1)[1]
            run_apk(file)

        elif command.startswith("monitor "):
            path = command.split(" ", 1)[1]
            run_monitor(path)

        elif command == "cleanup":
            cleanup_quarantine()

        elif command == "exit":
            break

        else:
            print("Invalid option")
