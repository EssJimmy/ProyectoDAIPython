import Proyecto as Pr


directory = "C:\\Users\\jaime\\Documents\\ITAM\\Desarrollo de aplicaciones informáticas\\Python\\Equipo1\\"

df_amazon = Pr.read_file(directory, "Amazon.csv")
df_amex = Pr.read_file(directory, "AmericanExpress.csv")
df_astra = Pr.read_file(directory, "AstraZeneca.csv")
df_danone = Pr.read_file(directory, "Danone.csv")
df_netflix = Pr.read_file(directory, "Netflix.csv")
df_list = [df_amazon, df_amex, df_astra, df_danone, df_netflix]
names_list = ["Amazon", "Amex", "AstraZeneca", "Danone", "Netflix"]

for frame in df_list:
    Pr.total_transactions(frame)
    Pr.earnings(frame)

Pr.plot_shares(df_list, "Ganancias", names_list)
