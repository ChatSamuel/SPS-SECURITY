import os
import sys
import time

banner = """
███████╗██████╗ ███████╗
██╔════╝██╔══██╗██╔════╝
███████╗██████╔╝███████╗
╚════██║██╔═══╝ ╚════██║
███████║██║     ███████║
╚══════╝╚═╝     ╚══════╝

   SPS - SECURITY
 Malware Detection Tool
 Author: Samuel Pontes
"""

signatures = [
    "powershell",
    "cmd.exe",
    "wget",
    "curl",
    "base64"
]


def loading():
    print("Inicializando SPS-SECURITY", end="")
    
    for i in range(5):
        time.sleep(0.5)
        print(".", end="")
        sys.stdout.flush()

    print("\nSistema carregado!\n")


def scan_file(file_path):

    if "sps_security.py" in file_path:
        return False

    try:
        with open(file_path, "r", errors="ignore") as file:
            content = file.read()

        for sig in signatures:

            if sig in content:

                print("⚠️ POSSÍVEL MALWARE:", sig, "no arquivo", file_path)

                return True

    except:
        pass

    return False


def scan_folder(folder):

    arquivos_verificados = 0
    ameacas = 0

    print("\n🔍 Iniciando análise...\n")

    for root, dirs, files in os.walk(folder):

        for file in files:

            path = os.path.join(root, file)

            arquivos_verificados += 1

            if scan_file(path):
                ameacas += 1

    print("\n✔ Scan finalizado")
    print("Arquivos analisados:", arquivos_verificados)
    print("Ameaças encontradas:", ameacas)
    print("")


def menu():

    print("1 - Escanear arquivo")
    print("2 - Escanear pasta")
    print("3 - Sair")

    escolha = input("\nEscolha uma opção: ")

    return escolha


print(banner)

loading()

while True:

    opcao = menu()

    if opcao == "1":

        arquivo = input("Digite o caminho do arquivo: ")

        if scan_file(arquivo):
            print("⚠️ Arquivo suspeito detectado\n")
        else:
            print("✔ Nenhuma ameaça encontrada\n")

    elif opcao == "2":

        pasta = input("Digite o caminho da pasta: ")

        scan_folder(pasta)

    elif opcao == "3":

        print("Encerrando SPS-SECURITY...\n")

        break
