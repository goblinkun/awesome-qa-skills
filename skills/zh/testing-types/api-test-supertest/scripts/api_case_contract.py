"""Check a normalized request before generating executable smoke assertions.

This module is copied into each API tool Skill; no repository dependency is used.
Complex schema, file, and parameter resolution stays explicitly incomplete.
"""
import json
import math
import re

METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}


def contract_errors(method, path, endpoint):
    errors = []
    if method.upper() not in METHODS:
        errors.append("unsupported HTTP method")
    if not isinstance(path, str) or not path.startswith("/") or "\n" in path or "\r" in path:
        errors.append("a relative resource path is required")
    elif re.search(r"\{[^}]+\}|\$\{|:[A-Za-z_]", path):
        errors.append("resolve path/query variables")
    statuses = endpoint.get("expected_statuses")
    if not isinstance(statuses, list) or not statuses or any(type(s) is not int or not 100 <= s <= 599 for s in statuses):
        errors.append("supply explicit expected_statuses")
    if endpoint.get("body_required") and "body" not in endpoint:
        errors.append("supply the required request body")
    if any(value for key,value in endpoint.items() if key.startswith('unresolved_')) or endpoint.get("review_required"):
        errors.append("resolve unsupported source fields")
    if endpoint.get("parameters"):
        errors.append("resolve declared parameters into the path/body")
    if endpoint.get("response_schema"):
        errors.append("implement and review response_schema assertions")
    elif any(media.get('schema') for response in endpoint.get('response_contracts',{}).values() for media in response.get('content',{}).values()):
        errors.append("implement schema assertions for all declared success responses")
    if "body" in endpoint and endpoint.get("body_encoding", "json") not in {"json", "raw"}:
        errors.append("unsupported body encoding")
    if endpoint.get("body_encoding") == "raw" and not isinstance(endpoint.get("body"), str):
        errors.append("raw body must be text")
    headers = endpoint.get("headers", {})
    if not isinstance(headers, dict) or any(not isinstance(k, str) or not isinstance(v, str) or any(c in k+v for c in '\r\n') for k,v in headers.items()):
        errors.append("headers must be single-line string pairs")
    else:
        if any(k.lower() in {"authorization", "cookie", "x-api-key", "proxy-authorization"} for k in headers):
            errors.append("move credential headers to headers_env")
        if any(re.search(r"\{\{.*?\}\}|\$\{", v) for v in headers.values()):
            errors.append("resolve header variables")
    env = endpoint.get("headers_env", {})
    if not isinstance(env, dict) or any(not isinstance(k,str) or not isinstance(v,str) or not re.fullmatch(r"[A-Z][A-Z0-9_]*",v) or any(c in k for c in '\r\n') for k,v in env.items()):
        errors.append("headers_env must map header names to environment variable names")
    if re.search(r"\{\{.*?\}\}|\$\{", json.dumps(endpoint.get("body", ""))):
        errors.append("resolve body variables")
    limit = endpoint.get("max_response_ms")
    if limit is not None and (type(limit) not in {int, float} or not math.isfinite(limit) or limit <= 0):
        errors.append("max_response_ms must be a supplied positive finite number")
    return errors


def endpoints_from(payload):
    endpoints = payload.get("endpoints") if isinstance(payload, dict) else None
    if not isinstance(endpoints, list) or not endpoints:
        raise ValueError("No endpoints: provide a nonempty endpoint collection")
    if any(not isinstance(ep, dict) for ep in endpoints):
        raise ValueError("Each endpoint must be an object")
    return endpoints


def incomplete_message(errors):
    return "Incomplete contract: " + "; ".join(errors)


def fail_incomplete(endpoints):
    count = sum(bool(contract_errors(str(ep.get('method', '')), str(ep.get('path', '')), ep)) for ep in endpoints)
    if count:
        raise SystemExit(f"Generated {count} incomplete scaffold(s); review the contract before running requests.")
