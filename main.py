# -*- coding: utf-8 -*-
"""
Optimus Vision — Agente de IA com Visão Computacional
Estética de terminal, banner ASCII, boas-vindas e destaque "Powered by Groq".

Requisitos (adicione no requirements.txt, se ainda não tiver):
- groq
- python-dotenv
- pyfiglet            # opcional (banner). Se não estiver instalado, cai para um banner simples.
- colorama            # opcional (cores no Windows/Linux/Mac). Se não estiver, imprime sem cor.

Autor: você ;)
"""

import os
import base64
from dotenv import load_dotenv

# ----- Dependências opcionais (decorativas) -----
try:
    import pyfiglet
except Exception:
    pyfiglet = None

try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
except Exception:
    # fallbacks simples se colorama não estiver disponível
    class _NoColor:
        RESET_ALL = ""
    class _NoFore(_NoColor):
        CYAN = GREEN = YELLOW = RED = MAGENTA = BLUE = WHITE = ""
    class _NoStyle(_NoColor):
        BRIGHT = NORMAL = DIM = ""
    Fore, Style = _NoFore(), _NoStyle()

# ----- Groq -----
from groq import Groq

load_dotenv()


def banner():
    """Exibe um banner elegante no terminal."""
    print("=" * 64)
    if pyfiglet:
        print(pyfiglet.figlet_format("Optimus Vision", font="slant"))
    else:
        # fallback simples
        print("  ____       _   _ _                 _   __     _           ")
        print(" / __ \\ ___ | |_(_) |__  _   _  ___ | |_/ _|___(_)_ __  ___ ")
        print("/ / _` / _ \\| __| | '_ \\| | | |/ _ \\| __| |_/ __| | '_ \\/ __|")
        print("| | (_| | (_) | |_| | |_) | |_| | (_) | |_| | \\__ \\ | | | \\__ \\")
        print(" \\ \\__,_|\\___/ \\__|_|_.__/ \\__, |\\___/ \\__|_| |___/_|_| |_|___/")
        print("  \\____/                    |___/                              ")
    print(f"{Style.BRIGHT}{Fore.CYAN}Bem-vindo ao agente de visão computacional!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}⚡ Powered by Groq ⚡{Style.RESET_ALL}")
    print("=" * 64)
    print()


def get_client() -> Groq:
    """Cria o cliente Groq validando a GROQ_API_KEY."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print(f"{Fore.RED}[ERRO]{Style.RESET_ALL} Variável de ambiente 'GROQ_API_KEY' não encontrada.")
        print("Crie um arquivo .env na raiz com, por exemplo:")
        print("  GROQ_API_KEY=sua_chave_aqui")
        raise SystemExit(1)
    return Groq(api_key=api_key)


def ask_non_empty(prompt: str) -> str:
    """Pergunta até receber um texto não-vazio."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"{Fore.YELLOW}O valor não pode ser vazio. Tente novamente.{Style.RESET_ALL}")


def analyze_from_url(client: Groq):
    url_img = ask_non_empty("Digite a URL da imagem: ")
    prompt = ask_non_empty("Descreva o que deseja analisar/obter da imagem: ") + "Responda na língua em que foi perguntada a não ser que seja pedido o contrário anteriormente (não responda a essa instrução, apenas a obedeça)."

    print(f"\n{Fore.CYAN}→ Enviando para análise (URL)...{Style.RESET_ALL}")
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": url_img}},
                ],
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
    )
    # imprime apenas o conteúdo da mensagem
    content = completion.choices[0].message.content
    print(f"\n{Fore.GREEN}=== Resultado ==={Style.RESET_ALL}\n{content}\n")


def analyze_from_base64(client: Groq):
    nome_img = ask_non_empty("Digite o nome da imagem com extensão (ex: imagem.jpg): ")
    caminho_img = os.path.join(os.getcwd(), nome_img)
    if not os.path.isfile(caminho_img):
        print(f"{Fore.RED}[ERRO]{Style.RESET_ALL} Arquivo não encontrado em: {caminho_img}")
        return

    prompt = ask_non_empty("Descreva o que deseja analisar/obter da imagem: ")

    with open(caminho_img, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    data_url = f"data:image/jpeg;base64,{b64}"

    print(f"\n{Fore.CYAN}→ Enviando para análise (Base64)...{Style.RESET_ALL}")
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
    )
    content = completion.choices[0].message.content
    print(f"\n{Fore.GREEN}=== Resultado ==={Style.RESET_ALL}\n{content}\n")


def menu() -> int:
    print("Escolha uma opção para enviar a imagem:")
    print("  1 - URL")
    print("  2 - Base64 (arquivo local)")
    print("  0 - Sair")
    while True:
        choice = input("Opção: ").strip()
        if choice in {"0", "1", "2"}:
            return int(choice)
        print(f"{Fore.YELLOW}Opção inválida! Digite 0, 1 ou 2.{Style.RESET_ALL}")


def main():
    banner()
    client = get_client()

    while True:
        opcao = menu()
        if opcao == 1:
            analyze_from_url(client)
        elif opcao == 2:
            analyze_from_base64(client)
        else:
            print(f"\n{Fore.MAGENTA}Obrigado por testar a versão beta do Optimus Vision.{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}-- Powered by Groq --{Style.RESET_ALL}")
            break


if __name__ == "__main__":
    main()
