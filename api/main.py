"""Minimal FastAPI service."""

from __future__ import annotations

from agent.router import optimize_route
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class SolveRequest(BaseModel):
    addresses: list[str]


@app.post("/solve")
async def solve(req: SolveRequest):
    res = optimize_route(req.addresses)
    return {
        "order": res.order,
        "distance_km": res.distance_km,
        "duration_min": res.duration_min,
    }


@app.get("/job/{job_id}")
async def job(job_id: str):
    return {"job_id": job_id, "status": "pending"}
