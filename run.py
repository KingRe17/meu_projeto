from app import criar_app

app = criar_app()

if __name__ == '__main__': # se este arquivo for o principal que está rodando
    app.run(debug=True) # inicia o servidor Flask com o modo debug ativado (ajuda a ver erros no terminal)
