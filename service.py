import json
import requests
import time
import os
import sys
import pandas as pd

import dados_cliente

# Fazer a leitura de arquivos
file_service = 'data/sheets-service.xlsx'
file_log = 'data/file_log.txt'
file_log_error = 'data/file_log_error.txt'


# def resource_path(relative_path): # Fazer a leitura de arquivos após criar executável
#     try:
#         # 1. Tenta acessar o caminho temporário do PyInstaller
#         base_path = sys._MEIPASS
#     except Exception:
#         # 2. Se não estiver no executável, usa o diretório do projeto
#         base_path = os.path.abspath(".")
#
#     # 3. Retorna o caminho completo (base_path + 'data' + nome_do_arquivo)
#     # Note que 'data' é o nome da pasta que definimos no --add-data acima
#     return os.path.join(base_path, 'data', relative_path)


# file_service = resource_path("sheets-service.xlsx")
# file_log = resource_path("file_log.txt")
# file_log_error = resource_path("file_log_error.txt")


def write_record(file_path_log, record):  #Função de log
    file = open(file_path_log, 'a', encoding="utf-8")
    file.write(f'{record}\n')
    file.close()


def post_service_movidesk(data: dict): #Post API Movidesk
    # url_full = f'https://api.movidesk.com/public/v1/services?token=ab17d7fd-cb24-4943-b446-3de25465a338'
    token = dados_cliente.token_movidesk
    url = f'https://api.movidesk.com/public/v1/services?token={token}'
    headers = {'Content-Type': 'application/json'}
    body_json = json.dumps(data)
    response = requests.post(url=url, data=body_json, headers=headers, verify=False)
    # return [response.json(), response, response.status_code, url]
    return response


def processar_e_enviar_dados(): # Processar a planilha
    post_count = 0
    """
    Lê a planilha XLSX, itera sobre as linhas e envia cada uma como
    payload JSON para a URL da API especificada, utilizando a estrutura
    JSON fornecida pelo usuário.
    """
    print(f"Iniciando a leitura do arquivo: {file_service}")

    if not os.path.exists(file_service):
        print(f"ERRO: Arquivo '{file_service}' não encontrado.")
        print("Certifique-se de que o arquivo existe no mesmo diretório do script.")
        return

    try:
        # Carrega o arquivo XLSX para um DataFrame do pandas
        df = pd.read_excel(file_service)
        print(f"Planilha carregada com sucesso. Total de {len(df)} linhas para processar.")

        # Converte os nomes das colunas para minúsculas e remove espaços para facilitar o acesso
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

    except Exception as e:
        print(f"ERRO ao ler o arquivo XLSX: {e}")
        return

    # Loop principal para processar cada linha
    for index, row in df.iterrows():
        # index + 2 pois pandas é 0-based e a linha 1 é o cabeçalho
        num_linha = index + 2

        name_service = row.get('name', 'Serviço sem nome')
        description_service = row.get('description', None)
        parent_service_id = row.get('parent_service_id', None)
        parent_service_id = int(parent_service_id) if pd.notna(parent_service_id) else None
        service_for_ticket_type = row.get('service_for_ticket_type', 2)
        service_for_ticket_type = int(service_for_ticket_type) if pd.notna(service_for_ticket_type) else 2
        is_visible = row.get('is_visible', 3)
        is_visible = int(is_visible) if pd.notna(is_visible) else 3
        allow_selection = row.get('allow_selection', 3)
        allow_selection = int(allow_selection) if pd.notna(allow_selection) else 3
        allow_finish_ticket = row.get('allow_finish_ticket', True)
        allow_finish_ticket = bool(allow_finish_ticket) if pd.notna(allow_finish_ticket) else True
        is_active = row.get('is_active', True)
        is_active = bool(is_active) if pd.notna(is_active) else True
        allow_all_categories = row.get('allow_all_categories', True)
        allow_all_categories = bool(allow_all_categories) if pd.notna(allow_all_categories) else True

        # Cria o payload JSON com os dados da linha, usando a estrutura que você forneceu.
        payload = {
            "name": name_service,
            "description": description_service,
            "parentServiceId": parent_service_id,
            "serviceForTicketType": service_for_ticket_type,
            "isVisible": is_visible,
            "allowSelection": allow_selection,
            "allowFinishTicket": allow_finish_ticket,
            "isActive": is_active,
            "automationMacro": row.get('automation_macro', ""),
            "defaultCategory": row.get('default_category', ""),
            "defaultUrgency": row.get('default_urgency', ""),
            "allowAllCategories": allow_all_categories,
            "categories": row.get('categories', [])
        }

        # Remove chaves com valores None ou NaN (Opcional, mas útil se a API for rigorosa)
        payload = {k: v for k, v in payload.items() if pd.notna(v)}

        print(f"\n--- Processando Linha {num_linha} ---")
        print(f"Payload: {payload}")

        try:
            # Envia a requisição POST para a API
            # response = requests.post(URL_API, json=payload, headers=HEADERS)
            response = post_service_movidesk(payload)

            # Verifica o status da resposta
            if response.status_code in [200]:
                print(f"SUCESSO: Linha {num_linha} enviada. Status: {response}")
                post_count += 1
                record = f'{post_count} - Serviço inserido: {name_service}'
                file = open(file_log, 'a', encoding="utf-8")
                file.write(f'{record}\n')
                file.close()
                print('------------------------------------------\n')
                # response.write_record(file_path_log=file_log, record=record)
                # print(f"Resposta da API: {response.json()}") # Descomente para ver o retorno da API
            else:
                print(f"FALHA: Linha {num_linha}. Status: {response}")
                record = f'{post_count} - Serviço NÃO inserido: {payload}'
                file = open(file_log, 'a', encoding="utf-8")
                file.write(f'{record}\n')
                file.close()
                print('------------------------------------------\n')

        except requests.exceptions.RequestException as req_err:
            print(f"ERRO DE CONEXÃO ao enviar a Linha {num_linha}: {req_err}")

        # Pequena pausa para evitar sobrecarregar a API (opcional, mas recomendado)
        time.sleep(0.1)

    print("\nProcessamento da planilha concluído.")


# --- Execução Principal ---
if __name__ == "__main__":
    # Verifique se as bibliotecas estão instaladas:
    # pip install pandas openpyxl requests
    processar_e_enviar_dados()


