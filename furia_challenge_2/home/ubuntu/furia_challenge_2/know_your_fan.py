
import json
import os
from datetime import datetime

DATA_FILE = os.path.join("/home/ubuntu/furia_challenge_2", "fan_profile.json")

def get_input(prompt, validation_func=None, error_message="Entrada inválida."):
   
    while True:
        try:
            value = input(prompt).strip()
            if validation_func:
                if validation_func(value):
                    return value
                else:
                    print(error_message)
            elif value: 
                return value
            else:
                 print("Entrada não pode ser vazia.")
        except EOFError:
            print("\nEntrada encerrada inesperadamente. Saindo.")
            exit()
        except Exception as e:
            print(f"Ocorreu um erro: {e}")

def validate_year(year_str):
    """Valida se a string é um ano válido (4 dígitos)."""
    return year_str.isdigit() and len(year_str) == 4 and 1900 <= int(year_str) <= datetime.now().year

def validate_yes_no(answer):
    """Valida se a resposta é 's' ou 'n'."""
    return answer.lower() in ["s", "n"]

def validate_number_range(min_val, max_val):
    """Retorna uma função que valida se a entrada é um número dentro de um intervalo."""
    def validator(value_str):
        return value_str.isdigit() and min_val <= int(value_str) <= max_val
    return validator

def collect_fan_data():
    """Coleta dados do fã através de perguntas no console."""
    fan_data = {}
    print("\n--- Coleta de Dados - Know Your Fan (FURIA Tech) ---")
    print("Por favor, responda às perguntas abaixo para conhecermos melhor você como fã.")

    # 1. Dados Básicos
    print("\n--- Seção 1: Informações Básicas ---")
    fan_data["nickname"] = get_input("Qual seu nickname ou nome preferido? ")
    fan_data["birth_year"] = get_input("Em que ano você nasceu (AAAA)? ", validation_func=validate_year, error_message="Ano inválido. Digite um ano entre 1900 e o ano atual.")
    fan_data["location"] = get_input("Onde você mora? ")

    # 2. Preferências de E-sports
    print("\n--- Seção 2: Preferências de E-sports ---")
    fan_data["favorite_team"] = get_input("Qual seu time de e-sport favorito (além da FURIA, claro!)? ")
    fan_data["favorite_player"] = get_input("Você tem um jogador profissional favorito? Quem? ")
    fan_data["other_games"] = get_input("Quais outros jogos de e-sport você acompanha? (separados por vírgula, se houver) ")

    # 3. Hábitos de Visualização
    print("\n--- Seção 3: Hábitos de Visualização ---")
    fan_data["watch_frequency_hours"] = get_input("Quantas horas por semana, em média, você dedica a assistir e-sports? ", validation_func=lambda x: x.isdigit(), error_message="Por favor, digite um número.")
    fan_data["preferred_platform"] = get_input("Qual plataforma você mais usa para assistir e-sports (Twitch, YouTube, etc.)? ")
    fan_data["attended_live_event"] = get_input("Você já foi a algum evento presencial de e-sports? (s/n) ", validation_func=validate_yes_no)

    # 4. Engajamento com a Comunidade
    print("\n--- Seção 4: Engajamento ---")
    fan_data["follows_furia_social"] = get_input("Você segue a FURIA nas redes sociais? (s/n) ", validation_func=validate_yes_no)
    fan_data["interacts_social_media"] = get_input("Você costuma comentar ou interagir em posts sobre e-sports? (s/n) ", validation_func=validate_yes_no)
    fan_data["member_community"] = get_input("Você participa de alguma comunidade online de e-sports (Discord, fórum, etc.)? (s/n) ", validation_func=validate_yes_no)
    fan_data["purchased_merch"] = get_input("Você já comprou algum produto oficial de time de e-sports (camisa, etc.)? (s/n) ", validation_func=validate_yes_no)

    # 5. Hábitos de Jogo
    print("\n--- Seção 5: Seus Hábitos de Jogo ---")
    fan_data["plays_esports_games"] = get_input("Você joga algum dos jogos de e-sport que acompanha? (s/n) ", validation_func=validate_yes_no)
    if fan_data["plays_esports_games"].lower() == 's':
        fan_data["play_frequency_hours"] = get_input("Quantas horas por semana, em média, você joga? ", validation_func=lambda x: x.isdigit(), error_message="Por favor, digite um número.")
        fan_data["main_game_played"] = get_input("Qual jogo você mais joga? ")
        fan_data["competitive_rank"] = get_input("Qual seu nível/rank nesse jogo (se aplicável)? ")


    print("\n--- Coleta Concluída! Obrigado pelas suas respostas. ---")
    return fan_data

def save_data(data):
    
    try:
        all_data = []
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                try:
                    all_data = json.load(f)
                    if not isinstance(all_data, list):
                        print(f"Aviso: O arquivo {DATA_FILE} não contém uma lista JSON válida. Iniciando com uma lista vazia.")
                        all_data = []
                except json.JSONDecodeError:
                    print(f"Aviso: O arquivo {DATA_FILE} está corrompido ou não é um JSON válido. Iniciando com uma lista vazia.")
                    all_data = []
        
       
        data["timestamp"] = datetime.now().isoformat()
        all_data.append(data)

       
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)
        print(f"\nDados salvos com sucesso em {DATA_FILE}")
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

def view_profiles():
    
    print("\n--- Visualização de Perfis de Fãs ---")
    try:
        if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
            print("Nenhum perfil encontrado.")
            return

        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
            if not isinstance(all_data, list) or not all_data:
                 print("Nenhum perfil encontrado.")
                 return

        print(f"Total de perfis encontrados: {len(all_data)}\n")
        for i, profile in enumerate(all_data):
            print(f"--- Perfil {i+1} ---")
            for key, value in profile.items():
                print(f"  {key.replace('_', ' ').capitalize()}: {value}")
            print("--------------------\n")
            
            if (i + 1) % 3 == 0 and len(all_data) > i + 1:
                input("Pressione Enter para ver os próximos perfis...")

    except json.JSONDecodeError:
        print(f"Erro: O arquivo {DATA_FILE} está corrompido.")
    except Exception as e:
        print(f"Erro ao carregar os perfis: {e}")

def main_menu():
    
    while True:
        print("\n--- Menu Principal - Know Your Fan ---")
        print("1. Coletar Novo Perfil de Fã")
        print("2. Visualizar Perfis Salvos")
        print("3. Sair")
        
        choice = input("Escolha uma opção (1-3): ")

        if choice == '1':
            collected_data = collect_fan_data()
            save_data(collected_data)
        elif choice == '2':
            view_profiles()
        elif choice == '3':
            print("Saindo do programa.!")
            break
        else:
            print("Opção inválida. Por favor, escolha 1, 2 ou 3.")

if __name__ == "__main__":
    main_menu()

