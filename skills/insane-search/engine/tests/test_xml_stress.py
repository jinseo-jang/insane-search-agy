#!/usr/bin/env python3
"""Stress test harness for XML validator logic in engine/validators.py.

Verifies handling of BOM, whitespace, malformed XML, case-sensitivity,
alternative declarations, and XML entity expansion attacks.
"""
from __future__ import annotations

import os
import sys
import time
import unittest

# Allow running from anywhere.
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, ROOT)

from engine.validators import validate, Verdict, ValidationResult  # noqa: E402


class MockResponse:
    def __init__(self, text: str, status_code: int = 200, content_type: str = "text/xml", cookies: dict = None):
        self.text = text
        self.status_code = status_code
        self.headers = {"content-type": content_type}
        self.cookies = cookies or {}
        # Simulate .content attribute if present in curl_cffi/requests
        self.content = text.encode("utf-8", "ignore")


class TestXMLValidatorStress(unittest.TestCase):

    def test_bom_with_leading_whitespace(self):
        # Case A: Normal BOM
        body_a = "\ufeff<?xml version=\"1.0\"?><root><tag>hello</tag></root>"
        res_a = validate(MockResponse(body_a))
        self.assertEqual(res_a.verdict, Verdict.WEAK_OK, f"BOM only failed: reasons={res_a.reasons}")

        # Case B: BOM followed by whitespace
        body_b = "\ufeff  \n  <?xml version=\"1.0\"?><root><tag>hello</tag></root>"
        res_b = validate(MockResponse(body_b))
        # Note: If this fails, verdict might fall through to HTML and become CHALLENGE because it's too short (tiny_body)
        self.assertEqual(res_b.verdict, Verdict.WEAK_OK, f"BOM followed by whitespace failed: verdict={res_b.verdict}, reasons={res_b.reasons}")

        # Case C: Whitespace followed by BOM
        body_c = "  \n  \ufeff  <?xml version=\"1.0\"?><root><tag>hello</tag></root>"
        res_c = validate(MockResponse(body_c))
        self.assertEqual(res_c.verdict, Verdict.WEAK_OK, f"Whitespace followed by BOM failed: verdict={res_c.verdict}, reasons={res_c.reasons}")

    def test_malformed_xml_fallthrough(self):
        # XML that is malformed but has generic Content-Type or xml Content-Type and exceeds 3000 bytes
        malformed_body = "<root><child>unclosed" + ("x" * 4000)
        
        # Test with XML Content-Type: should NOT be WEAK_OK if malformed
        res_xml = validate(MockResponse(malformed_body, content_type="text/xml"))
        self.assertNotEqual(res_xml.verdict, Verdict.WEAK_OK, 
                            f"Malformed XML with text/xml was accepted as WEAK_OK: reasons={res_xml.reasons}")

        # Test with no Content-Type: if it doesn't look like XML or fails, it might fall through.
        # But wait! If it starts with `<root>` and doesn't have `<?xml`, `_looks_like_xml` won't match (unless Content-Type is XML).
        # What if it starts with `<?xml` but is malformed?
        malformed_body_with_decl = '<?xml version="1.0"?><root><child>unclosed' + ("x" * 4000)
        res_xml_decl = validate(MockResponse(malformed_body_with_decl, content_type="text/plain"))
        self.assertNotEqual(res_xml_decl.verdict, Verdict.WEAK_OK,
                            f"Malformed XML with decl was accepted as WEAK_OK: reasons={res_xml_decl.reasons}")

    def test_alternative_declarations(self):
        # Case A: Uppercase <?XML
        body_upper = '<?XML version="1.0"?><root><tag>hello</tag></root>'
        res_upper = validate(MockResponse(body_upper, content_type="text/plain"))
        self.assertEqual(res_upper.verdict, Verdict.WEAK_OK, 
                         f"Uppercase XML declaration failed: verdict={res_upper.verdict}, reasons={res_upper.reasons}")

        # Case B: Comment prefix before RSS root
        body_comment = '<!-- feed generator --><rss version="2.0"><channel><title>Test</title></channel></rss>'
        res_comment = validate(MockResponse(body_comment, content_type="text/plain"))
        self.assertEqual(res_comment.verdict, Verdict.WEAK_OK,
                         f"Comment prefixed RSS failed: verdict={res_comment.verdict}, reasons={res_comment.reasons}")

    def test_billion_laughs_entity_expansion(self):
        # Standard Billion Laughs payload
        payload = """<?xml version="1.0"?>
<!DOCTYPE lolz [
 <!ENTITY lol "lol">
 <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
 <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
 <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
 <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
 <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
 <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
]>
<lolz>&lol6;</lolz>"""
        
        t0 = time.time()
        res = validate(MockResponse(payload))
        duration = time.time() - t0
        
        print(f"Billion Laughs parse time: {duration:.4f}s, verdict={res.verdict}, reasons={res.reasons}")
        
        # If it parsed it and expanded successfully, lol6 is 1,000,000 "lol"s, which takes a few milliseconds,
        # but if we used lol9 (1,000,000,000 "lol"s), it would crash or freeze.
        # Let's make sure it doesn't take too long (e.g. timeout threshold of 2 seconds for lol6).
        self.assertLess(duration, 2.0, "Entity expansion took too long, possible DoS vulnerability!")

    def test_extremely_large_xml(self):
        # Generate a large XML body (approx 5MB)
        large_body = '<?xml version="1.0"?><root>' + ('<child>data</child>' * 250000) + '</root>'
        t0 = time.time()
        res = validate(MockResponse(large_body))
        duration = time.time() - t0
        print(f"5MB XML parse time: {duration:.4f}s, verdict={res.verdict}, reasons={res.reasons}")
        self.assertEqual(res.verdict, Verdict.WEAK_OK)
        self.assertLess(duration, 3.0, "Large XML parsing took too long")

    def test_empty_xml(self):
        # Empty root
        body_empty = "<root></root>"
        res_empty = validate(MockResponse(body_empty))
        self.assertEqual(res_empty.verdict, Verdict.WEAK_OK)
        self.assertIn("xml_ok", res_empty.reasons)

        # Non-empty root
        body_ok = "<root><child/></root>"
        res_ok = validate(MockResponse(body_ok))
        self.assertEqual(res_ok.verdict, Verdict.WEAK_OK)


if __name__ == "__main__":
    unittest.main()
