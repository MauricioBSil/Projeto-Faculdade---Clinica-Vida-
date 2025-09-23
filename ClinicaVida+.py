#início

#importando libs
import sqlite3
from datetime import datetime


#banco de dados
def get_connection():
    con = sqlite3.connect("clinica.db")
    con.execute("PRAGMA foreign_keys = ON")
    return con

def inicializar_db():
    con = get_connection()
    cur = con.cursor()

    #tabela de pacientes
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        nome TEXT NOT NULL,
        idade INTEGER NOT NULL,
        telefone TEXT NOT NULL)
    """)

     #tabela de agendamentos (relacionada a pacientes)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        hora TEXT NOT NULL,
        medico TEXT NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
    )
    """)
    #tabela de médicos
    cur.execute('''
    CREATE TABLE IF NOT EXISTS medicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        especialidade TEXT NOT NULL,
        crm TEXT NOT NULL
    )
    ''')

    con.commit()
    con.close()

#CRUD

#definindo as funções

#função de cadastro
def cadastrar_paciente():
    print("*** Cadastro de Paciente ***")
    nome = input("Nome Completo: ")
    idade = int(input("Idade: "))
    telefone = input("Telefone: ")

    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO pacientes (nome, idade, telefone) VALUES (?, ?, ?)",
        (nome, idade, telefone))
    con.commit()
    con.close()
    print("Paciente cadastrado com sucesso!")

#listar pacientes
def listar_pacientes():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id, nome, idade, telefone FROM pacientes")
    pacientes = cur.fetchall()
    con.close()

    if not pacientes:
        print("Nenhum paciente cadastrado.")
    else:
        print("--- Pacientes Cadastrados ---")
        for p in pacientes:
            print(f"ID: {p[0]} | Nome: {p[1]} | Idade: {p[2]} | Telefone: {p[3]}")
        print("-----------------------------")
    return pacientes


#função de busca
def buscar_paciente():
    print("--- Consulta de Cadastro ---")
    nome = input("Digite o nome do paciente: ")
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT * FROM pacientes WHERE nome LIKE ?", (f"%{nome}%",))
    pacientes = cur.fetchall()
    con.close()

    if pacientes:
        for p in pacientes:
            print(f"ID: {p[0]} | Nome {p[1]} | Idade: {p[2]} | Telefone: {p[3]}")
    else:
        print("Paciente não encontrado.")

#removendo pacientes
def remover_paciente():
    listar_pacientes()
    id_paciente = int(input("Digite o ID do paciente a remover: "))
    con = get_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
    con.commit()
    con.close()
    print("Paciente removido com sucesso!")

#agendamento
def agendar_consulta():
    print("--- Agendamento de Consulta ---")
    pacientes = listar_pacientes()
    if not pacientes:
        print("Nenhum paciente encontrado. Cadastre primeiro.")
        return
    paciente_id = int(input("Informe o ID do paciente: "))

    #validar se paciente existe
    if not any(p[0] == paciente_id for p in pacientes):
        print("Paciente não encontrado.")
        return
    data = input("Informe a Data (DD/MM/AAAA): ")
    hora = input("Informe o horário (HH:MM): ")
    medico = input("Informe o nome do médico responsável: ")

    #validar formato
    try:
        datetime.strptime(data, "%d/%m/%Y")
        datetime.strptime(hora, "%H:%M")
    except ValueError:
        print("Data ou Hora inválida. Use o formato correto.")
        return
    con = get_connection()
    cur = con.cursor()
    #verifica se já existe agendamento correspondente
    cur.execute("SELECT * FROM agendamentos WHERE data=? AND hora=?", (data, hora))
    if cur.fetchone():
        print("Esse horário já está agendado. Escolha outro.")
        con.close()
        return
    cur.execute("INSERT INTO agendamentos (paciente_id, data, hora, medico) VALUES (?, ?, ?, ?)",
                (paciente_id, data, hora, medico))
    con.commit()
    con.close()
    print(f"Consulta marcada com sucesso! Médico responsável: {medico}")

