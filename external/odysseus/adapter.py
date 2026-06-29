"""Observation-safe Odysseus workspace adapter."""

from __future__ import annotations

from json import JSONDecodeError, dumps, loads
from types import MappingProxyType
from typing import Mapping
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from provenance import noncanonical_external_output

from .interfaces import (
    Failure,
    HttpResponse,
    MAX_PROMPT_CHARS,
    MAX_RESPONSE_CHARS,
    MAX_SESSION_ID_LENGTH,
    OdysseusConfig,
    OdysseusHealthStatus,
    OdysseusPromptRequest,
    OdysseusPromptResult,
    OdysseusTransport,
)


class HttpOdysseusTransport:
    """Standard-library HTTP transport with explicit timeout and byte caps."""

    def request_json(
        self,
        method: str,
        url: str,
        payload: Mapping[str, object] | None,
        timeout_seconds: float,
        max_response_bytes: int,
    ) -> HttpResponse:
        """Send one bounded JSON request.

        Inputs: method, absolute URL, optional JSON mapping, timeout seconds,
        response byte cap.
        Outputs: HttpResponse.
        Runtime: bounded by timeout_seconds. Memory: O(max_response_bytes).
        Failure: raises TimeoutError, OSError, ValueError, or URLError.
        Deterministic: depends on remote service.
        """

        body = None if payload is None else dumps(dict(payload), sort_keys=True).encode("utf-8")
        headers = {"Accept": "application/json"}
        if body is not None:
            headers["Content-Type"] = "application/json"
        request = Request(url=url, data=body, headers=headers, method=method.upper())
        try:
            with urlopen(request, timeout=timeout_seconds) as response:
                data = response.read(max_response_bytes + 1)
                if len(data) > max_response_bytes:
                    raise ValueError("response exceeds maximum size")
                return HttpResponse(
                    status_code=int(response.status),
                    body=data,
                    headers=MappingProxyType(dict(response.headers.items())),
                )
        except HTTPError as exc:
            data = exc.read(max_response_bytes + 1)
            if len(data) > max_response_bytes:
                raise ValueError("response exceeds maximum size") from exc
            return HttpResponse(status_code=int(exc.code), body=data, headers=MappingProxyType({}))
        except TimeoutError:
            raise
        except URLError as exc:
            if isinstance(exc.reason, TimeoutError):
                raise exc.reason from exc
            raise


