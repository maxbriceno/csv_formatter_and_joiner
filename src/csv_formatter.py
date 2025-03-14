import os
import csv
import sys
import time
from colorama import Fore, Style, init

# Inizializza Colorama per Windows
init(autoreset=True)

# Definizione delle cartelle
input_folder = os.path.normpath(os.path.join("data"))
output_folder = os.path.normpath(os.path.join("data", "output"))

print(Fore.CYAN + "Step 1/3: Checking directories...")

# Verifica che la cartella di input esista
if not os.path.exists(input_folder):
    print(Fore.RED + f"❌ Error: input dir '{input_folder}' doesn't exist.")
    sys.exit(1)

# Assicurati che la cartella di output esista
try:
    os.makedirs(output_folder, exist_ok=True)
    print(Fore.GREEN + f"✅ Output dir '{output_folder}' ready.")
except OSError as e:
    print(Fore.RED + f"❌ Error in creation of the output dir: {e}")
    sys.exit(1)

print(Fore.CYAN + "\nStep 2/3: Searching CSV files...")

# Lista di file CSV nella cartella
files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]

# Controlla se ci sono file CSV
if not files:
    print(Fore.YELLOW + f"⚠️ No CSV file found in the directory '{input_folder}'.")
    sys.exit(1)

print(Fore.GREEN + f"✅ Found {len(files)} CSV files.")

# Funzione per stampare una barra di avanzamento ASCII
def progress_bar(iteration, total, length=30):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = "█" * filled_length + "-" * (length - filled_length)
    sys.stdout.write(f"\r[{bar}] {percent:.0f}%")
    sys.stdout.flush()

# Funzione per processare ogni file CSV
def process_csv_file(input_file, output_file, file_index, total_files):
    print(Fore.CYAN + f"\n📄 Processing file {file_index}/{total_files}: {input_file}")

    try:
        with open(input_file, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)

            with open(output_file, mode='w', newline='', encoding='utf-8') as new_file:
                writer = csv.writer(new_file, delimiter=';')

                for row in reader:
                    row = [value.replace('.', ',') if '.' in value else value for value in row]
                    writer.writerow(row)
                    # print(Fore.YELLOW + f"✏️  Modified: {second_last_value} -> {row[-2]}")

                    writer.writerow(row)

        print(Fore.GREEN + f"✅ File successfully elaborated: {output_file}")
    except Exception as e:
        print(Fore.RED + f"❌ Error during r/w of {input_file}: {e}")

# Step 3: Processamento dei file CSV con barra di avanzamento
print(Fore.CYAN + "\nStep 3/3: Elaborating CSV file...\n")

for index, filename in enumerate(files, start=1):
    input_path = os.path.join(input_folder, filename)
    original_name = filename.split(".")
    output_path = os.path.join(output_folder, original_name[0]+ "_formatted.csv")

    process_csv_file(input_path, output_path, index, len(files))

    # Aggiorna la barra di avanzamento
    progress_bar(index, len(files))
    time.sleep(0.3)  # Ritardo per rendere la barra più visibile

print("\n\n" + Fore.GREEN + "🎉 All files have been successfully elaborated!")
