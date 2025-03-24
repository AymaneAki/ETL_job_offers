import pandas as pd

data = pd.read_csv("data.csv")

data["Expérience"] = data["Expérience"].str.replace(r"[^0-9\-]", "", regex=True)  
data["Expérience"] = data["Expérience"].apply(lambda x: x + " ans" if x != "-" else x)  

data['Ville'].fillna("Non spécifiée", inplace=True)

def clean_poste(poste):
    if " - " in poste:  
        return poste.rsplit(" - ", 1)[0] 
    return poste  

data["Poste"] = data["Poste"].apply(clean_poste)

data.to_csv("cleaned_data.csv", index=False, encoding="utf-8") 