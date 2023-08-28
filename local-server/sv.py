from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import os
from datetime import datetime

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def dic_getidx(dic, idx):
    key = list(dic.keys())[idx]
    return {key: dic[key]}


def out_format(dic, is_split):
    if is_split:
        return {'labels': list(dic.keys()), 'values': list(dic.values())}
    return {'data': dic}

@app.put('/update_humidity')
def update_humidity(info: float):
    if not os.path.exists('data.json'):
        with open('data.json', 'w+') as f:
            f.write('')
    with open('data.json', 'r+') as f:
        time = datetime.now().strftime("%d %B %Y %H %M %S")
        inf = f.read()
        f.seek(0)
        if inf:
            data = json.loads(inf)
        else:
            data = {}
        data.update({time: info})
        f.write(json.dumps(data))
        f.truncate()

    return Response(status_code=200)

@app.get('/get_humidity')
def get_humidity(is_split: bool = False,
                date: Optional[str] =  None,
                index: Optional[int] = None,
                all: bool = False):
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            inf = f.read()
            if inf:
                data = json.loads(inf)
            else:
                data = {}
    if index is not None:
        return out_format(dic_getidx(data, index), is_split)
    elif date is not None:
        rvalue = data.get(date, None)
        return out_format({date: rvalue}, is_split)
    elif all:
        return out_format(data, is_split)
    else:
        raise HTTPException(status_code=422, detail='Either [index], [date] or [all] should be defined.')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)