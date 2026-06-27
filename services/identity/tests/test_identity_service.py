from services.identity import IdentityService, generate_request_id, normalize_namespace


def test_generate_request_id_preserves_inbound_value():
    result = generate_request_id(" req-123 ")

    assert result.request_id == "req-123"
    assert result.generated is False


def test_generate_request_id_matches_legacy_hex_length():
    result = generate_request_id()

    assert result.generated is True
    assert len(result.request_id) == 16
    int(result.request_id, 16)


def test_normalize_namespace_is_lowercase_and_strict():
    assert normalize_namespace(" Entity-Registry ") == "entity-registry"


def test_identity_service_resolves_rid_and_alias():
    record = IdentityService.build_record(
        namespace="entity",
        key="entity-1",
        identity_type="device",
        aliases=("Kitchen Sensor", "kitchen_sensor"),
        canonical_label="Kitchen Sensor",
        confidence=0.9,
    )
    service = IdentityService((record,))

    by_rid = service.resolve("entity:entity-1")
    by_alias = service.resolve("KITCHEN SENSOR")

    assert by_rid.status == "ok"
    assert by_rid.canonical_rid == "entity:entity-1"
    assert by_alias.status == "ok"
    assert by_alias.canonical_rid == "entity:entity-1"


def test_identity_service_builds_from_truth_spine_entities():
    service = IdentityService.from_entities(
        (
            {
                "entity_id": "entity-1",
                "entity_type": "Person",
                "aliases": ("Trevor", "T"),
                "canonical_label": "Trevor",
                "confidence": 0.95,
            },
        )
    )

    result = service.resolve("trevor")

    assert result.status == "ok"
    assert result.record is not None
    assert result.record.identity_type == "person"
    assert result.record.canonical_label == "Trevor"


def test_merge_selects_higher_confidence_canonical_without_mutation():
    left = IdentityService.build_record(
        namespace="entity",
        key="a",
        identity_type="device",
        aliases=("alpha",),
        canonical_label="Alpha",
        confidence=0.7,
    )
    right = IdentityService.build_record(
        namespace="entity",
        key="b",
        identity_type="device",
        aliases=("beta",),
        canonical_label="Beta",
        confidence=0.9,
    )
    service = IdentityService((left, right))

    decision = service.merge("entity:a", "entity:b")

    assert decision.status == "ok"
    assert decision.canonical_rid == "entity:b"
    assert decision.absorbed_rid == "entity:a"
    assert "alpha" in decision.merged_aliases
    assert "entity:a" in decision.merged_aliases


def test_merge_rejects_type_conflict_with_structured_failure():
    person = IdentityService.build_record(
        namespace="entity",
        key="person-1",
        identity_type="person",
        aliases=(),
        canonical_label="Person",
        confidence=0.8,
    )
    device = IdentityService.build_record(
        namespace="entity",
        key="device-1",
        identity_type="device",
        aliases=(),
        canonical_label="Device",
        confidence=0.8,
    )
    service = IdentityService((person, device))

    decision = service.merge("entity:person-1", "entity:device-1")

    assert decision.status == "error"
    assert decision.failure is not None
    assert decision.failure.error_code == "IDENTITY_MERGE_TYPE_CONFLICT"
    assert decision.failure.recoverable is False


def test_health_reports_bounds():
    record = IdentityService.build_record(
        namespace="entity",
        key="entity-1",
        identity_type="device",
        aliases=("sensor",),
        canonical_label="Sensor",
        confidence=1.0,
    )
    service = IdentityService((record,), max_records=5, max_aliases_per_record=4)

    health = service.health()

    assert health.status == "ok"
    assert health.records == 1
    assert health.aliases == 1
    assert health.max_records == 5
    assert health.max_aliases_per_record == 4
