# src/api/upload_api.py

import logging

from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Query

from src.services.policy_uploader import (
    save_policy_pdf,
    update_policy_mapping,
    ingest_all_policies,
)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    load_dotenv()
    logging.info("🔑 Loaded .env variables")

@app.post("/upload-policy")
async def upload_policy(
    policy_name: str = Query(..., description="Friendly name for this policy"),
    file: UploadFile = File(...),
):
    try:
        policy_id = await save_policy_pdf(file)

        update_policy_mapping(policy_id, policy_name)

        ingest_all_policies()

    except ValueError as ve:
        logging.error(f"[UploadAPI] Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logging.error(f"[UploadAPI] Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to process upload.")

    return {
        "detail": f"Policy '{policy_name}' (id: {policy_id}) uploaded, mapped, and indexed successfully."
    }



@app.get("/")
def health_check():
    return {"status": "ok"}
