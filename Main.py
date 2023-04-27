import Proyecto as Pr


directory = "C:\\Users\\jaime\\Documents\\ITAM\\Desarrollo de aplicaciones informáticas\\Python\\Equipo1\\"
df_amazon = Pr.read_file(directory, "Amazon.csv")

print(df_amazon)
print(Pr.find_month_values(df_amazon))
Pr.total_transactions(df_amazon)
Pr.earnings(df_amazon)
print(df_amazon)

Pr.plot_shares(df_amazon, "Close/Last")