class OdysseusWorkspaceAdapter:
    """Narrow adapter for optional Odysseus workspace interaction.

    Odysseus is treated as a replaceable UI/agent workspace. This adapter does
    not read or write canonical memory, inventory, bearings, ARK evidence, or
    Wayfinder constitutional state.
    """

    def __init__(self, config: OdysseusConfig, transport: OdysseusTransport | None = None) -> None:
        """Construct an adapter with explicit dependencies.

        Inputs: OdysseusConfig and optional transport.
        Outputs: adapter instance.
        Runtime: O(1). Memory: O(1).
        Failure: raises ValueError for invalid response caps.
        Deterministic: yes.
        """

        if config.max_response_bytes <= 0:
            raise ValueError("max_response_bytes must be positive")
        if config.max_prompt_chars <= 0:
            raise ValueError("max_prompt_chars must be positive")
        self._config = config
        self._transport = transport or HttpOdysseusTransport()

    def health(self) -> OdysseusHealthStatus:
        """Return adapter availability without mutating remote state.

        Inputs: adapter config. Outputs: OdysseusHealthStatus.
        Runtime: bounded by config.timeout_seconds. Memory:
        O(config.max_response_bytes).
        Failure: disabled, missing URL, timeout, HTTP error, or transport error.
        Deterministic: validation deterministic; network depends on transport.
        """

        if not self._config.enabled:
            return OdysseusHealthStatus(
                status="disabled",
                enabled=False,
                available=False,
                base_url=self._config.base_url,
                timeout_seconds=self._config.timeout_seconds,
            )
        if not self._config.base_url:
            return OdysseusHealthStatus(
                status="error",
                enabled=True,
                available=False,
                base_url="",
                timeout_seconds=self._config.timeout_seconds,
                failure=Failure.build("ODYSSEUS_BASE_URL_MISSING", "Odysseus base URL is not configured"),
            )
        try:
            response = self._transport.request_json(
                "GET",
                self._url(self._config.health_path),
                None,
                self._config.timeout_seconds,
                self._config.max_response_bytes,
            )
        except TimeoutError:
            return self._health_failure("ODYSSEUS_TIMEOUT", "Odysseus health check timed out")
        except (OSError, ValueError, URLError) as exc:
            return self._health_failure("ODYSSEUS_UNREACHABLE", str(exc))
        if 200 <= response.status_code < 300:
            return OdysseusHealthStatus(
                status="ok",
                enabled=True,
                available=True,
                base_url=self._config.base_url,
                timeout_seconds=self._config.timeout_seconds,
            )
        return self._health_failure(
            "ODYSSEUS_HEALTH_HTTP_ERROR",
            "Odysseus health check returned a non-success status",
            {"status_code": response.status_code},
        )

    def send_prompt(self, prompt_request: OdysseusPromptRequest) -> OdysseusPromptResult:
        """Send one prompt to Odysseus and return its response.

        Inputs: OdysseusPromptRequest.
        Outputs: OdysseusPromptResult.
        Runtime: bounded by config.timeout_seconds, max_prompt_chars, and
        max_response_bytes.
        Memory: O(max_prompt_chars + max_response_bytes).
        Failure: disabled adapter, invalid request, timeout, HTTP error,
        malformed JSON, missing response, or oversized response.
        Deterministic: validation deterministic; network depends on transport.
        """

        if not self._config.enabled:
            return OdysseusPromptResult(
                status="error",
                response=None,
                failure=Failure.build("ODYSSEUS_DISABLED", "Odysseus adapter is disabled"),
            )
        validation_failure = self._validate_prompt_request(prompt_request)
        if validation_failure is not None:
            return OdysseusPromptResult(status="error", response=None, failure=validation_failure)
        payload = {
            "message": prompt_request.prompt.strip(),
            "session": prompt_request.session_id.strip(),
            "use_web": False,
            "use_research": False,
        }
        try:
            response = self._transport.request_json(
                "POST",
                self._url(self._config.chat_path),
                payload,
                self._config.timeout_seconds,
                self._config.max_response_bytes,
            )
        except TimeoutError:
            return self._prompt_failure("ODYSSEUS_TIMEOUT", "Odysseus prompt call timed out")
        except (OSError, ValueError, URLError) as exc:
            return self._prompt_failure("ODYSSEUS_TRANSPORT_ERROR", str(exc))
        if response.status_code < 200 or response.status_code >= 300:
            return self._prompt_failure(
                "ODYSSEUS_HTTP_ERROR",
                "Odysseus prompt call returned a non-success status",
                {"status_code": response.status_code},
            )
        try:
            decoded = loads(response.body.decode("utf-8"))
        except (UnicodeDecodeError, JSONDecodeError) as exc:
            return self._prompt_failure("ODYSSEUS_RESPONSE_INVALID", str(exc))
        if not isinstance(decoded, Mapping):
            return self._prompt_failure("ODYSSEUS_RESPONSE_INVALID", "Odysseus response must be a JSON object")
        response_text = decoded.get("response")
        if not isinstance(response_text, str) or not response_text.strip():
            return self._prompt_failure("ODYSSEUS_RESPONSE_MISSING", "Odysseus response field is missing")
        if len(response_text) > MAX_RESPONSE_CHARS:
            return self._prompt_failure("ODYSSEUS_RESPONSE_TOO_LARGE", "Odysseus response text exceeds maximum length")
        provenance = None
        if prompt_request.include_provenance:
            request_id = prompt_request.request_id.strip() or f"odysseus:{prompt_request.session_id.strip()}"
            trace_id = prompt_request.trace_id.strip() or request_id
            provenance = noncanonical_external_output(
                source_system="odysseus",
                source_adapter="external.odysseus.workspace",
                source_session_id=prompt_request.session_id.strip(),
                request_id=request_id,
                timestamp=prompt_request.timestamp,
                trace_id=trace_id,
            )
        return OdysseusPromptResult(status="ok", response=response_text, provenance=provenance)

    def _validate_prompt_request(self, prompt_request: OdysseusPromptRequest) -> Failure | None:
        if not self._config.base_url:
            return Failure.build("ODYSSEUS_BASE_URL_MISSING", "Odysseus base URL is not configured")
        prompt = prompt_request.prompt.strip()
        if not prompt:
            return Failure.build("ODYSSEUS_PROMPT_INVALID", "prompt is required")
        if len(prompt) > min(self._config.max_prompt_chars, MAX_PROMPT_CHARS):
            return Failure.build("ODYSSEUS_PROMPT_TOO_LARGE", "prompt exceeds maximum length")
        session_id = prompt_request.session_id.strip()
        if not session_id:
            return Failure.build("ODYSSEUS_SESSION_INVALID", "session_id is required")
        if len(session_id) > MAX_SESSION_ID_LENGTH:
            return Failure.build("ODYSSEUS_SESSION_INVALID", "session_id exceeds maximum length")
        return None

    def _url(self, path: str) -> str:
        return f"{self._config.base_url}{path}"

    def _health_failure(
        self,
        error_code: str,
        reason: str,
        context: Mapping[str, object] | None = None,
    ) -> OdysseusHealthStatus:
        return OdysseusHealthStatus(
            status="error",
            enabled=self._config.enabled,
            available=False,
            base_url=self._config.base_url,
            timeout_seconds=self._config.timeout_seconds,
            failure=Failure.build(error_code, reason, context),
        )

    def _prompt_failure(
        self,
        error_code: str,
        reason: str,
        context: Mapping[str, object] | None = None,
    ) -> OdysseusPromptResult:
        return OdysseusPromptResult(
            status="error",
            response=None,
            failure=Failure.build(error_code, reason, context),
        )
