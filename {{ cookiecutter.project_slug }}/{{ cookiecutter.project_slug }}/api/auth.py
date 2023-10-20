import logging
import fastapi_auth0


logger = logging.getLogger("fastapi_auth0")

# config for auth
from ..config import AUTH0_AUDIENCE, AUTH0_DOMAIN

SCOPES = {}


class {{ cookiecutter.project_slug.capitalize() }}Auth0User(fastapi_auth0.Auth0User):
    ...


class {{ cookiecutter.project_slug.capitalize() }}Auth0(fastapi_auth0.Auth0): 
    ...

auth0 = {{ cookiecutter.project_slug.capitalize() }}Auth0(
    domain=AUTH0_DOMAIN,
    api_audience=AUTH0_AUDIENCE,
    org_id=None,
    scopes=SCOPES,
    user_model={{ cookiecutter.project_slug.capitalize() }}Auth0User,
)
