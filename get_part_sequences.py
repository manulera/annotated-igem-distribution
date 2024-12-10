"""
Download part sequences from iGEM registry and add them to the csv file as a new column
"""

import pandas as pd
import httpx
import asyncio


async def get_part_sequence(client, part_id):
    url = f"https://parts.igem.org/cgi/xml/part.cgi?part={part_id}"
    print("downloading sequence for", part_id)
    response = await client.get(url)
    response.raise_for_status()
    # Find the first seq_data tag and extract its content
    start_tag = "<seq_data>"
    end_tag = "</seq_data>"
    start_index = response.text.find(start_tag) + len(start_tag)
    end_index = response.text.find(end_tag)
    seq = response.text[start_index:end_index].strip()
    # Remove internal line breaks
    seq = seq.replace("\n", "")
    return seq


async def get_all_sequences(part_ids, max_concurrent=5):
    async with httpx.AsyncClient() as client:
        # Create a semaphore to limit concurrent tasks
        semaphore = asyncio.Semaphore(max_concurrent)

        async def get_sequence_with_limit(part_id):
            async with semaphore:
                return await get_part_sequence(client, part_id)

        tasks = [get_sequence_with_limit(part_id) for part_id in part_ids]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    data = pd.read_csv("2024_Parts_List.csv")
    # Now you can specify the number of concurrent tasks
    sequences = asyncio.run(get_all_sequences(data["Part Name"], max_concurrent=12))
    data["part_sequence"] = sequences
    data.to_csv("results/2024_Parts_List_with_sequences.csv", index=False)
