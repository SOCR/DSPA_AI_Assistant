import supabase
import json
import os
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()

embedder = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_embeddings(text: str):
    # Handle potential empty strings
    if not text or not text.strip():
        # Return a zero vector or handle as appropriate
        # Using a zero vector of the expected dimension (1536 for text-embedding-3-small)
        print("Warning: Empty string encountered for embedding. Returning zero vector.")
        return [0.0] * 1536
    try:
        return embedder.embeddings.create(input=[text.strip()], model="text-embedding-3-small").data[0].embedding
    except Exception as e:
        print(f"Error creating embedding for text: '{text[:100]}...': {e}")
        # Decide how to handle errors, e.g., return zero vector or skip
        return [0.0] * 1536


def main():
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    supabase_client = supabase.create_client(supabase_url, supabase_key)

    source_dir = "parsed_docs/"
    try:
        files_to_extract = [f for f in os.listdir(source_dir) if f.endswith(".json")]
    except FileNotFoundError:
        print(f"Error: Directory '{source_dir}' not found.")
        return

    if not files_to_extract:
        print(f"No JSON files found in '{source_dir}'.")
        return

    print(f"Found {len(files_to_extract)} JSON files to process.")

    for file in tqdm(files_to_extract, desc="Processing files"):
        file_path = os.path.join(source_dir, file)
        # Extract chapter name from filename (e.g., "05_SupervisedClassification_parsed.json" -> "05_SupervisedClassification")
        chapter_name = file.removesuffix('_parsed.json') # More robust than replace

        try:
            with open(file_path, 'r', encoding='utf-8') as f: # Specify encoding
                data = json.load(f)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}. Skipping.")
            continue
        except Exception as e:
            print(f"Error reading file {file_path}: {e}. Skipping.")
            continue

        batch_inserts = [] # Initialize batch list for this file

        # Process sections
        for section in data.get("sections", []):
            title = section.get("title", "").strip()
            content = section.get("content", "").strip()
            # if section['content'] != '': # Content check is good, let's make it more robust
            if title and content: # Only insert if both title and content exist
                embedding = create_embeddings(title) # Embed based on title
                batch_inserts.append(
                    {
                        "title": title,
                        "content": content,
                        "type": "section",
                        "chapter": chapter_name, # Use extracted chapter name
                        "embedding": embedding,
                    }
                )

        # Process tables
        for table in data.get("tables", []):
            section_title = table.get("section", "").strip()
            content = table.get("content", "").strip()
            if section_title and content:
                embedding = create_embeddings(section_title) # Embed based on section title
                batch_inserts.append(
                    {
                        "title": section_title, # Use section title as the main title
                        "content": content, # Assumes content is the table's text/markdown
                        "type": "table",
                        "chapter": chapter_name, # Use extracted chapter name
                        "embedding": embedding,
                    }
                )

        # Process R code
        for code in data.get("r_code", []):
            section_title = code.get("section", "").strip()
            code_content = code.get("code", "").strip()
            if section_title and code_content:
                embedding = create_embeddings(section_title) # Embed based on section title
                batch_inserts.append(
                    {
                        "title": section_title, # Use section title
                        "content": code_content,
                        "type": "r_code",
                        "chapter": chapter_name, # Use extracted chapter name
                        "embedding": embedding,
                    }
                )

        # Insert the batch for the current file if not empty
        if batch_inserts:
            try:
                supabase_client.table("dspa_docs").insert(batch_inserts).execute()
                # Optional: Add logging for successful batch insert
                # print(f"Successfully inserted batch of {len(batch_inserts)} items for file {file}.")
            except Exception as e:
                print(f"Error inserting batch for file {file}: {e}")
                # Optional: Add more robust error handling here, e.g., retry logic or saving failed batches

if __name__ == "__main__":
    main()



