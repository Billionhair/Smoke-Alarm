from __future__ import annotations
import json
from typing import Sequence
from google.oauth2 import service_account
from .config import cfg

def get_credentials(scopes: Sequence[str]):
    with open(cfg.sa_path, "r") as f:
        info = json.load(f)
    creds = service_account.Credentials.from_service_account_info(info, scopes=list(scopes))
    if cfg.subject_email:
        creds = creds.with_subject(cfg.subject_email)
    return creds
