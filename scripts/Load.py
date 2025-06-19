import pandas as pd
import mysql.connector

csv_file = 'cleaned_data.csv' 
data = pd.read_csv(csv_file)


conn = mysql.connector.connect(
    host='', 
    user='', 
    password='',  
    database='emploi'  
)
cursor = conn.cursor()


create_table_query = """
CREATE TABLE IF NOT EXISTS offres_emploi (
    Poste VARCHAR(255),
    Entreprise VARCHAR(255),
    Ville VARCHAR(255),
    Type_de_contrat VARCHAR(50),
    Experience VARCHAR(50),
    Lien TEXT
);
"""
cursor.execute(create_table_query)


insert_query = """
INSERT INTO offres_emploi (Poste, Entreprise, Ville, Type_de_contrat, Experience, Lien)
VALUES (%s, %s, %s, %s, %s, %s)
"""

data_tuples = [tuple(row) for row in data.to_numpy()]

cursor.executemany(insert_query, data_tuples)

conn.commit()

cursor.close()
conn.close()

print("Data has been successfully loaded into the MySQL database!")
