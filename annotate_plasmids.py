"""
Annotate plasmids using plannotate in parallel
"""

from plannotate.annotate import annotate
from plannotate import resources as rsc
from pandas import read_csv
import os
from multiprocessing import Pool


def annotate_plasmid(inSeq):
    recordDf = annotate(inSeq, is_detailed=True, linear=False)
    gbk = rsc.get_gbk(recordDf, inSeq, is_linear=False)
    csv = rsc.get_clean_csv_df(recordDf)

    return gbk, csv


def process_plasmid(row):
    plasmid_file = f"results/plasmids/{row['Part Name']}_plannotate.gb"
    csv_file = f"results/reports/{row['Part Name']}.csv"
    if not os.path.exists(plasmid_file):
        print(row["Part Name"])
        gbk, csv = annotate_plasmid(str(row["Full Plasmid Seq"]))
        with open(plasmid_file, "w") as f:
            f.write(gbk)
        csv.to_csv(csv_file, index=False)


if __name__ == "__main__":
    df = read_csv("results/2024_Parts_List_with_sequences.csv")

    with Pool() as pool:
        pool.map(process_plasmid, [row for _, row in df.iterrows()])
