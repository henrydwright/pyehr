import logging
from uuid import uuid4

from flask import Flask, jsonify, make_response, request

from pyehr.core.base.base_types.identification import HierObjectID, PartyRef
from pyehr.core.rm.common.generic import PartyIdentified
from pyehr.server.apps.rest.blueprints.demographic import create_demographic_blueprint
from pyehr.server.change_control import VersionedStore
from pyehr.server.database.local import InMemoryDB

def create_app():
    logging.basicConfig(level=logging.DEBUG)

    SYSTEM_ID_HID = str(uuid4())
    SYSTEM_ID_STR = "com.eldonhealth.ehr1"
    LOCATION_BASE_URL = "http://localhost:5000"

    log = logging.getLogger("apps.rest")
    log.info("pyehr REST API server starting...")

    log.info("Initialising database")
    db = InMemoryDB()

    log.info("Initialising versioned store")
    vs = VersionedStore(
        db_engine=db,
        system_id=SYSTEM_ID_STR
    )

    logged_in_user_uuid = str(uuid4())

    logged_in_user = PartyIdentified(
        external_ref=PartyRef("local", "PERSON", HierObjectID(logged_in_user_uuid)),
        name="DR ABBEY EXAMPLE"
    )

    app = Flask(__name__)

    log.info("Registering / paths")
    @app.route("/", methods=['OPTIONS'])
    def options():
        resp = make_response(
            jsonify({
                "solution": "pyehr",
                "solution_version": "BUILD",
                "vendor": "Eldon Health",
                "restapi_specs_version": "1.0.3",
                "endpoints": [
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

    log.info("Registering /demographic paths")
    app.register_blueprint(create_demographic_blueprint(SYSTEM_ID_STR, LOCATION_BASE_URL, logged_in_user, db, vs))
    
    return app

