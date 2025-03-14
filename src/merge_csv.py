import os
import csv
import sys
import time
from colorama import Fore, Style, init

# Inizializza Colorama
init(autoreset=True)

# Directory e file di output
input_folder = os.path.normpath(os.path.join("data", "output")) 
output_file = os.path.normpath(os.path.join("data", "output", "combined_output.csv"))
print(Fore.CYAN + "Step 1/3: Controllo delle cartelle...")

# Verifica che la cartella di input esista
if not os.path.exists(input_folder):
    print(Fore.RED + f"❌ Errore: la cartella di input '{input_folder}' non esiste.")
    sys.exit(1)

# Ottieni la lista di file CSV
files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]

# Controlla se ci sono file CSV
if not files:
    print(Fore.YELLOW + f"⚠️ Nessun file CSV trovato nella cartella '{input_folder}'.")
    sys.exit(1)

print(Fore.GREEN + f"✅ Trovati {len(files)} file CSV.")

# Funzione per la barra di avanzamento
def progress_bar(iteration, total, length=30):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = "█" * filled_length + "-" * (length - filled_length)
    sys.stdout.write(f"\r[{bar}] {percent:.0f}%")
    sys.stdout.flush()

print(Fore.CYAN + "\nStep 2/3: Creazione del file di output...")

# Flag per scrivere l'intestazione solo una volta
header_written = False

# Crea e apri il file di output per la scrittura
try:
    with open(output_file, mode='w', newline='', encoding='utf-8') as output_csv_file:
        writer = csv.writer(output_csv_file, delimiter=';')

        print(Fore.GREEN + f"✅ File di output creato: {output_file}")

        print(Fore.CYAN + "\nStep 3/3: Unione dei file CSV...\n")

        # Itera sui file CSV con barra di avanzamento
        for index, filename in enumerate(files, start=1):
            input_path = os.path.join(input_folder, filename)
            print(Fore.BLUE + f"\n📄 Unendo file {index}/{len(files)}: {input_path}")

            # Apri il file CSV di input
            with open(input_path, mode='r', newline='', encoding='utf-8') as input_csv_file:
                reader = csv.reader(input_csv_file, delimiter=';')

                # Leggi l'intestazione
                try:
                    header = next(reader)
                except StopIteration:
                    print(Fore.YELLOW + f"⚠️ Il file {filename} è vuoto, viene saltato.")
                    continue

                # Scrivi l'intestazione solo per il primo file
                if not header_written:
                    writer.writerow(header)
                    header_written = True
                    print(Fore.GREEN + f"✅ Intestazione scritta da: {filename}")

                # Scrivi le righe successive (escludendo righe vuote)
                rows_written_for_file = 0
                for row in reader:
                    if any(row):  # Controlla se la riga non è vuota
                        writer.writerow(row)
                        rows_written_for_file += 1

                print(Fore.GREEN + f"✅ {rows_written_for_file} righe scritte da {filename}")

            # Aggiorna la barra di avanzamento
            progress_bar(index, len(files))
            time.sleep(0.3)

    print("\n\n" + Fore.GREEN + f"🎉 Tutti i file CSV sono stati uniti in: {output_file}")

except Exception as e:
    print(Fore.RED + f"❌ Errore durante la creazione o scrittura del file di output: {e}")
    sys.exit(1)
