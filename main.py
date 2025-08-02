from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import pandas as pd
import io
import time
from asterisk.ami import AMIClient, Action
import uuid
from app.event_handler import event_listener


app = FastAPI()

@app.post("/ligar/")
async def ligar(
    file: UploadFile = File(...),
    ramal: str = Form(...)
):
    contents = await file.read()
    s = contents.decode('utf-8')
    df = pd.read_csv(io.StringIO(s), sep=';')

    client = AMIClient(address='172.29.64.17', port=5038)
    response = client.login(username='pythonuser', secret='sua_senha_ami')
    print(response.response)

    client.add_event_listener(event_listener)

    for index, row in df.iterrows():
        telefone = row['telefone']  

        action = Action('Originate', {
            'Channel': f'PJSIP/{telefone}',
            'Exten': ramal,
            'Context': 'interno',
            'Priority': '1',
            'CallerID':'RAMAL <9999>',
            'Async': 'true',
            'ActionID': str(uuid.uuid4())
        })
        client.send_action(action)
        time.sleep(5)

    time.sleep(5)
    client.logoff()

    return JSONResponse(content={"message": "Chamadas disparadas com sucesso"})
