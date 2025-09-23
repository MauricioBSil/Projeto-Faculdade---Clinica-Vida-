#início

#importando libs
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog



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

     # Tabela de agendamentos (relacionada a pacientes)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        hora TEXT NOT NULL,
        FOREIGN KEY (paciente_id) REFERENCES pacientes (id)
    )
    """)

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
    cur.execute("INSERT INTO agendamentos (paciente_id, data, hora) VALUES (?, ?, ?)",
                (paciente_id, data, hora))
    con.commit()
    con.close()
    print("Consulta marcada com sucesso!")

def listar_agendamentos():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
    SELECT a.id, p.nome, a.data, a.hora
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
        print(f"ID:{a[0]} | Paciente: {a[1]} | Data: {a[2]} | Hora: {a[3]}")
    print("---------------------------------------")

#função para gerar relatórios

#cadastro de medicos

#menu
def menu():
    print("\n=== Clinica Vida+ ===")
    print("1. Cadastrar Paciente")
    print("2. Listar Pacientes")
    print("3. Buscar Paciente")
    print("4. Remover Paciente")
    print("5. Sair")
    print("6. Agendar Consulta")
    print("7. Listar Agendamentos")
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
                print("Saindo...")
                break
            elif opcao == 6:
                agendar_consulta()
            elif opcao == 7:
                listar_agendamentos()

        except ValueError:

            print("Opção inválida, tente novamente.")
