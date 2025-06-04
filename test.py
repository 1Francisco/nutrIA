import pandas as pd



# URLs de archivos NHANES 2021-2022
urls = {
    "Demographics": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.xpt",
    "BodyMeasures": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BMX_L.xpt",
    "Diabetes": "https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/AUQ_L.xpt"
}

# Descargar y cargar cada archivo en un DataFrame
dataframes = {}
for key, url in urls.items():
    print(f"Descargando {key}...")
    df = pd.read_sas(url, format='xport')
    dataframes[key] = df
    print(f"{key} cargado con {df.shape[0]} filas y {df.shape[1]} columnas.")

# Combinar DataFrames usando la columna SEQN como clave
df_merged = pd.merge(dataframes["Demographics"], dataframes["BodyMeasures"], on="SEQN")
df_merged = pd.merge(df_merged, dataframes["Diabetes"], on="SEQN", how="left")


# Diccionario para renombrar columnas por nombres comprensibles
columnas_renombradas = {
    "SEQN": "ID",
    "RIAGENDR": "Sexo",
    "RIDAGEYR": "Edad",
    "RIDRETH3": "Raza_Etnia",
    "DMDEDUC2": "Nivel_Educativo",
    "BMXWT": "Peso_kg",
    "BMXHT": "Estatura_cm",
    "BMXBMI": "IMC",
    "AUQ100": "Tiene_diabetes",
    "AUQ110": "Edad_diagnostico_diabetes",
    "AUQ120": "Uso_insulina"
}

# Renombrar las columnas existentes
columnas_existentes = {col: nombre for col, nombre in columnas_renombradas.items() if col in df_merged.columns}
df_merged.rename(columns=columnas_existentes, inplace=True)
df_merged.to_csv("datos_nhanes.csv", index=False)

# Mostrar las primeras filas con columnas renombradas
print(df_merged[list(columnas_existentes.values())].head())
