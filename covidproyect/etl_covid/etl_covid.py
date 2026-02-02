print("hello word")
print("data enginnerig covid")

import pandas as pd
import csv
import os
import numpy as np
import re 


datos = r"C:\Users\zabu\desktop\covidproyect\Monthly_Rates_of_Laboratory-Confirmed_COVID-19_Hospitalizations_from_the_COVID-NET_Surveillance_System.csv"
limpios = r"C:\Users\zabu\desktop\covidproyect\clean_covid.csv"

def transform(datos, limpios):
    try: 
        df = pd.read_csv(datos)
        print(df.head())
        print(df.info())
        print(df['_YearMonth'].dtype)
        print(df['AgeCategory_Legend'].dtype)

        df['MonthlyRate'] = df['MonthlyRate'].replace('*', np.nan)
        media_monthly_rate = df['MonthlyRate'].mean()
        df['MonthlyRate'] = df['MonthlyRate'].fillna(media_monthly_rate)

        df['year'] = df['_YearMonth'].astype(str).str[0:4]

        df['month'] = df['_YearMonth'].astype(str).str[4:6]


        ACLN = df['AgeCategory_Legend'] 

        def extraer_rango_edad(valor):
            if pd.isna(valor): 
                return None
            
            texto = str(valor)

            texto = texto.replace('â‰¥', '≥')
            texto = texto.replace('years', '')
            texto = texto.replace('year', '')
            texto = texto.strip()

            match_rango = re.search(r'(\d+)\s*-\s*(\d+)', texto)
            if match_rango: 
                return f"AGE_{match_rango.group(1)}_{match_rango.group(2)}"
            
            match_menor = re.search(r'(\d+)\s*-\s*<\s*(\d+)', texto)
            if match_menor: 
                return f"AGE_{match_menor.group(1)}_LT_{match_menor.group(2)}"
            
            match_mayor = re.search(r'[≥>]\s*(\d+)', texto)
            if match_mayor: 
                return f"{match_mayor.group(1)}_PLUS"
            
            match_solo_menor = re.search(r'<\s*(\d+)', texto)
            if match_solo_menor: 
                return f"AGE_LT_{match_solo_menor.group(1)}"
            
            return None 
        
        df['range_age'] = ACLN.apply(extraer_rango_edad)

        df['range_age_clean'] = df['range_age'].fillna('All')

        #fase pandemica 

        year = df['year']

        def pandemic_phase(year):
            if year == '2000': return 'early'
            elif year == '2001': return 'Vaccine rollout'
            elif year == '2002': return 'Omicron'
            elif year == '2023': return 'Endemic_early'
            else: 
                return 'Endemic+'
        
        df['pandemic_phase'] = year.apply(pandemic_phase)

        df['month_int'] = pd.to_numeric(df['month'], errors='coerce')

        MI = df['month_int']

        def seasonality(MI):
            if 3 <= MI <= 6: return 'Spring'
            elif 7 <= MI <= 9: return 'Summer'
            else: 
                return 'unknown'
            
        df['seansonality'] = MI.apply(seasonality)



        df.to_csv(limpios, index=False, encoding='utf-8')
        return True
    
    except Exception as e: 
        print(f"hubo un error: {e}")
        return False
    
if __name__ == "__main__":
    transform(datos, limpios)