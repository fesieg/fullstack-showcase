from typing import Any

from fastapi.testclient import TestClient

from app.models.bottle import BottleType


def make_bottle(
    user_id: int = 1,
    type_: str = BottleType.PLASTIC,
    brand: str = "TestBrand",
    barcode: str = "1234567890",
) -> dict[str, Any]:
    return {
        "user_id": user_id,
        "type": type_,
        "brand": brand,
        "barcode": barcode,
    }


def test_create_bottle(client: TestClient, auth_headers: dict[str, str]) -> None:
    data = make_bottle()
    resp = client.post("/api/bottles/", json=data, headers=auth_headers)
    assert resp.status_code == 200
    out = resp.json()
    assert out["brand"] == data["brand"]
    assert out["type"] == data["type"]
    assert out["deposit_value"] == 0.25
    assert out["redeemed"] is False


def test_get_bottles(client: TestClient, auth_headers: dict[str, str]) -> None:
    data = make_bottle(barcode="bottle1")
    client.post("/api/bottles/", json=data, headers=auth_headers)
    resp = client.get("/api/bottles/1", headers=auth_headers)
    assert resp.status_code == 200
    bottles = resp.json()
    assert any(b["barcode"] == "bottle1" for b in bottles)


def test_get_unredeemed(client: TestClient, auth_headers: dict[str, str]) -> None:
    data = make_bottle(barcode="unredeemed1")
    client.post("/api/bottles/", json=data, headers=auth_headers)
    resp = client.get("/api/bottles/unredeemed/1", headers=auth_headers)
    assert resp.status_code == 200
    bottles = resp.json()
    assert any(b["barcode"] == "unredeemed1" and b["redeemed"] is False for b in bottles)


def test_get_balance(client: TestClient, auth_headers: dict[str, str]) -> None:
    client.post(
        "/api/bottles/", json=make_bottle(type_="plastic", barcode="bal1"), headers=auth_headers
    )
    client.post(
        "/api/bottles/", json=make_bottle(type_="glass", barcode="bal2"), headers=auth_headers
    )
    resp = client.get("/api/bottles/balance/1", headers=auth_headers)
    assert resp.status_code == 200
    balance = resp.json()
    assert balance == 0.75


def test_redeem_all(client: TestClient, auth_headers: dict[str, str]) -> None:
    client.post(
        "/api/bottles/", json=make_bottle(type_="plastic", barcode="redeem1"), headers=auth_headers
    )
    resp = client.post("/api/bottles/redeem/1", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() >= 0.25

    # after redeem, unredeemed should be empty
    resp2 = client.get("/api/bottles/unredeemed/1", headers=auth_headers)
    assert resp2.status_code == 200
    assert all(b["redeemed"] for b in resp2.json())


def test_validate_barcode(client: TestClient, auth_headers: dict[str, str]) -> None:
    # unique barcode
    resp = client.post("/api/bottles/validate_barcode/unique123", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json() is True

    # not unique after adding
    client.post("/api/bottles/", json=make_bottle(barcode="unique123"), headers=auth_headers)
    resp2 = client.post("/api/bottles/validate_barcode/unique123", headers=auth_headers)
    assert resp2.status_code == 200
    assert resp2.json() is False


def test_auth_required(client: TestClient) -> None:
    resp = client.get("/api/bottles/1")
    assert resp.status_code == 403
    resp2 = client.post("/api/bottles/", json=make_bottle())
    assert resp2.status_code == 403


def test_invalid_type(client: TestClient, auth_headers: dict[str, str]) -> None:
    data = make_bottle(type_="notatype", barcode="badtype")
    resp = client.post("/api/bottles/", json=data, headers=auth_headers)
    assert resp.status_code == 422
