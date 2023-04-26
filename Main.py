import Proyecto as Pr
import pandas as pd


directory = "C:\\Users\\jaime\\Documents\\ITAM\\Desarrollo de aplicaciones informáticas\\Python\\Equipo1\\"
df_amazon = Pr.read_file(directory, "Amazon.csv")
df_amex = Pr.read_file(directory, "AmericanExpress.csv")
df_astra = Pr.read_file(directory, "AstraZeneca.csv")
df_danone = Pr.read_file(directory, "Danone.csv")
df_netflix = Pr.read_file(directory, "Netflix.csv")

print(df_amazon)
print(Pr.find_month_values(df_amazon))
