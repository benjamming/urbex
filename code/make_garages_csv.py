import geopandas
from os import path

raw_data =  (
    'data/raw/Louisville_KY_Downtown_Parking_shapefiles/Louisville_KY_Downtown_Parking.shp')
csv_path = 'data/clean/parking_garages.csv'

# Drop unneeded columns
def drop_columns(df):

    # 
    to_drop = ["CONTACT", "FAC_NUM", "COMPANY", "OPERATOR", "ID", "LDMD", "STR_BLOCK",
            "MEMO", "NOTES", "CITYPARK", "PROPOSED", "PARC","TOTAL_SPCS", "MONTHAVAIL", "PUB_SPC",
            "PHONE_AREA", 'ADDRESS_1', "NAME", "STREETSORT", "PUB_ACCESS",
            "PRIVATE", "CLASS", 
            "TYPE_FAC"] # TYPE_FAC is not necessary because the same information exists under
                        # TYPE column
    
    # easier to add more unused columns this way
    exclude_strings = ['RATE', 'TAX', 'WEB', "PVT", "SHAPE"]
    for string in exclude_strings:
        for col in df.columns:
            if string in col:
                to_drop.append(col)

    # drop the columns
    return df.drop(to_drop, axis=1)

def rename(df):
    # rename all columns to lowercase
    mapping = {column:column.lower() for column in df.columns}
    # make this column name less ambiguous
    mapping['FACILITY'] = 'facility_name'

    return df.rename(mapping, axis=1)

def select_garages(df):
    # select only records for parking garages
    # drop records for (boring) surface lots
    return df[df['type'] == "G"]

def clean(data_path):
    assert path.exists(data_path)
    df = geopandas.read_file(data_path)
    df = drop_columns(df)
    df = rename(df)
    df = select_garages(df)
    df = df.drop('type', axis=1) # This column is no longer needed.
    # All the rows should represent only parking garages

    # rearrange the column order to make it more readable
    return df

def ARC_gis_format(df, file_path):
    formatted = df.rename({'address':'Address'}, axis=1)
    formatted = formatted[['Address', 'facility_name', 'levels', 'objectid', 'geometry']]
    formatted.to_csv(file_path)

def dataframe_store(df, file_path):
    formatted = df[['facility_name', 'address','levels','objectid','geometry']]
    formatted.to_csv(file_path)

if __name__ == "__main__":
    #garages = main(raw_data)
    #garages.to_csv(csv_path)
    #ARC_gis_format(clean(raw_data), 'data/clean/parking_garages_arc.csv')
    dataframe_store(clean(raw_data), csv_path)