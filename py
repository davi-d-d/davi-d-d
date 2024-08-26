from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# Carregue suas credenciais do Google Calendar
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

try:
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
except Exception as e:
    print(f"Erro ao carregar as credenciais: {e}")
    exit()

# Crie o serviço do Google Calendar
try:
    service = build('calendar', 'v3', credentials=credentials)
except Exception as e:
    print(f"Erro ao criar o serviço do Google Calendar: {e}")
    exit()

# Defina o ID do seu calendário. Use "primary" para o calendário principal.
calendar_id = 'primary'

# Função para criar um evento
def create_event(summary, description, start_time, recurrence_rule):
    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': (start_time + timedelta(hours=1)).isoformat(),
            'timeZone': 'America/Sao_Paulo',
        },
        'recurrence': [
            recurrence_rule,
        ],
    }

    try:
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except Exception as e:
        print(f"Erro ao criar o evento: {e}")

# Função para converter uma data em texto para o formato datetime
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError as e:
        print(f"Erro ao converter a data: {e}")
        exit()

# Datas de início dos eventos (substitua '2024-09-01' pela data desejada)
start_date_str = input("Digite a data inicial no formato AAAA-MM-DD: ")
start_date = parse_date(start_date_str)

# Eventos a serem criados
materias = {
    'EN': 'EN review',
    'S1': 'S1 review',
    'Redes': 'Redes review'
}

# Intervalos de recorrência
recurrences = {
    'EN': 'RRULE:FREQ=DAILY;INTERVAL=7',  # A cada 7 dias
    'S1': 'RRULE:FREQ=DAILY;INTERVAL=1',  # Diariamente
    'Redes': 'RRULE:FREQ=DAILY;INTERVAL=30'  # A cada 30 dias
}

# Criação dos eventos
for materia, summary in materias.items():
    create_event(summary, f'Revisão da matéria de {materia}', start_date, recurrences[materia])
