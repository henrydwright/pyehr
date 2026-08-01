

from logging import Logger, getLogger

from pyehr.core.base.base_types.identification import HierObjectID
from pyehr.core.rm.common.generic import PartyIdentified, PartyProxy
from pyehr.core.rm.demographic import Actor
from pyehr.server.database import IDatabaseEngine
from pyehr.server.security.access_control import PyehrAccessPolicyEndpoint
from pyehr.server.security.auth import IPyehrAuthProvider

__all__ = ['AllowAllAuthProvider']


class AllowAllAuthProvider(IPyehrAuthProvider):
    """Auth provider which allows all actions for any role, executing
    all actions as a single party pre-configured at startup and accepting
    any provided header's audit detail information."""

    executing_as: PartyIdentified
    """The identification of the party as which all commands authorised
    by this provider will be run."""

    _executing_as_actor: Actor
    """The actor that this provider is executing as"""

    _log: Logger
    _db: IDatabaseEngine

    def __init__(self, execute_as: PartyIdentified, db: IDatabaseEngine):
        """Initialise the provider.
        
        :param execute_as: This is the PARTY_IDENTIFIED that will be returned
                           and used whenever an identity is needed for audit
                           purposes. The external_ref MUST resolve to an ACTOR
                           in the demographic service."""
        if execute_as.external_ref is None:
            raise ValueError("Provided party must have external_ref to ACTOR in demographic service")
        self.executing_as = execute_as
        self.accept_header_committer = True
        self._log = getLogger("auth.allowall")
        self._db = db
        super().__init__()

    def setup(self):
        actor_id = HierObjectID(self.executing_as.external_ref.id.value)
        actor_type = self.executing_as.external_ref.ref_type
        self._log.info(f"Loading {actor_type} at {actor_id.value}")
        self._executing_as_actor = self._db.retrieve_uid_object(actor_type, actor_id, self.executing_as.external_ref)

    def authenticated_actor(self) -> tuple[PartyProxy, Actor]:
        return (self.executing_as, self._executing_as_actor)

    def action_authorised(self, actor, policy, actions, endpoint, archetype_id = None):
        self._log.debug(f"PERMIT:actor={actor.uid.value if actor.uid is not None else ""}:policy={policy.uid.value if policy is not None and policy.uid is not None else ""}:actions={str([action.value for action in actions])}:endpoint={endpoint.value}:arch_id={archetype_id if archetype_id is not None else "*"}")
        return True
    
    def action_authorised_for_authenticated_actor(self, policy, actions, endpoint, archetype_id = None):
        return self.action_authorised(self.authenticated_actor()[1], policy, actions, endpoint, archetype_id)