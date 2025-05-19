import pandas as pd
import io
from utils.json_formatter import format_feedback_json
from utils.mongo_connector import save_feedback_to_mongo
from fastapi import UploadFile
from typing import Dict

async def process_csv(file: UploadFile) -> Dict:
    try:
        # Reset pointer in case it was read earlier
        file.file.seek(0)

        # Read CSV file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))

        if 'feedback_text' not in df.columns:
            return {"error": "CSV must contain a 'feedback_text' column."}

        processed = 0
        skipped = 0

        for index, row in df.iterrows():
            try:
                feedback_text = str(row['feedback_text']).strip()
                if not feedback_text or pd.isna(feedback_text):
                    skipped += 1
                    continue

                user_id = str(row.get('user_id', 'anonymous')).strip()

                # Run the analysis and save
                result = format_feedback_json(feedback_text, user_id)
                save_feedback_to_mongo(result)
                processed += 1

            except Exception as e:
                skipped += 1
                print(f"[Row {index}] Skipped due to error: {e}")

        return {
            "status": "success",
            "total": len(df),
            "processed": processed,
            "skipped": skipped
        }

    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}
