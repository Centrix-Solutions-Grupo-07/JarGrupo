import speedtest as st
import time
from mysql.connector import connect
import pymssql
from slack_sdk import WebClient
from datetime import datetime

cnx = connect(user='root', password='38762', host='localhost', database='centrix')
speed_test = st.Speedtest()

sql_server_cnx = pymssql.connect(server='44.197.21.59', database='centrix', user='sa', password='centrix')

slack_token = 'xoxb-5806834878417-6181633164562-UNgjvP47AfYcw63CbQhHVGXS'
slack_channel = '#notificação'
slack_client = WebClient(token=slack_token)


limite_dow = 50
limite_up = 50

while(True):
    download = speed_test.download()
    download_mbs = round(download / (10**6), 2)
    
    upload = speed_test.upload()
    upload_mbs = round(upload / (10**6), 2)
    
    data_e_hora_atuais = datetime.now()
    data_atual = data_e_hora_atuais.date()
    hora_atual = data_e_hora_atuais.time()
       
    if upload_mbs < limite_up:
        message = f"Aviso: Velocidade de upload abaixo do ideal! ({upload_mbs}mbs)"
        slack_client.chat_postMessage(channel=slack_channel, text=message)

    if  download_mbs < limite_dow:
        message = f"Aviso: Velocidade de download abaixo do ideal! ({download_mbs}mbs)"
        slack_client.chat_postMessage(channel=slack_channel, text=message)
    
    bd = cnx.cursor()
    bdServer_cursor = sql_server_cnx.cursor()
    
    #DOWNLOAD
    dados_DOWNLOAD_PC = [download_mbs, 5, 13, 1]

    add_leitura_DOWNLOAD = ("INSERT INTO Monitoramento"
                       "(Data_captura, Hora_captura, Dado_Capturado, fkCompMoniExistentes, fkMaqCompMoni, fkEmpMaqCompMoni)"
                       "VALUES (%s, %s, %s, %s, %s, %s)")
    

    bd.execute(add_leitura_DOWNLOAD, (data_atual, hora_atual, download_mbs, 5, 13, 1))
    bdServer_cursor.execute(add_leitura_DOWNLOAD, (str(data_atual), str(hora_atual), download_mbs, 5, 13, 1))
    
    #UPLOAD
    dados_UPLOAD_PC = [upload_mbs, 5, 6, 13, 1]

    add_leitura_UPLOAD = ("INSERT INTO Monitoramento"
                       "(Data_captura, Hora_captura, Dado_Capturado, fkCompMoniExistentes, fkMaqCompMoni, fkEmpMaqCompMoni)"
                       "VALUES (%s, %s, %s, %s, %s, %s)")
    

    bd.execute(add_leitura_UPLOAD, (data_atual, hora_atual, upload_mbs, 6, 13, 1))

    bdServer_cursor.execute(add_leitura_UPLOAD, (str(data_atual), str(hora_atual), upload_mbs, 6, 13, 1))

    
    cnx.commit()
    sql_server_cnx.commit()
    bdServer_cursor.close()

    time.sleep(20)
