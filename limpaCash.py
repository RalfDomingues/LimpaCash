import os
import shutil
import threading
import ctypes
import sys
from pathlib import Path

def is_admin():
    """
    Verifica se o script está sendo executado com privilégios de administrador.
    
    Returns:
        bool: True se for admin, False caso contrário.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """
    Reexecuta o script atual pedindo privilégios de administrador (UAC).
    Isso é necessário para conseguir apagar arquivos protegidos do Windows.
    """
    # Passa os parâmetros originais do script
    params = " ".join(f'"{arg}"' for arg in sys.argv[1:])
    # Executa novamente o Python com "runas" (modo administrador)
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{sys.argv[0]}" {params}', None, 1
    )
    sys.exit()  # encerra a execução atual, aguardando a nova com admin


def limpar_pasta(caminho, pastas_limpeza_cache):
    """
    Remove arquivos e subpastas de uma pasta específica.
    Usa cache para evitar limpar a mesma pasta mais de uma vez.

    Args:
        caminho (str): Caminho da pasta a ser limpa.
        pastas_limpeza_cache (set): Conjunto de pastas já limpas (evita repetição).
    """
    caminho = str(Path(caminho).resolve())
    if caminho in pastas_limpeza_cache:
        return  # já foi limpa
    pastas_limpeza_cache.add(caminho)

    print(f"Iniciando limpeza da pasta: {caminho}")
    pasta = Path(caminho)
    if not pasta.exists():
        print(f"Pasta não existe: {caminho}")
        return

    # Itera sobre os itens da pasta
    for item in pasta.iterdir():
        try:
            if item.is_file() or item.is_symlink():
                item.unlink()  # remove arquivos e atalhos
            elif item.is_dir() and not item.is_symlink():
                shutil.rmtree(item)  # remove pastas inteiras
        except Exception as e:
            msg = str(e).lower()
            if "being used by another process" in msg or "acesso negado" in msg:
                print(f"Aviso: Não foi possível excluir {item}: {e}")
            else:
                print(f"Erro: {item}: {e}")
    print(f"Limpeza concluída: {caminho}")


def limpar_lixeira():
    """
    Esvazia a lixeira do Windows usando a API nativa.
    """
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
    """
    Pergunta algo ao usuário com tempo limite de resposta.

    Args:
        mensagem (str): Mensagem exibida ao usuário.
        timeout (int): Tempo limite em segundos.

    Returns:
        str|None: Resposta do usuário, ou None se o tempo esgotar.
    """
    resposta = [None]

    def ask():
        resposta[0] = input(mensagem)

    # Cria thread para não travar a execução
    thread = threading.Thread(target=ask)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        return None  # tempo esgotado
    return resposta[0]


def limpar_temporarias_usuarios(pastas_limpeza_cache):
    """
    Limpa pastas temporárias em cada perfil de usuário do Windows.

    Args:
        pastas_limpeza_cache (set): Cache para evitar limpar a mesma pasta várias vezes.
    """
    users_dir = Path("C:/Users")
    if not users_dir.exists():
        print("Pasta C:/Users não encontrada.")
        return

    # Pastas alvo dentro de cada usuário
    pastas_para_limpar_por_usuario = [
        "AppData\\Local\\Temp",
        "AppData\\Roaming\\Microsoft\\Windows\\Recent",
        "AppData\\Local\\Microsoft\\Windows\\INetCache",
        "AppData\\Local\\Microsoft\\Windows\\WebCache",
    ]

    for user_folder in users_dir.iterdir():
        if user_folder.is_dir():
            nome = user_folder.name.lower()
            # Ignora perfis especiais do Windows
            if nome in ["default", "defaultuser0", "public", "all users"]:
                continue

            # Limpa cada subpasta alvo
            for subpasta in pastas_para_limpar_por_usuario:
                caminho = user_folder / subpasta
                if caminho.exists():
                    limpar_pasta(str(caminho), pastas_limpeza_cache)


def main():
    """Função principal: organiza a execução do script de limpeza."""

    # Verifica privilégios de administrador
    if not is_admin():
        print("O script precisa ser executado como administrador. Solicitando permissão...")
        run_as_admin()

    # Pastas fixas do Windows a serem limpas
    pastas_fixas = [
        r"C:\Windows\Temp",
        r"C:\Windows\Prefetch",
        r"C:\Windows\Logs",
        r"C:\Windows\Downloaded Program Files",
    ]

    pastas_limpeza_cache = set()  # evita duplicação de limpeza

    # Limpa as pastas fixas
    for pasta in pastas_fixas:
        limpar_pasta(pasta, pastas_limpeza_cache)

    # Limpa a pasta temporária do usuário atual
    user_temp = Path(os.getenv('LOCALAPPDATA', '')) / 'Temp'
    if user_temp.exists():
        limpar_pasta(str(user_temp), pastas_limpeza_cache)

    # Limpa pastas temporárias de todos os usuários do Windows
    limpar_temporarias_usuarios(pastas_limpeza_cache)

    # Pergunta ao usuário se deseja limpar a lixeira
    resposta = input_aguardar("Deseja limpar a lixeira? (s/n) Você tem 10 segundos para responder: ", 10)
    if resposta is not None and resposta.strip().lower() == 's':
        limpar_lixeira()
    else:
        print("Lixeira não será limpa.")


if __name__ == "__main__":
    main()
