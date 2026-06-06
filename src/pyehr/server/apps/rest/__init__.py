import logging
from uuid import uuid4
from pathlib import Path
import os
import json
import sys

from flask import Flask, jsonify, make_response, request
from dotenv import load_dotenv

from pyehr.core.base.base_types.identification import HierObjectID, PartyRef
from pyehr.core.its.json_tools import decode_json
from pyehr.core.rm.common.generic import PartyIdentified
from pyehr.core.rm.support.terminology import TerminologyService
from pyehr.server.apps.rest.blueprints.demographic import create_demographic_blueprint
from pyehr.server.apps.rest.blueprints.ehr import create_ehr_blueprint
from pyehr.server.change_control import VersionedStore
from pyehr.server.database import IDatabaseEngine, ObjectAlreadyExistsError
from pyehr.server.database.local import InMemoryDB
from pyehr.server.database.mongodb import MongoDBDatabaseEngine
from pyehr.server.security.auth import IPyehrAuthProvider
from pyehr.server.security.auth.noauth import AllowAllAuthProvider

from pyehr.term import PyehrGlobalTerminologyService

def preload_content(root: Path, db: IDatabaseEngine, term_svc: TerminologyService, log: logging.Logger):
    """Preload all content under a given folder structure into the EHR, checking if it already
    exists in the database"""
    jsons = root.glob("*.json")
    for json_f in jsons:
        log.info(f"Preloading... {json_f.as_posix()}")
        with json_f.open("r") as json_fh:
            py_obj = decode_json(json.load(json_fh), terminology_service=term_svc)
            try:
                db.create_uid_object(py_obj)
            except ObjectAlreadyExistsError:
                log.info(f"Object already existed, skipping.")
    for child in root.iterdir():
        if child.is_dir():
            preload_content(child, db, term_svc, log)

def create_app():
    app = Flask(__name__)

    lvl = logging.INFO
    if "SERVER_LOG_LEVEL" in app.config:
        if app.config["SERVER_LOG_LEVEL"] == "DEBUG":
            lvl = logging.DEBUG
        elif app.config["SERVER_LOG_LEVEL"] == "INFO":
            lvl = logging.INFO
        else:
            print("Log level not recognised, setting to INFO")

    logging.basicConfig(level=lvl)
    log = logging.getLogger("apps.rest")
    log.info("pyehr REST API server starting...")

    log.info(f"Loading config from: {os.getenv("PYEHR_REST_CONFIG")}")
    app.config.from_envvar("PYEHR_REST_CONFIG")

    log.info("Using parameter settings of:")
    log.info(f"SYSTEM_ID_STR: {app.config["SYSTEM_ID_STR"]}")
    log.info(f"SYSTEM_ID_HID: {app.config["SYSTEM_ID_HID"]}")
    log.info(f"BASE_URL: {app.config["BASE_URL"]}")

    
    db = None
    if app.config["DB_TYPE"] == "InMemory":
        log.info("Initialising database 'InMemory'")
        db = InMemoryDB()
    elif app.config["DB_TYPE"] == "MongoDB":
        log.info("Initialising database 'MongoDB'")
        if ("DB_MONGO_CONNECTION_STRING" not in app.config) or ("DB_MONGO_DATABASE_NAME" not in app.config):
            log.error("Could not initialise database: either 'DB_MONGO_CONNECTION_STRING' or 'DB_MONGO_DATABASE_NAME' are not set")
            sys.exit(1)
        db = MongoDBDatabaseEngine(connection_string=app.config["DB_MONGO_CONNECTION_STRING"], database_name=app.config["DB_MONGO_DATABASE_NAME"])
    else:
        log.error("Could not initialise database: 'DB_TYPE' not recognised, must be one of 'InMemory' or 'MongoDB'")
        sys.exit(1)

    log.info("Initialising OpenEHR terminology")
    term_svc = PyehrGlobalTerminologyService.get_global_terminology_service()

    if "CONTENT_PRELOAD_FOLDER" in app.config:
        log.info(f"Preloading content from {app.config["CONTENT_PRELOAD_FOLDER"]}")
        preload_content(Path(app.config["CONTENT_PRELOAD_FOLDER"]), db, term_svc, log)

    log.info("Initialising versioned store")
    vs = VersionedStore(
        db_engine=db,
        system_id=app.config["SYSTEM_ID_STR"],
        terminology_service=term_svc
    )

    log.info("Initialising auth provider")
    auth_type = app.config["AUTH_TYPE"].lower()
    auth_provider : IPyehrAuthProvider = None
    log.info(f"Auth type = \'{auth_type}\'")
    if auth_type == "noauth":
        auth_provider = AllowAllAuthProvider(
            execute_as=PartyIdentified(
                external_ref=PartyRef("local", "AGENT", HierObjectID("d0000000-0000-0000-FF00-FFFFFFFF0000")),
                name="Anonymous"
            ),
            db=db
        )
    
    auth_provider.setup()

    log.info("Registering / paths")
    @app.route("/", methods=['OPTIONS'])
    def options():
        endpoints = ["/"]
        if app.config["ENDPOINT_DEMOGRAPHICS_ENABLED"]:
            endpoints.append("/demographic")
        if app.config["ENDPOINT_EHR_ENABLED"]:
            endpoints.append("/ehr")
        resp = make_response(
            jsonify({
                "solution": "pyehr",
                "solution_version": "BUILD",
                "vendor": "Eldon Health",
                "restapi_specs_version": "1.0.3",
                "endpoints": [
                    "/",
                    "/ehr",
                    "/demographic"
                ]
            }))
        resp.headers.add("Allow", "GET, POST, PUT, DELETE, OPTIONS")
        resp.headers.add("Content-Type", "application/json")
        resp.status_code = 200
        return resp

    @app.route("/", methods=['GET'])
    def web_home():
        return "<h1>pyehr REST API Server</h1><p>You have reached an OpenEHR server running on pyehr.</p>"

    if app.config["ENDPOINT_DEMOGRAPHICS_ENABLED"]:
        log.info("Registering /demographic paths")
        app.register_blueprint(create_demographic_blueprint(auth_provider, db, vs))
    
    if app.config["ENDPOINT_EHR_ENABLED"]:
        log.info("Registering /ehr paths")
        app.register_blueprint(create_ehr_blueprint(auth_provider, db, vs))

    return app

