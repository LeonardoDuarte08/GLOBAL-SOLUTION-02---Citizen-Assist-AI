from base_conhecimento import BaseConhecimento
from assistente import Assistente
from validador_url import verificar_url


base = BaseConhecimento("data/base_conhecimento.json")
base.carregar()

assistente = Assistente("Citizen Assist AI", base)


while True:
    print("\n================================")
    print("       CITIZEN ASSIST AI")
    print("================================")
    print("1 - Fazer uma pergunta")
    print("2 - Navegar por categorias")
    print("3 - Verificar URL suspeita")
    print("4 - Visualizar indicadores")
    print("5 - Exportar atendimentos")
    print("0 - Sair")
    print("================================")

    opcao = input("Escolha uma opção: ").strip()

    if opcao == "1":
        assistente.perguntar()

    elif opcao == "2":
        assistente.navegar()

    elif opcao == "3":
        url = input("\nDigite a URL que deseja verificar (0 para voltar): ").strip()

        if url == "0":
            continue

        elif not url:
            print("Digite uma URL válida.")

        elif assistente.dados_pessoais(url):
            print("Atenção: não informe URLs com dados pessoais.")
            print("Remova informações pessoais antes de consultar.")

        else:
            verificar_url(url)

    elif opcao == "4":
        assistente.indicadores()

    elif opcao == "5":
        assistente.exportar_csv()

    elif opcao == "0":
        assistente.avaliar_facilidade()
        print("\nObrigado por utilizar o Citizen Assist AI!")
        break

    else:
        print("\nOpção inválida. Tente novamente.")
