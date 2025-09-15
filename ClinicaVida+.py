#início

#defininfd listas
pacientes = []
agenda = []

#definindo as funções

#menu
def menu():
    print("=== Clinica Vida+ ===")
    print("1.Cadastrar Paciente")
    print("2.Buscar Paciente")
    print("3.Agendar Consulta")
    print("4.Relatório Mensal")
    print('5.Sair')
    return int(input("Selecione um serviço: "))

#função de cadastro
def cadastrar_paciente():
    print("*** Cadastro de Paciente ***")
    nome = input("Nome Completo: ")
    idade = int(input("Idade: "))
    telefone = input("Telefone: ")
    cpf = input("Cpf (Somente números, sem espaços.): ")
    endereco = input("Endereço: ")

    paciente = {
        "nome": nome,
        "idade": idade,
        "telefone": telefone,
        "cpf": cpf,
        "endereco": endereco
    }
    pacientes.append(paciente)
    print("Paciente cadastrado com sucesso!")

#função de busca
def buscar_paciente():
    print("*** Consulta de Cadastro ***")
    busca = str(input("Digite o nome ou CPF do paciente: "))
    encontrado = False
    for paciente in pacientes:
        if paciente["nome"] == busca or paciente["cpf"] == busca:
            print(f"Nome: {paciente["nome"]}")
            print(f"Idade: {paciente["idade"]}")
            print(f"Telefone: {paciente["telefone"]}")
            print(f"CPF: {paciente["cpf"]}")
            print(f"Endereço: {paciente["endereco"]}")
        encontrado = True
        break

    if not encontrado:
        print("Paciente não encontrado!")

#agendamento
def agendar_consulta():
    print("*** Agende sua Consulta ***")
    cpf = input("Digite o CPF do paciente:")

    #buscar paciente para agendamento
    paciente_encontrado = None
    for paciente in pacientes:
        if paciente["cpf"] == cpf:
            paciente_encontrado = paciente
            break

    if paciente_encontrado is None:
        print("Paciente não encontrado, verifique os dados ou cadastre o paciente")
        return
        
    #coletar dados do agendamento
    hora = input("Informe o horário desejado (HR:MIN): ")
    data = input("Informe a data desejada (DD/MM/AAAA): ")

    #verifica se horário e data escolhidos já existem na lista
    for agendamento in agenda:
        if agendamento["data"] == data and agendamento["hora"] == hora:
            print("Horário e data já agendados, por favor escolha outro.")
            return
    
    agendamento = {
        "hora" : hora,
        "data" : data
    }
    
    agenda.append(agendamento)
    print("Agendamento concluído com sucesso!")

#função para gerar relatórios
def relatorio():
    print("*** Relatório Mensal ***")
    print(f"Total de pacientes cadastrados: {len(pacientes)}")
    print(f"Total de agendamentos: {len(agenda)}")

#loop principal
opcao = 0
while opcao != 5:
    try:
        opcao = menu()
        if opcao == 1:
            cadastrar_paciente()
        elif opcao == 2:
            buscar_paciente()
        elif opcao == 3:
            agendar_consulta()
        elif opcao == 4:
            relatorio()
        elif opcao == 5:
            print("Saindo...")
            break
            
        else:
            print("Opção inválida, tente novamente.")
        
    except ValueError:

        print("Opção inválida, tente novamente.")
