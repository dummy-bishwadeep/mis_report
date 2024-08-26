from typing import Dict, List, Optional
from pydantic import BaseModel

class Machine(BaseModel):
    meter_position: Optional[str]
    constant: Optional[str]
    running_hrs: Optional[str]
    param1: Optional[str]
    param2: Optional[str]
    param3: Optional[str]

class Chiller(BaseModel):
    Chiller_tag_id: Optional[str]

class Air(BaseModel):
    Air_tag_id: Optional[str]

class Dryer(BaseModel):
    Dryer_tag_id: Optional[str]

class PowerKWLine(BaseModel):
    Machine: Optional[Machine]
    Chiller: Optional[Chiller]
    Air: Optional[Air]
    Dryer: Optional[Dryer]

class DivisionData(BaseModel):
    # This will allow for any keys with dynamic values of PowerKWLine
    __root__: Dict[str, PowerKWLine]

# class DivisionData(BaseModel):
#     Power_KWH_Line_1: PowerKWLine
#     Power_KWH_Line_4A: PowerKWLine

class Formulas(BaseModel):
    Machine: Optional[str]
    Uty_Aux: Optional[str]
    Lighting_Losses: Optional[str]
    TOTAL: Optional[str]

class StaticParams(BaseModel):
    # Using Dict to handle dynamic keys for static parameters
    __root__: Dict[str, str]

# class StaticParams(BaseModel):
#     Total_Plant_Consumption: Optional[str]
#     DNHPDCL_Consumption: Optional[str]
#     Solar_Power: Optional[str]
#     DG_Generation: Optional[str]
#     Total_Consumption: Optional[str]
#     HSD_Consumption: Optional[str]

class MisModel(BaseModel):
    lines: Optional[Dict[str, Dict[str, PowerKWLine]]]
    formulas: Optional[Formulas]
    params: Optional[List[str]]
    static_params: Optional[StaticParams]
    report_type: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    tz: Optional[str]
