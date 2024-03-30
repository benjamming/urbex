import geopandas
from os import path

raw_data =  (
    'data/raw/Louisville_KY_Downtown_Parking_shapefiles/Louisville_KY_Downtown_Parking.shp')
csv_path = 'data/clean/parking_garages.csv'

# Drop unneeded columns
def drop_columns(df):
    to_drop = ["CONTACT", "FAC_NUM", "COMPANY", "OPERATOR", "ID", "LDMD", "STR_BLOCK",
            "MEMO", "NOTES", "CITYPARK", "PROPOSED", "PARC","TOTAL_SPCS", "MONTHAVAIL", "PUB_SPC",
            "PHONE_AREA", 'ADDRESS_1', "NAME", "STREETSORT", "PUB_ACCESS",
            "PRIVATE", "CLASS", "TYPE_FAC"]
    
    exclude_strings = ['RATE', 'TAX', 'WEB', "PVT", "SHAPE"]
    for string in exclude_strings:
        for col in df.columns:
            if string in col:
                to_drop.append(col)

    return df.drop(to_drop, axis=1)

def rename(df):
    mapping = {column:column.lower() for column in df.columns}
    mapping['FACILITY'] = 'facility_name'
    return df.rename(mapping, axis=1)

def select_garages(df):
    return df[df['type'] == "G"]

def main(data_path):
    assert path.exists(data_path)
    df = geopandas.read_file(data_path)
    df = drop_columns(df)
    df = rename(df)
    df = select_garages(df)
    df = df.drop('type', axis=1)
    return df[['facility_name', 'address', 'levels', 'geometry', 'objectid']]

if __name__ == "__main__":
    garages = main(raw_data)
    garages.to_csv(csv_path)