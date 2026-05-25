
from abc import ABC, abstractmethod
from typing import Optional

from pyehr.core.rm.common.generic import PartyIdentified, PartyProxy
from pyehr.core.rm.demographic import Actor, Party
from pyehr.server.security.access_control import PyehrAccessControlSettings, PyehrAccessPolicyEndpoint, PyehrAccessPolicyEndpointAction


class IPyehrAuthProvider(ABC):

    accept_header_committer: bool
    """Whether or not this provider allows the 'committer' in the request
    header to be used to fill AUDIT_DETAILS"""

    def __init__(self):
        self.accept_header_committer = True
        super().__init__()
    
    @abstractmethod
    def setup(self) -> None:
        """Perform initial setup of the auth provider at start up
        of the server"""
        pass

    @abstractmethod
    def authenticated_actor(self) -> tuple[PartyProxy, Actor]:
        """Return the identity of the currently authenticated actor
        in the context of the current request.
        
        The ACTOR returned must also be referenced in the external_ref
        of the PARTY_PROXY returned.
        
        The ACTOR must reference all ROLEs it has that are relevant to
        access control within ACTOR.roles"""
        pass

    @abstractmethod
    def action_authorised(
            self,
            actor: Actor,
            policy: PyehrAccessControlSettings, 
            actions: set[PyehrAccessPolicyEndpointAction],
            endpoint: PyehrAccessPolicyEndpoint,  
            archetype_id: Optional[str] = None) -> bool:
        """Return whether a given `actor` is permitted under the
        `policy` (PYEHR_ACCESS_CONTROL SETTINGS) applying to this EHR or demographic object 
        to carry out a desired set of `actions` on an `endpoint` for objects modelled with
        `archetype_id` (in body or response)."""
        pass

    @abstractmethod
    def action_authorised_for_authenticated_actor(
            self,
            policy: PyehrAccessControlSettings, 
            actions: set[PyehrAccessPolicyEndpointAction],
            endpoint: PyehrAccessPolicyEndpoint,  
            archetype_id: Optional[str] = None
    ):
        """Return whether the currently authenticated `actor` is permitted under the
        `policy` (PYEHR_ACCESS_CONTROL SETTINGS) applying to this EHR or demographic object 
        to carry out a desired set of `actions` on an `endpoint` for objects modelled with
        `archetype_id` (in body or response)."""
        pass
