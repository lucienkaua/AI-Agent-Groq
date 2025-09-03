from groq import Groq
from dotenv import load_dotenv
import base64
import os
load_dotenv()

def main():
    while True:
        opcao = int(input("Escolha uma opção para enviar a imagem:\n1 - URL\n2 - Base64\n0 - Sair\nOpção: "))

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        if opcao == 1:
            url_img = str(input("Digite a URL da imagem: "))
            prompt = str(input("Descreva o que deseja analisar ou obter dessa imagem: "))

            while prompt.strip() == "":
                print("O prompt não pode estar vazio. Tente novamente.")
                prompt = str(input("Descreva o que deseja analisar ou obter dessa imagem: "))

            completion_url = client.chat.completions.create(
            model = "meta-llama/llama-4-scout-17b-16e-instruct",
            messages = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{prompt}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                            "url": f"{url_img}"
                                }
                        }
                    ]
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
            )
            print(completion_url.choices[0].message)
        
        elif opcao == 2:
            nome_img = str(input("Digite o nome da imagem com a extensão (ex: imagem.jpg): "))
            caminho_img = os.path.join(os.getcwd(), nome_img)
            prompt = str(input("Descreva o que deseja analisar ou obter dessa imagem: "))
            while prompt.strip() == "":
                print("O prompt não pode estar vazio. Tente novamente.")
                prompt = str(input("Descreva o que deseja analisar ou obter dessa imagem: "))
            with open(caminho_img, "rb") as imagem:
                completion_b64 = client.chat.completions.create(
                    model = "meta-llama/llama-4-scout-17b-16e-instruct",
                    messages = [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"{prompt}"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64.b64encode(imagem.read()).decode('utf-8')}"
                                    }
                                }
                            ]
                        }
                    ]
                )
                print(completion_b64.choices[0].message)
            
        elif opcao == 0:
            print("Obrigado por testar a versão beta do Optimus Vision. -- Powered by Groq.")
            exit()

        else:
            print("Opção inválida! Escolha 1 ou 2.")

if __name__ == "__main__":
    main()