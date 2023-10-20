import logging
import fastapi_auth0
from typing import Optional, List
import pydantic

logger = logging.getLogger("fastapi_auth0")

# config for auth
from ..config import AUTH0_AUDIENCE, AUTH0_DOMAIN

READ_PROPERTY = "read:property"
READ_ENERGY = "read:energy"
READ_WEATHER = "read:weather"
CREATE_RPC = "create:rpc"
READ_USER = "read:user"
CREATE_USER = "create:user"
UPDATE_USER = "update:user"
DELETE_USER = "delete:user"


SCOPES = {
    READ_PROPERTY: "Access all property routes",
    READ_ENERGY: "Access all siteenergy routes",
    READ_WEATHER: "Access all weather routes",
    CREATE_RPC: "Use rpc routes to create a resource",
    READ_USER: "Read user",
    CREATE_USER: "Create user",
    UPDATE_USER: "Update user",
    DELETE_USER: "Delete user",
}


_Ids = List[int]


class OrgMeta(pydantic.BaseModel):
    agencies: Optional[_Ids]


class {{ cookiecutter.project_slug.capitalize() }}Auth0User(fastapi_auth0.Auth0User):
    org_metadata: Optional[OrgMeta] = None

    def get_agencies(self) -> Optional[_Ids]:
        if self.org_metadata and self.org_metadata.agencies:
            return self.org_metadata.agencies
        return None


# NOTE from 286 org_id is being evaluated on each user if available so setting this explicitly to None
auth0 = fastapi_auth0.Auth0(
    domain=AUTH0_DOMAIN,
    api_audience=AUTH0_AUDIENCE,
    org_id=None,
    scopes=SCOPES,
    user_model={{ cookiecutter.project_slug.capitalize() }}Auth0User,
)
