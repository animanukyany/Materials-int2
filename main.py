import json
import material
import pyodbc
import uuid
from sqlalchemy import create_engine, text


with open("config.json", "r", encoding="utf-8") as file:
    conf = json.load(file)

with open(conf["mat_file_path"], "r", encoding="utf-8") as file:
    data = json.load(file)

def insert(data):
    engine = create_engine(conf["connection"])

    query = text("""
        EXEC dbo.asp_addMT 
            :MTCode, :Caption, :FullCaption, :Type, :Group, :SubstituteItemsGroup,
            :CPACode, :Unit, :AltUnit, :ExpMethod, :Show, :Descr, :Country, :Producer, 
            :Property1, :Property2, :Bonus, :Point, :Extra, :Vat, :EcoFeeRate, :IsWeight, 
            :Coeff, :Discount, :PLUCode, :B2BExported, :ExternalCode, :ISN, :TS, :Status, :MTID, :BODY, 
            :CaptionEN, :CaptionRU, :AdditionalDescr1, :AdditionalDescr2, :MainSupplier
    """)

    with engine.begin() as connection:
        for material in data:


            params = {
                "MTCode": material.get("code", ""),
                "Caption": material.get("name", ""),
                "FullCaption": material.get("name", ""),
                "Type": material.get("type", ""),
                "Group": material["group"]["code"],
                "SubstituteItemsGroup": "",
                "CPACode": "",
                "Unit": material["unit"]["code"],
                "AltUnit": material["unit"]["code"],
                "ExpMethod": 1,
                "Show": 1,
                "Descr": "",
                "Country": "",
                "Producer": "",
                "Property1": "",
                "Property2": "",
                "Bonus": 0,
                "Point": 0,
                "Extra": 0,
                "Vat": True,
                "EcoFeeRate": 0,
                "IsWeight": 0,
                "Coeff": 1,
                "Discount": "",
                "PLUCode": None,
                "B2BExported": 0,
                "ExternalCode": "",
                "ISN": uuid.uuid4(),
                "TS": 1,
                "Status": "",
                "MTID": "",
                "BODY": None,
                "CaptionEN": "",
                "CaptionRU": "",
                "AdditionalDescr1": "",
                "AdditionalDescr2": "",
                "MainSupplier": 0,
            }

            try:
                connection.execute(query, params)

                ###
                mt_id = connection.execute(text("SELECT @@IDENTITY")).fetchone()[0]
                unit_params = {'MTID': mt_id, 'QntUnit': material["unit"]["code"], 'Coef': 1, 'Status': ''}
                connection.execute(text(f"""EXEC dbo.asp_addMTQntUnits :MTID, :QntUnit, :Coef, :Status"""),
                                   unit_params)
            except Exception as e:
                   print(f" Error inserting material {material}: {e}")

    return "ok"

allowed_groups = {
    "1": "Տեխնիկա",
    "11": "հեռւստացույց",
    "12": "տեսամագնիտաֆոն"
}
group_input = {"code": "001", "name": "Տեխնիկա"}
code = group_input.get("code")
if code in allowed_groups:
    print(f"Valid group: {code} - {allowed_groups[code]}")
else:
    raise ValueError(f"Invalid group code: {code}")

if __name__ == "__main__":
    insert(data)
    print(" Materials inserted successfully!")