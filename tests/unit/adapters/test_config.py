import os
import pytest
from open_shield.adapters.config import OpenShieldConfig


def test_config_loads_from_env():
    os.environ["OPEN_SHIELD_ISSUER_URL"] = "https://env.example.com"
    os.environ["OPEN_SHIELD_AUDIENCE"] = "env-api"
    os.environ["OPEN_SHIELD_REQUIRE_SCOPES"] = "false"
    
    config = OpenShieldConfig()
    
    assert config.ISSUER_URL == "https://env.example.com"
    assert config.AUDIENCE == "env-api"
    assert config.REQUIRE_SCOPES is False
    
    # Cleanup
    del os.environ["OPEN_SHIELD_ISSUER_URL"]
    del os.environ["OPEN_SHIELD_AUDIENCE"]
    del os.environ["OPEN_SHIELD_REQUIRE_SCOPES"]


def test_config_defaults():
    os.environ["OPEN_SHIELD_ISSUER_URL"] = "https://default.example.com"
    # Ensure no other env vars interfere
    if "OPEN_SHIELD_REQUIRE_SCOPES" in os.environ:
        del os.environ["OPEN_SHIELD_REQUIRE_SCOPES"]
        
    config = OpenShieldConfig()
    
    assert config.ISSUER_URL == "https://default.example.com"
    assert config.ALGORITHMS == ["RS256"]
    assert config.REQUIRE_SCOPES is True
    
    del os.environ["OPEN_SHIELD_ISSUER_URL"]
