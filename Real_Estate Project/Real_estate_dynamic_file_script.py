import mysql.connector
from config import HOST,DB_PASSWORD,DB_USERNAME
import pandas as pd
try:
    connection=mysql.connector.connect(
        host=HOST,
        username=DB_USERNAME,
        password=DB_PASSWORD,
        database="real_estate_database"
    )
    query="SELECT * FROM housing_data_copy"
    df=pd.read_sql(query,connection)
    df.to_csv('real_estate_housing.csv',index=False)
    print("file creation done.")
except Exception as e:
    print(f"ERROR: {e}")
finally:
    connection.close()