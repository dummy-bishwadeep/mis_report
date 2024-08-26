from typing import Dict, Optional, List, Any

from pydantic import BaseModel


class DefaultRequest(BaseModel):
    tz: str
    project_id: str
    language: Optional[str] = "en"


class Machine(BaseModel):
    meter_position: str
    constant: str
    running_hrs: str
    param1: str
    param2: str
    param3: str

class Chiller(BaseModel):
    Chiller_tag_id: str

class Air(BaseModel):
    Air_tag_id: str

class Dryer(BaseModel):
    Dryer_tag_id: str

class PowerKWLine(BaseModel):
    Machine: Machine
    Chiller: Chiller
    Air: Air
    Dryer: Dryer

class DivisionData(BaseModel):
    Power_KWH_Line_1: PowerKWLine
    Power_KWH_Line_4A: PowerKWLine

class Formulas(BaseModel):
    Machine: str
    Uty_Aux: str
    Lighting_Losses: str
    TOTAL: str

class StaticParams(BaseModel):
    Total_Plant_Consumption: str
    DNHPDCL_Consumption: str
    Solar_Power: str
    DG_Generation: str
    Total_Consumption: str
    HSD_Consumption: str

class MisModel(BaseModel):
    lines: Dict[str, DivisionData]
    formulas: Formulas
    params: List[str]
    static_params: StaticParams
    report_type: str
    start_date: str
    end_date: str
    tz: str
