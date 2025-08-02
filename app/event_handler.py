import uuid
from datetime import datetime
from app.database import SessionLocal
from app.models import Log

# Variáveis globais para guardar o estado atual (ideal: usar dict por Uniqueid)
caller_number = None
receiver_number = None
call_answered = False
call_rejected = False
call_started_at = None
call_ended_at = None

def saveLog(caller, receiver, started, answered, rejected, ended, duration):
    session = SessionLocal()
    unique_id = str(uuid.uuid4())
    print(f"Gerando unique_id: {unique_id}")  # Debug print
    
    log = Log(
        unique_id=unique_id,
        caller_number=caller,
        receiver_number=receiver,
        call_started_at=started,
        call_answered=answered,
        call_rejected=rejected,
        call_ended_at=ended,
        call_duration_seconds=duration
    )
    session.add(log)
    session.commit()
    session.close()


def event_listener(event, **kwargs):
    print(event, "INCIAAAAANDO")
    global caller_number, receiver_number, call_answered, call_rejected, call_started_at, call_ended_at
    if event.name == 'DialEnd':
        print(event.keys.get('DialStatus'), 'finalizou')
    if event.name == 'Newstate':
        caller_number = event.keys.get('CallerIDNum')
        if event.keys.get('ChannelStateDesc') == 'Up':
            call_started_at = datetime.utcnow()
            call_answered = True

    elif event.name == 'OriginateResponse':
        receiver_number = event.keys.get('Channel')

    elif event.name == 'Hangup':
        call_rejected = (event.keys.get('Cause-txt') == 'Call Rejected')
        call_ended_at = datetime.utcnow()

        # Calcular duração (se tiver data de início)
        if call_started_at and call_ended_at:
            duration = int((call_ended_at - call_started_at).total_seconds())
        else:
            duration = 0

        # Chamar saveLog só quando chamada termina
        saveLog(
            caller=caller_number or "Unknown",
            receiver=receiver_number or "Unknown",
            started=call_started_at or datetime.utcnow(),
            answered=call_answered,
            rejected=call_rejected,
            ended=call_ended_at,
            duration=duration
        )

        # Resetar variáveis para próxima chamada (opcional)
        caller_number = None
        receiver_number = None
        call_answered = False
        call_rejected = False
        call_started_at = None
        call_ended_at = None
