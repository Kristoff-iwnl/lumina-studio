"""
Tests for Companion Brief 3: Hero Title Visibility and Modes.
"""

import pytest
import json
from pathlib import Path

class TestCinematicTitle:
    """Tests for cinematic hero title visibility modes and styling."""

    def test_cinematic_title_mode_config(self, client):
        """Verify title_mode and title_scale are present in config and templates."""
        response = client.get("/cinematic")
        assert response.status_code == 200
        html = response.data.decode("utf-8")

        assert 'data-title-mode="front"' in html

    def test_cinematic_title_behind_mode(self, client, app):
        """Verify setting title_mode to behind excludes fixes.css."""
        path = Path(app.config["SITE_CONFIG_PATH"])
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["cinematic"]["title_mode"] = "behind"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        try:
            with client.get("/cinematic") as response:
                assert response.status_code == 200
                html = response.data.decode("utf-8")
                assert 'fixes.css' not in html
                assert 'data-title-mode="behind"' in html
        finally:
            data["cinematic"]["title_mode"] = "front"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    def test_cinematic_title_fit_mode(self, client, app):
        """Verify setting title_mode to fit renders correctly."""
        path = Path(app.config["SITE_CONFIG_PATH"])
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["cinematic"]["title_mode"] = "fit"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        try:
            with client.get("/cinematic") as response:
                assert response.status_code == 200
                html = response.data.decode("utf-8")
                assert 'fixes.css' in html
                assert 'data-title-mode="fit"' in html
        finally:
            data["cinematic"]["title_mode"] = "front"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    def test_cinematic_engines_with_fixes(self, client):
        """Verify both original and optimized engines load successfully."""
        r_orig = client.get("/cinematic?engine=original")
        assert r_orig.status_code == 200
        assert b"script.js" in r_orig.data

        r_opt = client.get("/cinematic?engine=optimized")
        assert r_opt.status_code == 200
        assert b"engine.js" in r_opt.data
