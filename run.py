from app import criar_app
import os
from dotenv import load_dotenv
load_dotenv()

# Carrega variáveis do .env
load_dotenv()

if __name__ == '__main__': # se este arquivo for o principal que está rodando
    app = criar_app()
    
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    app.run(host=HOST, port=PORT, debug=DEBUG) # inicia o servidor Flask com o modo debug ativado (ajuda a ver erros no terminal)


'''
os.getenv("variavel no .env", "se estiver vazio no .env usa esse")

'''