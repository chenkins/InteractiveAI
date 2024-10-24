from datetime import datetime

import pytest
from api.models import UseCaseModel, db
from api.utils import load_usecases_db
from app import create_app
from settings import logger

PUBLISHER_TEST_BEARER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJSbXFOVTNLN0x4ck5SRmtIVTJxcTZZcTEya1RDaXNtRkw5U2NwbkNPeDBjIn0.eyJleHAiOjE2OTk5Nzk0NTEsImlhdCI6MTY5OTM3NDY1MSwianRpIjoiMjg5YTg5MDUtOTQ0YS00MGIwLWJkYTYtNzU5ODkzZWVmODFmIiwiaXNzIjoiaHR0cDovLzE5Mi4xNjguMjExLjk1OjMyMDAvYXV0aC9yZWFsbXMvZGV2IiwiYXVkIjoiYWNjb3VudCIsInN1YiI6InB1Ymxpc2hlcl90ZXN0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoib3BmYWItY2xpZW50Iiwic2Vzc2lvbl9zdGF0ZSI6ImI1ZjUwZTc0LTYwOWEtNGI5MC1iMDhkLTFjNDQwM2MyMGMzYSIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoiZW1haWwgcHJvZmlsZSIsInNpZCI6ImI1ZjUwZTc0LTYwOWEtNGI5MC1iMDhkLTFjNDQwM2MyMGMzYSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZ3JvdXBzIjoiRGlzcGF0Y2hlcjtSZWFkT25seTtTdXBlcnZpc29yIiwicHJlZmVycmVkX3VzZXJuYW1lIjoicHVibGlzaGVyX3Rlc3QiLCJnaXZlbl9uYW1lIjoiIiwiZmFtaWx5X25hbWUiOiIifQ.RddLBhlhPMZst7TIRe10goMEZCriUchF9qNLBG889dnRP_YRh_bc-63cPeDbPG-YmeiXiQGJ3CJ9xGvc7uQl7iKLtCrBtTqn0A1IKOWmCrfaQ_czTyNKz5mrlU9HmzpO6H534Wjrx4uylwwhXrjuO7c06wZvn03tpNrBdoIVvCQqyInfY_QDoOttXU6-dj8S6aZavAsPDSNSrfzgiP33VT5Y0atoiHZ4gNvIeRAFIl6VrbAAQ7YkVDwzHAMPcA4QC4_k6t_m9t8KJ5otdzicDS6QJLV9hKUGzFPKJN60FSmscE9Gs7Uud_EGT-9GA_i53-1Pzxq6EWr-BkQ28kQDFQ"


@pytest.fixture(scope="function")
def app():
    app = create_app("test")
    with app.app_context():
        # Create the database tables
        db.create_all()

        yield app

        use_case_factory = app.use_case_factory
        try:
            orange_factory = use_case_factory.get_context_manager("ORANGE")
            orange_factory.correaltion_manager.correlation_request_process.terminate()
        except Exception as e:
            logger.info(f"Ignore this error {e}")

        # Clean up the database after the test
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.fixture
def rte_auth_mocker(client, mocker):
    # Mock the keycloak.introspect method to return a valid response
    mocker.patch(
        "cab_common_auth.decorators.keycloak.introspect",
        return_value={
            "exp": 1684333261,
            "iat": 1683728461,
            "jti": "716b02d4-29ba-41bd-85b2-8004cec1a033",
            "iss": "http://192.168.211.95:3200/realms/dev",
            "aud": "account",
            "sub": "rte_user",
            "typ": "Bearer",
            "azp": "opfab-client",
            "session_state": "8976b125-39a8-4bdf-b523-7e0dcbcdd3b4",
            "given_name": "",
            "family_name": "",
            "preferred_username": "rte_user",
            "email_verified": False,
            "acr": "1",
            "realm_access": {"roles": ["offline_access", "uma_authorization"]},
            "resource_access": {
                "account": {
                    "roles": [
                        "manage-account",
                        "manage-account-links",
                        "view-profile",
                    ]
                }
            },
            "scope": "email profile",
            "sid": "8976b125-39a8-4bdf-b523-7e0dcbcdd3b4",
            "groups": "Dispatcher;ReadOnly;Supervisor",
            "entitiesId": "RTE",
            "client_id": "opfab-client",
            "username": "rte_user",
            "active": True,
        },
    )


@pytest.fixture
def da_auth_mocker(client, mocker):
    # Mock the keycloak.introspect method to return a valid response
    mocker.patch(
        "cab_common_auth.decorators.keycloak.introspect",
        return_value={
            "exp": 1684401219,
            "iat": 1683796419,
            "jti": "a28734f6-f5c8-4130-8fb7-573d75c39d8c",
            "iss": "http://192.168.211.95:3200/realms/dev",
            "aud": "account",
            "sub": "da_user",
            "typ": "Bearer",
            "azp": "opfab-client",
            "session_state": "bd3b8610-1d05-4bdd-916b-61dcfe6d5e72",
            "preferred_username": "da_user",
            "email_verified": False,
            "acr": "1",
            "realm_access": {"roles": ["offline_access", "uma_authorization"]},
            "resource_access": {
                "account": {
                    "roles": [
                        "manage-account",
                        "manage-account-links",
                        "view-profile",
                    ]
                }
            },
            "scope": "email profile",
            "sid": "bd3b8610-1d05-4bdd-916b-61dcfe6d5e72",
            "groups": "RTE;ADMIN;ReadOnly",
            "entitiesId": "DA",
            "client_id": "opfab-client",
            "username": "da_user",
            "active": True,
        },
    )


