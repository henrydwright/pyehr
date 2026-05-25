

from enum import Enum
from typing import Optional

from pyehr.core.base.base_types.identification import HierObjectID, ObjectRef, PartyRef
from pyehr.core.base.foundation_types.any import AnyClass
from pyehr.core.base.foundation_types.structure import is_equal_value
from pyehr.core.rm.common.change_control import VersionedObject
from pyehr.core.rm.ehr import AccessControlSettings

class PyehrAccessPolicyEndpoint(Enum):
    """Enum of the different REST API endpoints an access policy may act upon."""

    EHR = "ehr"
    """All endpoints relating to the EHR object, namely:
    * /ehr
    * /ehr/{ehr_id}"""

    EHR_STATUS = "ehr_status"
    """All endpoints relating to the EHR_STATUS object, namely:
    * /ehr/{ehr_id}/ehr_status
    * /ehr/{ehr_id}/versioned_ehr_status
    * /ehr/{ehr_id}/versioned_ehr_status/revision_history
    * /ehr/{ehr_id}/versioned_ehr_status/version
    * /ehr/{ehr_id}/versioned_ehr_status/version/{version_id}"""
    
    EHR_ACCESS = "ehr_access"
    """All endpoints relating to the EHR_ACCESS object."""

    EHR_COMPOSITION = "ehr_composition"
    """All endpoints relating to COMPOSITION objects within an EHR, namely:
    * /ehr/{ehr_id}/composition
    * /ehr/{ehr_id}/composition/{composition_id}
    * /ehr/{ehr_id}/versioned_composition/{composition_id}
    * /ehr/{ehr_id}/versioned_composition/{composition_id}/revision_history
    * /ehr/{ehr_id}/versioned_composition/{composition_id}/version
    * /ehr/{ehr_id}/versioned_composition/{composition_id}/version/{version_id}"""

    EHR_DIRECTORY = "ehr_directory"
    """All endpoints relating to FOLDER objects within an EHR, namely:
    * /ehr/{ehr_id}/directory
    * /ehr/{ehr_id}/directory/{version_id}"""

    EHR_CONTRIBUTION = "ehr_contribution"
    """All endpoints relating to reading and writing CONTRIBUTION sets, namely:
    * /ehr/{ehr_id}/contribution
    * /ehr/{ehr_id}/contribution/{contribution_id}
    
    **Warning:** Enabling this will permit sets of COMPOSITIONS and FOLDERs to be
    acted upon, even if EHR_DIRECTORY and EHR_COMPOSITION permissions have not been
    given."""

    DEMOGRAPHIC_AGENT = "demographic_agent"

    DEMOGRAPHIC_GROUP = "demographic_group"

    DEMOGRAPHIC_ORGANISATION = "demographic_organisation"

    DEMOGRAPHIC_PERSON = "demographic_person"

    DEMOGRAPHIC_ROLE = "demographic_role"

    DEMOGRAPHIC_VERSIONED_PARTY = "demographic_versioned_party"

    DEMOGRAPHIC_CONTRIBUTION = "demographic_contribution"


class PyehrAccessPolicyEndpointAction(Enum):
    """Enum of the different actions that may be taken at an endpoint"""

    GET = "get"
    """Any action relating to reading the contents of the item
    itself at the endpoint."""

    CREATE = "create"
    """Any action relating to creating new items at the endpoint.
    This is required to commit contribution sets."""

    UPDATE = "update"
    """Any action relating to updating an already existing item at
    the endpoint. This is required to commit contribution sets or
    use soft deletion."""


