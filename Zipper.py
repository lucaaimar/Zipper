import os
import zipfile
import configparser

setting_file = 'setting.ini'


# Funzione per ottenere i parametri dal file .ini
def get_config_from_ini(ini_file):
    config = configparser.ConfigParser()
    config.read(ini_file)
    zip_name = config['ZIP']['zip_name']
    file_extension = config['ZIP']['file_extension']
    return zip_name, file_extension


# Funzione per zippare i file con una determinata estensione
def zip_files_with_extension(ini_file=setting_file):
    # Ottieni il nome dello ZIP e l'estensione dei file dal file .ini
    zip_name, extension = get_config_from_ini(ini_file)

    # Ottieni il percorso della directory corrente
    current_dir = os.getcwd()
    # print(current_dir)

    # Crea/aggiorna il file ZIP
    with zipfile.ZipFile(zip_name, 'a', compression=zipfile.ZIP_DEFLATED) as zipf:  # 'a' per aggiungere file se lo ZIP esiste
        # Cerca tutti i file con l'estensione specificata nella directory corrente
        for foldername, subfolders, filenames in os.walk(current_dir):
            for filename in filenames:
                # print(filename)
                # print(extension)
                if filename.endswith(extension):
                    # print(extension)
                    file_path = os.path.join(foldername, filename)
                    # print(file_path)
                    # Aggiungi il file allo ZIP se non è già presente
                    if file_path not in zipf.namelist():
                        try:
                            zipf.write(file_path, os.path.relpath(file_path, current_dir))
                            print(f"Aggiunto: {file_path}")
                            # se va a buon fine l'inserimento nello zip cancello il file non zippato
                            os.remove(file_path)
                        except Exception as e:
                            print(f"Errore durante l'aggiunta del file '{file_path}': {e}")



if __name__ == '__main__':
    # conta i file da elaborare, con l'estensione selezionata, se non ci sono file da elaborare non faccio niente
    contatore_file = 0
    for foldername, subfolders, filenames in os.walk(os.getcwd()):
        for filename in filenames:
            if filename.endswith('.DAT'):
                contatore_file += 1
    if contatore_file == 0:
        print("Nessun file .DAT da elaborare.")
        exit(0)
    # Richiama la funzione principale per zippare i file
    zip_files_with_extension()

    print("ZIP creato con successo!")