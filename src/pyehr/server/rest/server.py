import json
from flask import Flask

import logging
from uuid import uuid4

from pyehr.core.base.base_types.builtins import Env
from pyehr.core.base.base_types.identification import ArchetypeID, HierObjectID, ObjectRef, PartyRef
from pyehr.core.rm.common.archetyped import Archetyped
from pyehr.core.rm.common.generic import PartyIdentified, PartySelf
from pyehr.core.rm.data_types.quantity.date_time import DVDateTime
from pyehr.core.rm.data_types.text import DVText
from pyehr.core.rm.ehr import EHR, EHRAccess, EHRStatus
from pyehr.server.change_control import VersionLifecycleState, VersionedStore
from pyehr.server.database.local import InMemoryDB

logging.basicConfig(level=logging.DEBUG)

SYSTEM_ID_HID = str(uuid4())
SYSTEM_ID_STR = "com.eldonhealth.ehr1"

log = logging.getLogger("RestAPIServer")

db = InMemoryDB()

vs = VersionedStore(
    db_engine=db,
    system_id=SYSTEM_ID_STR
)

logged_in_user = PartyIdentified(
    external_ref=PartyRef("local", "PERSON", str(uuid4())),
    name="DR ABBEY EXAMPLE"
)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def web_home():
    return "<h1>pyehr REST API Server</h1><p>You have reached an OpenEHR server running on pyehr.</p>"

@app.route("/ehr", methods=['POST', 'GET'])
def create_ehr():
    new_ehr_uid = db.generate_hier_object_id()
    new_ehr_status = EHRStatus(
        name=DVText("EHR Status"),
        archetype_node_id="openEHR-EHR-EHR_STATUS.generic.v1",
        archetype_details=Archetyped(ArchetypeID("openEHR-EHR-EHR_STATUS.generic.v1"), rm_version="1.1.0"),
        subject=PartySelf(),
        is_queryable=True,
        is_modifiable=True
    )
    new_ehr_status_vid, nes_contrib, nes_vo = vs.create(
        obj=new_ehr_status,
        owner_id=ObjectRef("local", "EHR", new_ehr_uid),
        committer=logged_in_user,
        lifecycle_state=VersionLifecycleState.COMPLETE,
        user=logged_in_user.external_ref
    )
    new_ehr = EHR(
        system_id=HierObjectID(SYSTEM_ID_HID),
        ehr_id=new_ehr_uid,
        ehr_status=ObjectRef("local", "VERSIONED_EHR_STATUS", nes_vo.uid),
        ehr_access=ObjectRef("local", "VERSIONED_EHR_ACCESS", db.generate_hier_object_id()),
        time_created=DVDateTime(Env.current_date_time())
    )
    db.create_uid_object(
        obj=new_ehr,
        creator=logged_in_user.external_ref
    )
    return new_ehr.as_json()

@app.route("/ehr/<uuid:ehr_id>", methods=['GET'])
def get_ehr_by_id(ehr_id):
    ehr = db.retrieve_uid_object(
        obj_type="EHR",
        uid=HierObjectID(str(ehr_id)),
        reader=logged_in_user.external_ref
    )
    return ehr.as_json()
