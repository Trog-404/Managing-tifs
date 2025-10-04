import re

base_unit = ['m', 'A', 'V', 's', 'sec', 'volt']

unit_conversion = {
    # lunghezza (metro)
    'k': 10**3,
    'm': 10 ** (-3),
    'µ': 10 ** (-6),
    'u': 10 ** (-6),
    'n': 10 ** (-9),
    'p': 10 ** (-12),
}

# regex per dividere chiave=valore
line_pattern = r'^([^=]+?)\s*=\s*(.+)$'
# regex per estrarre numero + unità, se presente
num_unit_pattern = r'^([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*([^\d\s]*)$'


def read_external_file(file_to_read: str) -> dict:
    with open(file_to_read, encoding='latin-1') as f:
        new_dict = {}
        for line in f:
            match = re.match(line_pattern, line.strip())
            if not match:
                continue
            name, raw_value = match.groups()
            raw_value = raw_value.strip()
            # provo a separare numero e unità
            mu = re.match(num_unit_pattern, raw_value)
            if mu:
                value, unit = mu.groups()
                if unit is not None:
                    if unit in base_unit:
                        value = round(float(value), 15)
                        # Questo arrotondamento per ora funziona perché l'ultima cifra
                        # che proviene dai dati è successiva al pico e l'ho messa anche
                        # pià alta/bassa
                    elif unit not in base_unit and unit[:1] in unit_conversion.keys():
                        value = round(float(value) * unit_conversion[unit[:1]], 15)
                new_dict.setdefault(name, value)
            else:
                # non è un numero -> lascio stringa intera
                new_dict.setdefault(name, raw_value)
    return new_dict
