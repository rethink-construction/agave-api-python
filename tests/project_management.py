import os
from typing import Callable
from pathlib import Path

from agave_api import AgaveClient

# Add the parent directory to the Python path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

SAVE_DIR = Path(__file__).parent / "data"


def save_json(data, filename):
    save_path = os.path.join(SAVE_DIR, filename)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "w") as f:
        json.dump(data, f, indent=2)


def test(
    agave_client: AgaveClient,
    test_name: str,
    test_func: Callable,
    check_func: Callable,
    additional_args: tuple = (),
):
    try:
        try:
            response = test_func(agave_client, *additional_args)
            save_json(response, f"{test_name}.json")
        except Exception as e:
            raise e
        if not check_func(response):
            raise Exception(f"Check failed for {test_name}")
        print(f"\033[92m{test_name} passed\033[0m")
        return response
    except Exception as e:
        raise Exception(f"\033[91m{test_name} failed: {e}\033[0m")


def test_projects(agave_client: AgaveClient):
    return test(
        agave_client,
        "projects",
        lambda client: client.project_management.projects(),
        lambda projects: isinstance(projects, dict) and "data" in projects,
    )


def test_project(agave_client: AgaveClient, project_id: str):
    return test(
        agave_client,
        f"project_{project_id}",
        lambda client: client.project_management.project(),
        lambda project: isinstance(project, dict) and "id" in project,
    )


def test_rfis(agave_client: AgaveClient):
    return test(
        agave_client,
        "rfis",
        lambda client: client.project_management.rfis(),
        lambda rfis: isinstance(rfis, dict) and "data" in rfis,
    )


def test_rfi(agave_client: AgaveClient, rfi_id: str):
    return test(
        agave_client,
        f"rfi_{rfi_id}",
        lambda client, rid: client.project_management.rfi(rid),
        lambda rfi: isinstance(rfi, dict) and "id" in rfi,
        (rfi_id,),
    )


def test_submittals(agave_client: AgaveClient):
    return test(
        agave_client,
        "submittals",
        lambda client: client.project_management.submittals(),
        lambda submittals: isinstance(submittals, dict) and "data" in submittals,
    )


def test_submittal(agave_client: AgaveClient, submittal_id: str):
    return test(
        agave_client,
        f"submittal_{submittal_id}",
        lambda client, sid: client.project_management.submittal(sid),
        lambda submittal: isinstance(submittal, dict) and "id" in submittal,
        (submittal_id,),
    )


def test_specifications(agave_client: AgaveClient):
    return test(
        agave_client,
        "specifications",
        lambda client: client.project_management.specifications(),
        lambda specifications: isinstance(specifications, dict)
        and "data" in specifications,
    )


def test_specification(agave_client: AgaveClient, specification_id: str):
    return test(
        agave_client,
        f"specification_{specification_id}",
        lambda client, sid: client.project_management.specification(sid),
        lambda specification: isinstance(specification, dict) and "id" in specification,
        (specification_id,),
    )


def test_contacts(agave_client: AgaveClient):
    return test(
        agave_client,
        "contacts",
        lambda client: client.project_management.contacts(),
        lambda contacts: isinstance(contacts, dict) and "data" in contacts,
    )


def test_contact(agave_client: AgaveClient, contact_id: str):
    return test(
        agave_client,
        f"contact_{contact_id}",
        lambda client, cid: client.project_management.contact(cid),
        lambda contact: isinstance(contact, dict) and "id" in contact,
        (contact_id,),
    )


def test_vendors(agave_client: AgaveClient):
    return test(
        agave_client,
        "vendors",
        lambda client: client.project_management.vendors(),
        lambda vendors: isinstance(vendors, dict) and "data" in vendors,
    )


def test_vendor(agave_client: AgaveClient, vendor_id: str):
    return test(
        agave_client,
        f"vendor_{vendor_id}",
        lambda client, vid: client.project_management.vendor(vid),
        lambda vendor: isinstance(vendor, dict) and "id" in vendor,
        (vendor_id,),
    )


def test_drawings(agave_client: AgaveClient):
    return test(
        agave_client,
        "drawings",
        lambda client: client.project_management.drawings(),
        lambda drawings: isinstance(drawings, dict) and "data" in drawings,
    )


def test_drawing(agave_client: AgaveClient, drawing_id: str):
    return test(
        agave_client,
        f"drawing_{drawing_id}",
        lambda client, did: client.project_management.drawing(did),
        lambda drawing: isinstance(drawing, dict) and "id" in drawing,
        (drawing_id,),
    )


def test_drawing_versions(agave_client: AgaveClient, drawing_id: str):
    return test(
        agave_client,
        f"drawing_versions_{drawing_id}",
        lambda client, did: client.project_management.drawing_versions(did),
        lambda drawing_versions: isinstance(drawing_versions, dict)
        and "data" in drawing_versions,
        (drawing_id,),
    )


def get_id_to_test(resource_name: str, multiple_response: dict):
    if not isinstance(multiple_response, dict):
        raise Exception(f"Expected a dictionary, got {type(multiple_response)}")
    if not isinstance(multiple_response.get("data", []), list):
        raise Exception(
            f"Expected a list, got {type(multiple_response.get('data', []))}"
        )
    test_id = multiple_response.get("data", [{}])[0].get("id", None)
    if not test_id:
        raise Exception(f"No {resource_name} id found")
    return test_id


def run_tests(agave_client: AgaveClient, project_id: str):
    projects_response = test_projects(agave_client)
    # Use consistent project id for all tests
    test_project(agave_client, project_id)

    # Test RFIs
    rfis_response = test_rfis(agave_client)
    test_rfi(agave_client, get_id_to_test("rfi", rfis_response))

    # Test Submittals
    submittals_response = test_submittals(agave_client)
    test_submittal(agave_client, get_id_to_test("submittal", submittals_response))

    # Test Specifications
    specifications_response = test_specifications(agave_client)
    test_specification(
        agave_client, get_id_to_test("specification", specifications_response)
    )

    # Test Contacts
    contacts_response = test_contacts(agave_client)
    test_contact(agave_client, get_id_to_test("contact", contacts_response))

    # Test Vendors
    vendors_response = test_vendors(agave_client)
    test_vendor(agave_client, get_id_to_test("vendor", vendors_response))

    # Test Drawings
    drawings_response = test_drawings(agave_client)
    drawing_id = get_id_to_test("drawing", drawings_response)
    test_drawing(agave_client, drawing_id)

    # Test Drawing Versions
    test_drawing_versions(agave_client, drawing_id)


if __name__ == "__main__":
    import os
    import json
    from dotenv import load_dotenv

    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    account_token = os.getenv("ACCOUNT_TOKEN")
    project_id = os.getenv("PROJECT_ID")

    agave_client = AgaveClient(client_id, client_secret, account_token, project_id)

    run_tests(agave_client, project_id)
