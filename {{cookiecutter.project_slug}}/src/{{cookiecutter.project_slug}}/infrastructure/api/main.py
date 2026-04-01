"""HTTP application entry point.

This file creates and configures the web application instance.
It is the outermost layer of the system — the only place that knows
about the HTTP framework and wires everything together at startup.

The examples below use FastAPI, but the same pattern works with any
ASGI or WSGI framework (Flask, Litestar, Django, etc.).

To use FastAPI:
    pip install fastapi uvicorn

To run the server:
    uv run uvicorn {{ cookiecutter.project_slug }}.infrastructure.api.main:app --reload
    # or via Makefile:
    make run-api

Conventions:
    - Application-level configuration (CORS origins, middleware, lifespan) lives here.
    - Routers are registered here; business logic stays in application/.
    - Do not put route handlers in this file — use routers/ for that.
"""

# TODO: Install your chosen web framework and uncomment the relevant block.

# ── FastAPI example ───────────────────────────────────────────────────────────
#
# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from {{ cookiecutter.project_slug }}.infrastructure.api.routers import agent, health
#
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup: initialize expensive resources (DB pools, SDK clients, etc.)
#     yield
#     # Shutdown: close connections gracefully
#
#
# app = FastAPI(
#     title="{{ cookiecutter.project_name }}",
#     version="0.1.0",
#     lifespan=lifespan,
# )
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Restrict in production
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# app.include_router(health.router, prefix="/health", tags=["health"])
# app.include_router(agent.router, prefix="/agent", tags=["agent"])
# ─────────────────────────────────────────────────────────────────────────────

# TODO: Implement your application entry point above.
