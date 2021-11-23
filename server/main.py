from enum import Enum
from typing import Tuple, List
from psycopg2 import sql
from fastapi import FastAPI, Query, HTTPException, Request
from fastapi.responses import HTMLResponse 
from fastapi.staticfiles import StaticFiles 
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from db_config.config import get_db_conn

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

db_conn = get_db_conn()

CIP_CHECK_QUERY = 'SELECT cip2010code, {}, cip2020code from cip2010_cip2020 where {} = %(cip)s'
CIP_INFO_QUERY = """
            SELECT cip2010code, cip2010title, cip2020code, cip2020title, action, textchange
             from cip2010_cip2020 where cip2010code = %(cip)s or cip2020code = %(cip)s"""
CIP_SOC_DATA_QUERY = """
                SELECT occ_code, occ_title, tot_emp, a_mean from cip2020_soc2018 INNER JOIN bls2020 ON cip2020_soc2018.SOC2018Code=bls2020.occ_code
                where cip2020code LIKE %(cip)s"""
SOC_INFO_QUERY = """SELECT occ_code, occ_title, tot_emp, a_mean from bls2020 where occ_code = %(soc)s"""


class CIPCodeKind(str, Enum):
    twentyTen = "2010"
    twentyTwenty = "2020"

class SOCData(BaseModel):
    soc_code: str
    soc_title: str
    total_employed: int 
    annual_mean: float

class CIPData(BaseModel):
    cip2010code: str
    cip2010title: str
    cip2020code: str
    cip2010title: str
    action: str
    textchange: str


@app.on_event("shutdown")
def shutdown_event():
    db_conn.close()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})

@app.get("/cipsoc", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("cip_soc_crosswalk.html", {'request': request})


@app.get("/api/cip/{cip_code}", response_model=CIPData)
def get_cip_info(cip_code: str = Query(..., regex=r'^\d{2}(\.(\d{2}|\d{4}))?$')):
    check, data = get_cip_code_info(cip_code)
    if not check:
        raise HTTPException(
            status_code=404, detail='cip_code not found')
    keyNames = ['cip2010code', 'cip2010title', 'cip2020code',
                'cip2010title', 'action', 'textchange']
    return convert_db_data_to_body(data[0], keyNames)


@app.get("/api/cip/{cip_code}/soc/", response_model=List[SOCData])
def get_soc_codes(cip_code: str = Query(..., regex=r'^\d{2}(\.(\d{2}|\d{4}))?$'),
                  cip_code_kind: CIPCodeKind = Query(..., title="The type of CIP code")):
    check, data = check_cip_code(cip_code, cip_code_kind)
    if not check:
        raise HTTPException(
            status_code=404, detail=f'cip_code not found for cip_code_kind {cip_code_kind}')

    cip_2020_code = data[0][2]
    keyNames = ['soc_code', 'soc_title', 'total_employed', 'annual_mean']
    return [convert_db_data_to_body(info, keyNames) for info in get_soc_data_for_cip(cip_2020_code)]

@app.get("/api/soc/{soc_code}", response_model=SOCData)
def get_soc_info(soc_code: str = Query(..., regex=r'^\d{2}-\d{4}$')):
    check, data = get_soc_code_info(soc_code)
    if not check:
        raise HTTPException(
            status_code=404, detail='cip_code not found')
    keys = ['soc_code', 'soc_title', 'total_employed', 'annual_mean']
    return convert_db_data_to_body(data[0], keys)


# Helper functions


def check_cip_code(cip_code: str, cip_code_kind: CIPCodeKind):
    cip_title = f'cip{cip_code_kind}title'
    cip_kind = f'cip{cip_code_kind}code'
    cur = db_conn.cursor()
    try:
        cur.execute(sql.SQL(CIP_CHECK_QUERY).format(sql.Identifier(cip_title),
                                                    sql.Identifier(cip_kind)), {'cip': cip_code})
        data = cur.fetchall()
        db_conn.commit()
        cur.close()
    except Exception as err:
        raise(err)
    finally:
        cur.close()
        db_conn.rollback()

    if len(data) == 0:
        return False, None
    else:
        return True, data


def get_soc_data_for_cip(cip_2020_code: str):
    cur = db_conn.cursor()
    try:
        cur.execute(CIP_SOC_DATA_QUERY, {'cip': cip_2020_code + '%%'})
        data = cur.fetchall()
        db_conn.commit()
        cur.close()
    except Exception as err:
        raise(err)
    finally:
        db_conn.rollback()
        cur.close()
    return data


def get_cip_code_info(cip_code: str):
    cur = db_conn.cursor()
    try:
        cur.execute(CIP_INFO_QUERY, {'cip': cip_code})
        data = cur.fetchall()
        db_conn.commit()
        cur.close()
    except Exception as err:
        raise(err)
    finally:
        cur.close()
        db_conn.rollback()

    if len(data) == 0:
        return False, None
    else:
        return True, data

def get_soc_code_info(soc_code: str):
    cur = db_conn.cursor()
    try:
        cur.execute(SOC_INFO_QUERY, {'soc': soc_code})
        data = cur.fetchall()
        db_conn.commit()
        cur.close()
    except Exception as err:
        raise(err)
    finally:
        cur.close()
        db_conn.rollback()

    if len(data) == 0:
        return False, None
    else:
        return True, data

def convert_db_data_to_body(data: Tuple, keys: List[str]):
    return {value: data[i] for i, value in enumerate(keys)}
