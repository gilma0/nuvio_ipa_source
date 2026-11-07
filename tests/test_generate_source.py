import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("generate_source", ROOT / "scripts/generate_source.py")
generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator)
CONFIG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
VERSION_PATTERN = CONFIG["apps"][0]["source"]["versionTagPattern"]


class SourceVersionsTest(unittest.TestCase):
    def test_nuvio_release_labels_match_ipa_version(self):
        for tag, expected in [
            ("0.6.9-beta", "0.6.9"),
            ("v0.6.9-beta.2", "0.6.9"),
            ("0.4.0-alpha", "0.4.0"),
            ("0.4.21", "0.4.21"),
        ]:
            with self.subTest(tag=tag):
                self.assertEqual(generator.version_from_tag(tag, VERSION_PATTERN), expected)

    def test_other_sources_preserve_prerelease_versions_by_default(self):
        self.assertEqual(generator.version_from_tag("v1.2.3-beta"), "1.2.3-beta")

    def test_unknown_tag_format_fails_instead_of_publishing_bad_version(self):
        with self.assertRaises(ValueError):
            generator.version_from_tag("nightly", VERSION_PATTERN)

    def test_fix_changes_install_version_without_changing_release_download(self):
        url = "https://github.com/NuvioMedia/NuvioMobile/releases/download/0.6.9-beta/nuvio-0.6.9-full-release.ipa"
        releases = [{
            "tag_name": "0.6.9-beta", "published_at": "2026-11-01T12:00:00Z",
            "assets": [{"name": "nuvio-0.6.9-full-release.ipa", "size": 69322992,
                        "browser_download_url": url}],
        }]
        with patch.object(generator, "gh_get", return_value=releases):
            app = generator.build_app(CONFIG["apps"][0])
        latest = app["versions"][0]
        self.assertEqual(latest["version"], "0.6.9")
        self.assertEqual(latest["downloadURL"], url)
        self.assertEqual(latest["size"], 69322992)

    def test_missing_ipa_cannot_erase_the_published_listing(self):
        with patch.object(generator, "gh_get", return_value=[]):
            with self.assertRaises(ValueError):
                generator.build_app(CONFIG["apps"][0])


if __name__ == "__main__":
    unittest.main()
