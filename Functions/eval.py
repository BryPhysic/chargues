import pandas as pd

file = pd.read_csv('files\data.csv', delimiter=';')


def eval_p(file, n):
    def eval_cuota(row, cuota):
        name = str(row['nombre']).title()

        telf = str(row['telefono'])
        pago = float(str(row[f'pago_{cuota}']).replace(',', '.'))
        dif = float(str(row['v_cuota'].replace(',', '.'))) - 0.4
        saldo = dif - pago

        if pd.isnull(row[f'pago_{cuota}']):
            mensaje = f' - Pago pendiente correspondiente a la Cuota Número {cuota} por $ {row["v_cuota"]} '
            adeudado = dif
        elif pago < dif:
            mensaje = f' - Tiene un saldo pendiente de $ {saldo:.2f} correspondiente al la Cuota N {cuota}'
            adeudado = saldo
        else:
            mensaje = f' - Cuota Número {cuota} *al dia*.'
            adeudado = 0

        return {'Usuario': telf, 'mensaje': mensaje, 'valor_adeudado': adeudado,'name':name}

    def eval_certificado(row):
        name = str(row['nombre']).title()
        telf = str(row['telefono'])
        pago = float(str(row['certificado']).replace(',', '.'))
        dif = 35
        saldo = dif - pago

        if pd.isnull(row['certificado']):
            mensaje = f' - Valor pendiente del certificado por $ 35'
            adeudado = dif
        elif pago < dif:
            mensaje = f' - Tiene un saldo pendiente de $ {saldo:.2f} correspondiente al certificado.'
            adeudado = saldo
        else:
            mensaje = ' - al dia'
            adeudado = 0

        return {'Usuario': telf, 'mensaje': mensaje, 'valor_adeudado': adeudado,'name':name}

    msj = []
    for _, row in file.iterrows():
        if n in [1, 2, 3]:
            for i in range(1, n + 1):
                msj.append(eval_cuota(row, i))
        elif n == 'c':
            for i in range(1, 4):
                msj.append(eval_cuota(row, i))
            msj.append(eval_certificado(row))

    return msj

def data_list(file,n):

    G = eval_p(file,n)
    df = pd.DataFrame(G, columns=['Usuario', 'mensaje', 'valor_adeudado','name'])
    df_sum = df.groupby('Usuario')['valor_adeudado'].sum().reset_index()
    df_sum.columns = ['Usuario', 'total_adeudado']
    df_merged = df.merge(df_sum, on='Usuario')
    unique_totals = df_merged[['Usuario', 'total_adeudado']].drop_duplicates()
    unique_names = df_merged[['Usuario', 'name']].drop_duplicates()  # Crear un dataframe con valores únicos de 'Usuario' y 'name'
    def join_messages_and_total(messages, total_adeudado):
        joined_messages = '\n'.join(messages)
        return f'{joined_messages}\n - *Total adeudado:   ${total_adeudado:.2f}*'

    grouped_df = df_merged.groupby('Usuario').apply(lambda x: join_messages_and_total(x['mensaje'], x['total_adeudado'].iloc[0])).reset_index(name='mensaje')

    grouped_df = grouped_df.merge(unique_names, on='Usuario')  # Combinar el dataframe 'grouped_df' con el dataframe 'unique_names'
    return grouped_df


def create_message(row):
    name = row['name']
    valores = row['mensaje']
    numero = row['Usuario']
    msj = f'{numero}', f'Buenas tardes estimad@ {name}, Sciedtec le saluda, este mensaje es para mencionarle que sus saldos pendientes que corresponden a:\n\n{valores} '
    return msj

if __name__ == "__main__":
    data_list(file,1)
    create_message(row)
