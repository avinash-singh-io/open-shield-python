import os

from open_shield.adapters.config import OpenShieldConfig


def test_config_loads_from_env() -> None:
    os.environ["OPEN_SHIELD_ISSUER_URL"] = "https://env.example.com"
    os.environ["OPEN_SHIELD_AUDIENCE"] = "env-api"
    os.environ["OPEN_SHIELD_REQUIRE_SCOPES"] = "false"

    config = OpenShieldConfig(ISSUER_URL="https://env.example.com", AUDIENCE="env-api")

    assert config.ISSUER_URL == "https://env.example.com"
    assert config.AUDIENCE == "env-api"
    assert config.REQUIRE_SCOPES is False

    # Cleanup
    del os.environ["OPEN_SHIELD_ISSUER_URL"]
    del os.environ["OPEN_SHIELD_AUDIENCE"]
    del os.environ["OPEN_SHIELD_REQUIRE_SCOPES"]


def test_config_defaults() -> None:
    os.environ["OPEN_SHIELD_ISSUER_URL"] = "https://default.example.com"
    # Ensure no other env vars interfere
    if "OPEN_SHIELD_REQUIRE_SCOPES" in os.environ:
        del os.environ["OPEN_SHIELD_REQUIRE_SCOPES"]

    config = OpenShieldConfig(ISSUER_URL="https://default.example.com")

    assert config.ISSUER_URL == "https://default.example.com"
    assert config.ALGORITHMS == ["RS256"]
    assert config.REQUIRE_SCOPES is True

    del os.environ["OPEN_SHIELD_ISSUER_URL"]
