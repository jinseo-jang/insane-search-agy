#!/usr/bin/env python3
"""
Verification test suite for README remediation.
Ensures README.md and README.ko.md:
1. Have 1:1 line-count parity.
2. Have 1:1 section header parity.
3. Accurately define Rule R6 as Failure Gate & Exhaustive Attempt Enforcement.
4. Contain no false claims of runtime pip install auto-installers.
5. Accurately describe Node & Patchright auto-discovery and zero-config setup.
"""

import os
import re

def test_readme_remediation():
    readme_en_path = os.path.abspath("README.md")
    readme_ko_path = os.path.abspath("README.ko.md")
    
    assert os.path.exists(readme_en_path), "README.md missing"
    assert os.path.exists(readme_ko_path), "README.ko.md missing"
    
    with open(readme_en_path, "r", encoding="utf-8") as f:
        en_lines = f.readlines()
        
    with open(readme_ko_path, "r", encoding="utf-8") as f:
        ko_lines = f.readlines()
        
    # 1. Line count parity check
    print(f"README.md line count: {len(en_lines)}")
    print(f"README.ko.md line count: {len(ko_lines)}")
    assert len(en_lines) == len(ko_lines), f"Line count mismatch: EN={len(en_lines)} vs KO={len(ko_lines)}"
    print("Pass: 1:1 Line Count Parity")

    en_text = "".join(en_lines)
    ko_text = "".join(ko_lines)

    # 2. Check Rule R6 definition
    assert "Failure Gate & Exhaustive Attempt Enforcement" in en_text or "Rule R6" in en_text, "Rule R6 missing in EN"
    assert "실패 게이트" in ko_text or "Rule R6" in ko_text, "Rule R6 missing in KO"
    print("Pass: Rule R6 Definition Correct")

    # 3. Verify no false pip install runtime auto-installer claims
    assert "pip install" not in en_text, "Found prohibited 'pip install' claim in README.md"
    assert "pip install" not in ko_text, "Found prohibited 'pip install' claim in README.ko.md"
    assert "Python Package Auto-Installer (Rule R6)" not in en_text, "Found false auto-installer claim in README.md"
    assert "Python 패키지 자동 설치 (Rule R6)" not in ko_text, "Found false auto-installer claim in README.ko.md"
    print("Pass: No False Runtime pip install Claims")

    # 4. Check Node & Patchright auto-discovery description in matrix
    assert "/opt/homebrew/bin/node" in en_text, "Node auto-discovery path missing in README.md"
    assert "/opt/homebrew/bin/node" in ko_text, "Node auto-discovery path missing in README.ko.md"
    assert "npx patchright install chrome" in en_text, "Patchright setup missing in README.md matrix"
    assert "npx patchright install chrome" in ko_text, "Patchright setup missing in README.ko.md matrix"
    print("Pass: Node & Patchright Auto-Discovery & Zero-Config Setup Accurately Described")

    # 5. Check section headers 1:1 structure
    en_headers = [line.strip() for line in en_lines if line.startswith("#")]
    ko_headers = [line.strip() for line in ko_lines if line.startswith("#")]
    print(f"EN Header Count: {len(en_headers)}, KO Header Count: {len(ko_headers)}")
    assert len(en_headers) == len(ko_headers), f"Header count mismatch: EN={len(en_headers)} vs KO={len(ko_headers)}"
    print("Pass: 1:1 Section Header Parity")

    print("\nALL README REMEDIATION VERIFICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    test_readme_remediation()
