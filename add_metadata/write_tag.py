import json
import os
from cffi import FFI
import re
import tifffile as tf
from read_external_file import read_external_file
import sys
import subprocess
import shutil

def load_registry(path="tag_registry.json"):
    if not os.path.exists(path):
        sys.exit(f"Errore: file {path} non trovato.")
    with open(path) as f:
        return json.load(f)

def write_metadata(file_tiff, instrument, metadata, registry, lib):
    if instrument not in registry:
        raise ValueError(f"The instrument '{instrument}' does not appear in the registry.")
    tag_code = registry[instrument]
    #Converti le sringhe in bytes per cffi
    file_tiff_b = file_tiff.encode('utf-8')
    tag_name_b = instrument.encode('utf-8')
    tag_value_b = metadata.encode('utf-8')
    
    with tf.TiffFile(file_tiff) as tiff:
        for count, page in enumerate(tiff.pages):
            if tag_code not in page.tags:
                res = lib.write_custom_tag(file_tiff_b, tag_code, tag_name_b, tag_value_b)
                if res == 0:
                    print(f"Tag scritto con successo nella pagina {count}")
                else:
                    print(f"Errore scrittura tag, codice: {res}")
            else:
                print(f"Tag {tag_code} già presente nella pagina {count}")    

if __name__ == '__main__':

    registry = load_registry()
    print("List of instruments actually supported:")
    for supported, tag in registry.items():
        print(f"Instrument {supported} with tag code {tag}")
    print ("Remember to choose one of these names to proceed")

    nome_script, file_tiff, instrument, file_path = sys.argv    
    print(f"""
    Il nome del file tiff da espandere è: {file_tiff}\n
    Il tipo di strumento selezionato è: {instrument}\n
    Il file sorgente dei metadati è: {file_path}\n""")
    control = input("Vuoi continuare? [y/N]: ").strip().lower()
    if control != "y":
        sys.exit("Operazione annullata.")
    
    json_str = json.dumps(read_external_file(file_path))
    print(f"DATI ESTRATTI:")
    print()
    print(json_str)
    print()
    ffi = FFI()
    # Definizione della funzione presente nella libreria C
    ffi.cdef("""
        int write_custom_tag(const char* filename,
                              unsigned short tag_code,
                              const char* tag_name,
                              const char* tag_value);
    """)
    lib_path = "./libmetadata_add.so"
    if os.path.exists(lib_path):
        os.remove(lib_path)    
    subprocess.run(["make"])
    
    lib = ffi.dlopen("./libmetadata_add.so")  # carica la libreria compilata
    src = f"./origin/{file_tiff}"
    dst= f"./outputs/{file_tiff}"
    shutil.copy2(src, dst)
    write_metadata(dst, instrument, json_str, registry, lib)