@pytest.fixture
def sncf_auth_mocker(client, mocker):
    # Mock the keycloak.introspect method to return a valid response
    mocker.patch(
        "cab_common_auth.decorators.keycloak.introspect",
        return_value={
            "exp": 1684413915,
            "iat": 1683809115,
            "jti": "6f63636a-625a-4926-9684-6d5ed3b80e2a",
            "iss": "http://192.168.211.95:3200/realms/dev",
            "aud": "account",
            "sub": "sncf_user",
            "typ": "Bearer",
            "azp": "opfab-client",
            "session_state": "0dee604d-5c03-416c-8d95-59b0aa95b61a",
            "preferred_username": "sncf_user",
            "email_verified": False,
            "acr": "1",
            "realm_access": {"roles": ["offline_access", "uma_authorization"]},
            "resource_access": {
                "account": {
                    "roles": [
                        "manage-account",
                        "manage-account-links",
                        "view-profile",
                    ]
                }
            },
            "scope": "email profile",
            "sid": "0dee604d-5c03-416c-8d95-59b0aa95b61a",
            "entitiesId": "SNCF",
            "client_id": "opfab-client",
            "username": "sncf_user",
            "active": True,
        },
    )


@pytest.fixture
def orange_auth_mocker(client, mocker):
    # Mock the keycloak.introspect method to return a valid response
    mocker.patch(
        "cab_common_auth.decorators.keycloak.introspect",
        return_value={
            "exp": 1684766859,
            "iat": 1684162059,
            "jti": "418dee2b-aac6-452e-a90f-32278e34a22b",
            "iss": "http://192.168.211.95:3200/realms/dev",
            "aud": "account",
            "sub": "orange_user",
            "typ": "Bearer",
            "azp": "opfab-client",
            "session_state": "5297805d-fc73-4d94-97fc-0c5a52c41440",
            "preferred_username": "orange_user",
            "email_verified": False,
            "acr": "1",
            "realm_access": {"roles": ["offline_access", "uma_authorization"]},
            "resource_access": {
                "account": {
                    "roles": [
                        "manage-account",
                        "manage-account-links",
                        "view-profile",
                    ]
                }
            },
            "scope": "email profile",
            "sid": "5297805d-fc73-4d94-97fc-0c5a52c41440",
            "groups": "RTE;ADMIN;ReadOnly",
            "entitiesId": "ORANGE",
            "client_id": "opfab-client",
            "username": "orange_user",
            "active": True,
        },
    )


@pytest.fixture
def publisher_test_auth_mocker(client, mocker):
    # Mock the keycloak.introspect method to return a valid response
    mocker.patch(
        "cab_common_auth.decorators.keycloak.introspect",
        return_value={
            "exp": 1699979608,
            "iat": 1699374808,
            "jti": "5e2dae33-5158-4667-b831-8a87f91656b0",
            "iss": "http://192.168.211.95:3200/auth/realms/dev",
            "aud": "account",
            "sub": "publisher_test",
            "typ": "Bearer",
            "azp": "opfab-client",
            "session_state": "c8f122de-77aa-46e5-8e0f-37516e0f2933",
            "given_name": "",
            "family_name": "",
            "preferred_username": "publisher_test",
            "email_verified": False,
            "acr": "1",
            "realm_access": {"roles": ["offline_access", "uma_authorization"]},
            "resource_access": {
                "account": {
                    "roles": [
                        "manage-account",
                        "manage-account-links",
                        "view-profile",
                    ]
                }
            },
            "scope": "email profile",
            "sid": "c8f122de-77aa-46e5-8e0f-37516e0f2933",
            "groups": "Dispatcher;ReadOnly;Supervisor",
            "entitiesId": "SNCF;ORANGE;DA;RTE",
            "client_id": "opfab-client",
            "username": "publisher_test",
            "active": True,
        },
    )


@pytest.fixture(scope="function")
def create_contexts(client, publisher_test_auth_mocker):
    with client.application.app_context():
        # save context to db
        headers = {"Authorization": f"Bearer {PUBLISHER_TEST_BEARER_TOKEN}"}
        context_data = {
            "date": "2022-11-07T16:06:00.741655",
            "data": {"observation": {"rho": 11}, "topology": "iii"},
            "use_case": "RTE",
        }

        client.post("/api/v1/contexts", headers=headers, json=context_data)

        context_data = {
            "date": "2022-12-01T16:08:29.060050",
            "data": {
                "trains": [
                    {
                        "id_train": "12345",
                        "nb_passengers_onboard": 200,
                        "nb_passengers_connection": 13,
                        "latitude": "45.8574215",
                        "longitude": "4.4819996",
                        "speed": 300,
                        "failure": False,
                    }
                ]
            },
            "use_case": "SNCF",
        }

        client.post("/api/v1/contexts", headers=headers, json=context_data)


@pytest.fixture(scope="function")
def create_usecases(client):
    with client.application.app_context():
        from flask import current_app

        db.create_all()

        da_use_case = UseCaseModel(
            name="DA",
            context_manager_class="DAContextManager",
            metadata_schema_class="MetadataSchemaDA",
        )

        orange_use_case = UseCaseModel(
            name="ORANGE",
            context_manager_class="OrangeContextManager",
            metadata_schema_class="MetadataSchemaOrange",
        )
        rte_use_case = UseCaseModel(
            name="RTE",
            context_manager_class="RTEContextManager",
            metadata_schema_class="MetadataSchemaRTE",
        )
        sncf_use_case = UseCaseModel(
            name="SNCF",
            context_manager_class="SNCFContextManager",
            metadata_schema_class="MetadataSchemaSNCF",
        )

        db.session.add(da_use_case)
        db.session.add(orange_use_case)
        db.session.add(rte_use_case)
        db.session.add(sncf_use_case)
        db.session.commit()
        # add use_case_factory
        use_case_factory = current_app.use_case_factory

        # Load use cases from the database
        load_usecases_db(use_case_factory)
