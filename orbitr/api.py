from __future__ import annotations

from typing import Any, Dict, NoReturn

from flask import Blueprint, current_app, jsonify, request

from .catalog import load_catalog
from .storage import RsoStore

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health", methods=["GET"])
def health() -> Any:
    store = _get_store()
    return jsonify({"status": "ok", "rso_count": len(store.list_all())})


@api_bp.route("/rso", methods=["GET", "POST"])
def rso_collection() -> Any:
    store = _get_store()
    if request.method == "GET":
        return jsonify(store.list_all())

    payload = _require_json()
    cleaned, errors = _validate_payload(payload, partial=False)
    if errors:
        return _bad_request("Validation failed.", errors)

    try:
        created = store.create(cleaned)
    except ValueError as exc:
        return _bad_request(str(exc))

    response = jsonify(created)
    response.status_code = 201
    return response


@api_bp.route("/rso/<satcat_number>", methods=["GET", "PUT", "PATCH", "DELETE"])
def rso_item(satcat_number: str) -> Any:
    store = _get_store()
    record = store.get(satcat_number)

    if request.method == "GET":
        if not record:
            return _not_found(satcat_number)
        return jsonify(record)

    if request.method == "DELETE":
        if not record:
            return _not_found(satcat_number)
        try:
            store.delete(satcat_number)
        except KeyError:
            return _not_found(satcat_number)
        return ("", 204)

    payload = _require_json()

    if request.method == "PUT":
        cleaned, errors = _validate_payload(payload, partial=False)
        if errors:
            return _bad_request("Validation failed.", errors)
        if cleaned["satcat_number"] != str(satcat_number):
            return _bad_request("SatCat number in body must match the URL segment.")
        try:
            updated = store.replace(satcat_number, cleaned)
        except KeyError:
            return _not_found(satcat_number)
        return jsonify(updated)

    # PATCH
    cleaned, errors = _validate_payload(payload, partial=True)
    if errors:
        return _bad_request("Validation failed.", errors)

    if "satcat_number" in cleaned and cleaned["satcat_number"] != str(satcat_number):
        return _bad_request("SatCat number cannot be reassigned.")

    if not record:
        return _not_found(satcat_number)

    merged = {**record, **cleaned}
    merged["aliases"] = cleaned.get("aliases", record.get("aliases", []))
    merged["tags"] = cleaned.get("tags", record.get("tags", []))

    try:
        updated = store.replace(satcat_number, merged)
    except KeyError:
        return _not_found(satcat_number)
    return jsonify(updated)


@api_bp.route("/rso/almanac/catalog", methods=["GET"])
def rso_catalog() -> Any:
    return jsonify(load_catalog())


def _require_json() -> Dict[str, Any]:
    payload = request.get_json(silent=True)
    if payload is None:
        raise _json_error("A JSON body is required for this request.")
    if not isinstance(payload, dict):
        raise _json_error("JSON payload must be an object.")
    return payload


def _validate_payload(
    payload: Dict[str, Any], *, partial: bool
) -> tuple[Dict[str, Any], Dict[str, str]]:
    required_fields = [
        "display_name",
        "satcat_number",
        "international_designator",
        "tle",
        "aliases",
        "tags",
    ]
    cleaned: Dict[str, Any] = {}
    errors: Dict[str, str] = {}

    for field in required_fields:
        if field not in payload:
            if not partial:
                errors[field] = "Field is required."
            continue

        value = payload[field]
        if field in {"display_name", "satcat_number", "international_designator", "tle"}:
            if not isinstance(value, (str, int)):
                errors[field] = "Value must be a string."
                continue
            cleaned_value = str(value).strip()
            if not cleaned_value:
                errors[field] = "Value cannot be empty."
                continue
            cleaned[field] = cleaned_value
            continue

        if not isinstance(value, list):
            errors[field] = "Value must be an array of strings."
            continue

        normalized = []
        for item in value:
            if not isinstance(item, str):
                errors[field] = "Every entry must be a string."
                normalized = []
                break
            stripped = item.strip()
            if stripped:
                normalized.append(stripped)
        if errors.get(field):
            continue
        cleaned[field] = sorted(set(normalized), key=str.casefold)

    if partial:
        return cleaned, errors

    missing = [field for field in required_fields if field not in cleaned]
    if missing:
        for field in missing:
            errors.setdefault(field, "Field is required.")

    return cleaned, errors


def _json_error(message: str) -> NoReturn:
    response = jsonify({"error": message})
    response.status_code = 400
    raise _FlaskAbort(response)


class _FlaskAbort(Exception):
    """Helper to bubble up JSON validation failures."""

    def __init__(self, response):
        super().__init__()
        self.response = response


@api_bp.errorhandler(_FlaskAbort)
def _handle_abort(exc: _FlaskAbort):
    return exc.response


def _bad_request(message: str, field_errors: Dict[str, str] | None = None):
    response = jsonify({"error": message, "fields": field_errors or {}})
    response.status_code = 400
    return response


def _not_found(satcat: str):
    response = jsonify({"error": f"RSO with SatCat {satcat} was not found."})
    response.status_code = 404
    return response


def _get_store() -> RsoStore:
    store = current_app.config.get("RSO_STORE")
    if store is None:
        raise RuntimeError("RSO store has not been configured.")
    return store
