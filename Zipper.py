import os
import zipfile
import configparser
from tqdm import tqdm

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

    # Crea/aggiorna il file ZIP
    with zipfile.ZipFile(zip_name, 'a', compression=zipfile.ZIP_DEFLATED) as zipf:  # 'a' per aggiungere file se lo ZIP esiste
        # Cerca tutti i file con l'estensione specificata nella directory corrente
        files_to_zip = []
        for foldername, subfolders, filenames in os.walk(current_dir):
            for filename in filenames:
                if filename.endswith(extension):
                    file_path = os.path.join(foldername, filename)
                    files_to_zip.append(file_path)

        # Se non ci sono file, interrompi l'esecuzione
        if not files_to_zip:
            print(f"Nessun file {extension} da elaborare.")
            return

        # Inizializza la barra di progresso con il numero di file da zippare
        with tqdm(total=len(files_to_zip), desc=f"Compressione dei file in corso", unit="file") as pbar:
            for file_path in files_to_zip:
                # Aggiungi il file allo ZIP se non è già presente
                if file_path not in zipf.namelist():
                    try:
                        zipf.write(file_path, os.path.relpath(file_path, current_dir))
                        # print(f"Aggiunto: {file_path}", flush=True)
                        # se va a buon fine l'inserimento nello zip cancello il file non zippato
                        os.remove(file_path)
                    except Exception as e:
                        print(f"Errore durante l'aggiunta del file '{file_path}': {e}")
                # Aggiorna la barra di avanzamento
                pbar.update(1)


if __name__ == '__main__':
    # conta i file da elaborare, con l'estensione selezionata
    contatore_file = 0
    # ottengo l'estensione da usare
    extension = get_config_from_ini(setting_file)[1]
    for foldername, subfolders, filenames in os.walk(os.getcwd()):
        for filename in filenames:
            if filename.endswith(f'.{extension}'):
                contatore_file += 1


    if contatore_file == 0:
        print(f'Nessun file {extension} da elaborare.')
        input("Premi Invio per uscire...")
        exit(0)
    else:
        print(f"Ci sono {contatore_file} file da elaborare.")

    # Richiama la funzione principale per zippare i file
    zip_files_with_extension()

    print("ZIP creato con successo!")
    input("Premi Invio per uscire...")
