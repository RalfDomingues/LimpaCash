import os
import shutil
import threading
import ctypes
import sys
from pathlib import Path

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    params = " ".join(f'"{arg}"' for arg in sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{sys.argv[0]}" {params}', None, 1)
    sys.exit()

def limpar_pasta(caminho, pastas_limpeza_cache):
    caminho = str(Path(caminho).resolve())
    if caminho in pastas_limpeza_cache:
        return
    pastas_limpeza_cache.add(caminho)

    print(f"Iniciando limpeza da pasta: {caminho}")
    pasta = Path(caminho)
    if not pasta.exists():
        print(f"Pasta não existe: {caminho}")
        return

    for item in pasta.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir() and not item.is_symlink():
                shutil.rmtree(item)
        except Exception as e:
            msg = str(e).lower()
            if "being used by another process" in msg or "acesso negado" in msg:
                print(f"Aviso: Não foi possível excluir {item}: {e}")
            else:
                print(f"Erro: {item}: {e}")
    print(f"Limpeza concluída: {caminho}")

def limpar_lixeira():
    try:
        SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW
        result = SHEmptyRecycleBin(None, None, 0)
        if result == 0:
            print("Lixeira esvaziada com sucesso.")
        else:
            print(f"Falha ao esvaziar a lixeira. Código de erro: {result}")
    except Exception as e:
        print(f"Erro ao tentar esvaziar a lixeira: {e}")

def input_aguardar(mensagem, timeout):
    resposta = [None]
    def ask():
        resposta[0] = input(mensagem)
    thread = threading.Thread(target=ask)
    thread.daemon = True
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        return None
    return resposta[0]

def limpar_temporarias_usuarios(pastas_limpeza_cache):
    users_dir = Path("C:/Users")
    if not users_dir.exists():
        print("Pasta C:/Users não encontrada.")
        return

    pastas_para_limpar_por_usuario = [
        "AppData\\Local\\Temp",
        "AppData\\Roaming\\Microsoft\\Windows\\Recent",
        "AppData\\Local\\Microsoft\\Windows\\INetCache",
        "AppData\\Local\\Microsoft\\Windows\\WebCache",
    ]

    for user_folder in users_dir.iterdir():
        if user_folder.is_dir():
            nome = user_folder.name.lower()
            if nome in ["default", "defaultuser0", "public", "all users"]:
                continue

            for subpasta in pastas_para_limpar_por_usuario:
                caminho = user_folder / subpasta
                if caminho.exists():
                    limpar_pasta(str(caminho), pastas_limpeza_cache)

def main():
    if not is_admin():
        print("O script precisa ser executado como administrador. Solicitando permissão...")
        run_as_admin()

    pastas_fixas = [
        r"C:\Windows\Temp",
        r"C:\Windows\Prefetch",
        r"C:\Windows\Logs",
        r"C:\Windows\Downloaded Program Files",
    ]

    pastas_limpeza_cache = set()

    for pasta in pastas_fixas:
        limpar_pasta(pasta, pastas_limpeza_cache)

    user_temp = Path(os.getenv('LOCALAPPDATA', '')) / 'Temp'
    if user_temp.exists():
        limpar_pasta(str(user_temp), pastas_limpeza_cache)

    limpar_temporarias_usuarios(pastas_limpeza_cache)

    resposta = input_aguardar("Deseja limpar a lixeira? (s/n) Você tem 10 segundos para responder: ", 10)
    if resposta is not None and resposta.strip().lower() == 's':
        limpar_lixeira()
    else:
        print("Lixeira não será limpa.")

if __name__ == "__main__":
    main()
