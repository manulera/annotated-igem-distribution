from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, SimpleLocation
from Bio.SeqRecord import SeqRecord
from pandas import read_csv

type_mapping = {
    "terminator": "terminator",
    "cds": "CDS",
    "promoter": "promoter",
    "rbs": "RBS",
    "device": "device",
    "5' UTR": "5'UTR",
    "3' UTR": "3'UTR",
    "rbs_tag": "RBS tag",
    "n2_tag": "N2 tag",
    "n3_tag": "N3 tag",
    "origin": "rep_origin",
    "marker": "CDS",
    "polyA": "CDS",
    "tag": "CDS",
    "linker": "CDS",
    "protease cleavage domain": "CDS",
}


def annotate_part(plasmid_record: SeqRecord, part_id, part_sequence, plasmid_name):
    # Rename the record
    plasmid_record.name = part_id
    for feature in plasmid_record.features:
        feature: SeqFeature
        if feature.location.extract(plasmid_record.seq) == part_sequence:
            feature.qualifiers["label"] = [f"{plasmid_name} / {part_id}"]
            if "db_xref" in feature.qualifiers:
                feature.qualifiers["db_xref"].append(part_id)
            else:
                feature.qualifiers["db_xref"] = [part_id]
            return plasmid_record
    # If the part is not found, find it's coordinates and add it as a new feature
    full_circ = (str(plasmid_record.seq) * 2).upper()
    start = full_circ.find(part_sequence.upper())
    if start == -1:
        raise ValueError(f"Part {part_id} not found in plasmid")
    end = start + len(full_circ)
    new_feature = SeqFeature(
        location=SimpleLocation(start, end),
        type="misc_feature",
        qualifiers={"label": f"{plasmid_name} / {part_id}", "db_xref": part_id},
    )
    plasmid_record.features.append(new_feature)


if __name__ == "__main__":
    df = read_csv("results/2024_Parts_List_with_sequences.csv")
    for index, row in df.iterrows():
        plasmid_file_in = f"results/plasmids/{row['Index ID']}_plannotate.gb"
        plasmid_file_out = f"results/plasmids/{row['Index ID']}.gb"
        plasmid_record: SeqRecord = SeqIO.read(plasmid_file_in, "genbank")
        annotate_part(
            plasmid_record,
            row["Part Name"],
            row["part_sequence"],
            row["Short Desc / Name"],
        )
        with open(plasmid_file_out, "w") as f:
            SeqIO.write(plasmid_record, f, "genbank")
