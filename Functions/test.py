from eval import data_list, create_message
import pandas as pd

file = pd.read_csv('files\data.csv', delimiter=';')

G = data_list(file, 3)
lis_msj = G.apply(create_message, axis=1).tolist()
for i in lis_msj:
    print(i[0])
    print(i[1])