def listar_agendamentos():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
    SELECT a.id, p.nome, a.data, a.hora, a.medico
    FROM agendamentos a
    JOIN pacientes p ON p.id = a.paciente_id
    ORDER BY a.data, a.hora
    """)
    agendamentos = cur.fetchall()
    con.close()

    if not agendamentos:
        print("Nenhum agendamento encontrado.")
        return
    
    print("--- Agenda de Consultas ---")
    for a in agendamentos:
        print(f"ID:{a[0]} | Paciente: {a[1]} | Data: {a[2]} | Hora: {a[3]} | Médico: {a[4]}")
    print("---------------------------------------")

#função para gerar relatórios
def gerar_relatorio():
    print("--- Relatório de Pacientes e Agendamentos ---")
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
    SELECT p.id, p.nome, p.idade, p.telefone, a.data, a.hora, a.medico
    FROM pacientes p
    LEFT JOIN agendamentos a ON p.id = a.paciente_id
    ORDER BY p.nome, a.data, a.hora
    """)
    registros = cur.fetchall()
    con.close()

    if not registros:
        print("Nenhum registro encontrado.")
        return
    
    for r in registros:
        paciente_info = f"ID: {r[0]} | Nome: {r[1]} | Idade: {r[2]} | Telefone: {r[3]}"
        if r[4] and r[5]:
            agendamento_info = f" | Consulta em {r[4]} às {r[5]} com Dr(a). {r[6]}"
        else:
            agendamento_info = " | Sem consultas agendadas"
        print(paciente_info + agendamento_info)
    print("---------------------------------------")

# Função para cadastrar um novo médico
def cadastrar_medico():
    print("--- Cadastro de Médico ---")
    nome = input("Nome do médico: ")
    especialidade = input("Especialidade: ")
    crm = input("CRM: ")
    con = get_connection()
    cur = con.cursor()
    cur.execute("INSERT INTO medicos (nome, especialidade, crm) VALUES (?, ?, ?)", (nome, especialidade, crm))
    con.commit()
    con.close()
    print("Médico cadastrado com sucesso!")

# Função para listar médicos
def listar_medicos():
    con = get_connection()
    cur = con.cursor()
    cur.execute("SELECT id, nome, especialidade, crm FROM medicos")
    medicos = cur.fetchall()
    con.close()
    if not medicos:
        print("Nenhum médico cadastrado.")
    else:
        print("--- Médicos Cadastrados ---")
        for m in medicos:
            print(f"ID: {m[0]} | Nome: {m[1]} | Especialidade: {m[2]} | CRM: {m[3]}")
        print("---------------------------")

#menu
def menu():
    print("\n=== Clinica Vida+ ===")
    print("1. Cadastrar Paciente")
    print("2. Listar Pacientes")
    print("3. Buscar Paciente")
    print("4. Remover Paciente")
    print("5. Gerar Relatório")
    print("6. Agendar Consulta")
    print("7. Listar Agendamentos")
    print("8. Cadastrar Médico")
    print("9. Listar Médicos")
    print("10. Sair")
    return int(input("Selecione uma opção: "))


#loop principal
if __name__ == "__main__":
    inicializar_db()
    while True:
        try:
            opcao = menu()
            if opcao == 1:
                cadastrar_paciente()    
            elif opcao == 2:
                listar_pacientes()
            elif opcao == 3:
                buscar_paciente()
            elif opcao == 4:
                remover_paciente()
            elif opcao == 5:
                gerar_relatorio()
            elif opcao == 6:
                agendar_consulta()
            elif opcao == 7:
                listar_agendamentos()
            elif opcao == 8:
                cadastrar_medico()
            elif opcao == 9:
                listar_medicos()
            elif opcao == 10:
                print("Saindo...")
                break
                

        except ValueError:

            print("Opção inválida, tente novamente.")