class PyehrAccessPolicyItem(AnyClass):
    """Individual access control line item, used to build an overall
    policy."""

    roles: Optional[set[PartyRef]]
    """Set of references to ROLEs in the demographic service to which
    this policy applies. (If None, assume to match all roles)"""

    actions: Optional[set[PyehrAccessPolicyEndpointAction]]
    """Actions to which this policy applies (if None, assume to 
    apply to all actions)"""
    
    endpoints: Optional[set[PyehrAccessPolicyEndpoint]]
    """Resource endpoint to which this policy applies (if None, assumed 
    to apply to all resource endpoints)"""

    archetype_ids: Optional[set[str]]
    """List of archetype_ids that this rule should match in the request body 
    or in the response object (dependant on action). This will match the 
    archetype_node_id in the top level object being retrieved. (if None, 
    assume to apply to all archetype_ids)"""

    allow_action: bool
    """If set to True, the `action(s)` are allowed. If set to False,
    they are denied/blocked."""

    def __init__(self, allow_action: bool, 
                 roles: Optional[set[PartyRef]] = None, 
                 actions: Optional[set[PyehrAccessPolicyEndpointAction]] = None,  
                 endpoints: Optional[set[PyehrAccessPolicyEndpoint]] = None,
                 archetype_id: Optional[set[str]] = None,
                 **kwargs):
        self.allow_action = allow_action
        self.roles = roles
        self.actions = actions
        self.endpoints = endpoints
        self.archetype_ids = archetype_id
        super().__init__(**kwargs)

    def as_json(self):
        draft = {}
        if self.roles is not None:
            draft["roles"] = [role.as_json() for role in self.roles]
        if self.actions is not None:
            draft["actions"] = [action.value for action in self.actions]
        if self.endpoints is not None:
            draft["endpoints"] = [endpoint.value for endpoint in self.endpoints]
        if self.archetype_ids is not None:
            draft["archetype_ids"] = [archetype_id for archetype_id in self.archetype_ids]
        draft["allow_action"] = self.allow_action
        draft["_type"] = "PYEHR_ACCESS_POLICY_ITEM"
        return draft
    
    def is_equal(self, other: 'PyehrAccessPolicyItem'):
        return (type(self) == type(other) and
                is_equal_value(self.roles, other.roles) and
                is_equal_value(self.actions, other.actions) and
                is_equal_value(self.endpoints, other.endpoints) and
                is_equal_value(self.archetype_ids, other.archetype_ids) and
                is_equal_value(self.allow_action, other.allow_action))

class PyehrAccessControlSettings(AccessControlSettings):
    """pyehr-specific implementation of ACCESS_CONTROL_SETTINGS on an EHR
    built to allow rule sets to be built in layers up to a specific policy
    for an individual EHR."""
    
    base_upon: Optional[ObjectRef]
    """Reference to settings to import before adding policies within
    these settings. The object ref may either be a HIER_OBJECT_ID, in which
    case the latest version of the references settings is used as the base, or
    OBJECT_VERSION_ID in which case the specific version referenced is used."""

    policies: Optional[list[PyehrAccessPolicyItem]]
    """List of policies to apply, in the order given in the list."""

    uid: Optional[HierObjectID]
    """Unique identifier for this set of access control policies"""

    def __init__(self, base_upon: Optional[ObjectRef] = None, policies: Optional[list[PyehrAccessPolicyItem]] = None, uid: Optional[HierObjectID] = None, **kwargs):
        self.base_upon = base_upon
        self.policies = policies
        self.uid = uid
        super().__init__(**kwargs)

    def as_json(self):
        draft = {}
        if self.base_upon is not None:
            draft["base_upon"] = self.base_upon.as_json()
        if self.policies is not None:
            draft["policies"] = [policy.as_json() for policy in self.policies]
        draft["_type"] = "PYEHR_ACCESS_CONTROL_SETTINGS"

    def is_equal(self, other: 'PyehrAccessControlSettings'):
        return (type(self) == type(other) and
                is_equal_value(self.policies, other.policies) and
                is_equal_value(self.base_upon, other.base_upon) and
                is_equal_value(self.uid, other.uid))


class VersionedPyehrAccessControlSettings(VersionedObject[PyehrAccessControlSettings]):
    """VERSIONED_OBJECT of PYEHR_ACCESS_CONTROL_SETTINGS allowing for
    version controlled access settings to be configured."""
    pass