#inicio

#defininfo listas
pacientes = []
agenda = []

#definindo as funcoes

#menu
def menu():
    print("=== Clinica Vida+ ===")
    print("1.Cadastrar Paciente")
    print("2.Buscar Paciente")
    print("3.Agendar Consulta")
    print("4.Relatorio")
    print('5.Sair')
    return int(input("Selecione seu servico: "))

#funcao de cadastro
def cadastrar_paciente():
    print("*** Cadastro de Paciente ***")
    nome = input("Nome Completo: ")
    idade = input("Idade: ")
    telefone = input("Telefone: ")
    cpf = input("Cpf (Somente numeros, sem espacos.)")
    endereco = input("Endereco: ")

    paciente = {
        "nome":nome,
        "idade": idade,
        "telefone":telefone,
        "cpf":cpf,
        "endereco":endereco
    }
    pacientes.append(paciente)
    print("Paciente cadastrado com sucesso!")

#funcao de busca
def buscar_paciente():
    print("*** Consulta de Cadastro ***")
    busca = input("Digite o nome ou CPF do paciente: ")
    encontrado = False
    for paciente in pacientes:
        if paciente["nome"] == busca or paciente["cpf"] == busca:
            print(f"Nome: {paciente["nome"]}")
            print(f"Idade: {paciente["idade"]}")
            print(f"Telefone: {paciente["telefone"]}")
            print(f"CPF: {paciente["cpf"]}")
            print(f"Endereco: {paciente["endereco"]}")
        encontrado = True
        break

    if not encontrado:
        print("Paciente nao encontrado!")

#agendamento
#*implementar funcao para buscar agendamentos
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
        print("Paciente nao encontrado, verifique os dados ou cadastre o paciente")
        return
    #coletar dados do agendamento
    hora = input("Informe o horario desejado (HR:MIN): ")
    data = input("Informe a data desejada (DD/MM/AAAA): ")

    agendamento = {
        "hora" : hora,
        "data" : data
    }

    #implementar checagem de horarios e datas disponiveis,
    #verificando se os valores digitados ja existem na lista "agendamento"
    agenda.append(agendamento)
    print("Agendamento concluido com sucesso!")

#funcao para gerar relatorios
def relatorio():
    print("Funcao para gerar relatorios, ainda em implementacao.")

#loop principal
opcao = 0
while opcao != 5:
    try:
        opcao = menu()
        if opcao == 1:
            cadastrar_paciente()
        if opcao == 2:
            buscar_paciente()
        if opcao == 3:
            agendar_consulta()
        if opcao == 4:
            relatorio()
        if opcao == 5:
            print("Saindo...")
            break
    except ValueError:
        print("Opcao invalida, tente novamente.")