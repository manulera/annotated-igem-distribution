# iGEM 2024 Distribution annotated

A set of scripts to annotate the iGEM 2024 distribution using [pLannotate](https://github.com/mmcguffi/pLannotate).

## Dependencies

### Non-Python dependencies

This project runs pLannotate not as a conda dependency, but as a pip dependency. To see how
to do this, see [this plannotate fork](https://github.com/manulera/plannotate).

This means, you have to install the command-line dependencies yourself, but it's not hard! See [this readme section](https://github.com/manulera/plannotate?tab=readme-ov-file#non-python-dependencies).

### Python dependencies

This project uses [poetry](https://python-poetry.org/docs/) to manage Python dependencies. Once, you have the previous dependencies installed, you can install the Python dependencies with:

```bash

poetry install

# Activate the virtual environment
poetry shell

# Download plannotate databases
python download_plannotate_databases.py

# Ready to go!
```

### External files

The file `2024_Parts_List.csv` contains the list of plasmids and comes from the [iGEM airtable](https://airtable.com/appgWgf6EPX5gpnNU/shrb0c8oYTgpZDRgH/tblNqHsHbNNQP2HCX).


## Running the pipeline

### Downloading part sequences

```bash
python get_part_sequences.py
```

This will download the sequences of the parts and add them to the `2024_Parts_List.csv` file as a new column, the result will be in `results/2024_Parts_List_with_sequences.csv`.

### Annotating plasmids with pLannotate

```bash
python annotate_plasmids.py
```

For each plasmid sequence in the `results/2024_Parts_List_with_sequences.csv` file, this script will:

- Annotate the sequence using pLannotate and save it to `results/plasmids/{part_name}_plannotate.gb`
- Save the annotation report to `results/reports/{part_name}.csv`

### Annotating parts

```bash
python annotate_parts.py
```

This script will add extra annotation to the gb files produced by pLannotate.

- If a feature found by pLannotate matches the part, it will rename it to `{part_name} / {part_id}` and add a `db_xref` qualifier with the part id.
- Otherwise, it will add a new feature with that label. It will try to guess the type from the `Part Type (unified)` column (see the dictionary `type_mapping` in the script).
- Will save the annotated file to `results/parts/{part_name}.gb`

### Building an index

```bash
python make_index.py
```

This script will turn the `2024_Parts_List.csv` file into `results/index.json`, a json file with the same information (without the sequences), that can be used as an index of what's in the repository.

## Accessing plasmids programmatically

You can make a request to get the files directly from github using a url like this:

```
https://raw.githubusercontent.com/manulera/annotated-igem-distribution/master/results/plasmids/{part_name}.gb
```

For instance, to get the plasmid file for `BBa_C0062`, you can do:

https://raw.githubusercontent.com/manulera/annotated-igem-distribution/master/results/plasmids/BBa_C0062.gb

This will return the gb file for the plasmid.

Similarly, you can get annotation info from plannotate using a url like this:

```
https://raw.githubusercontent.com/manulera/annotated-igem-distribution/master/results/reports/{part_name}.csv
```

For instance, to get the annotation report for `BBa_C0062`, you can do:

https://raw.githubusercontent.com/manulera/annotated-igem-distribution/master/results/reports/BBa_C0062.csv
