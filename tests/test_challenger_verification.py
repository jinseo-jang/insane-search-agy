#!/usr/bin/env python3
"""
Empirical test suite for challenger_1_m1.
Tests README installation commands, directory targets, copy integrity, and SKILL.md frontmatter/triggers.
"""

import os
import sys
import shutil
import subprocess
import yaml
import re

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    return res.returncode, res.stdout.strip(), res.stderr.strip()

def test_1_directory_creation():
    print("=== TEST 1: Directory Creation ===")
    global_target = os.path.expanduser("~/.gemini/config/skills")
    local_target = os.path.abspath(".agents/skills")
    
    cmd = f"mkdir -p {global_target} && mkdir -p {local_target}"
    code, out, err = run_cmd(cmd)
    
    pass_global = os.path.isdir(global_target)
    pass_local = os.path.isdir(local_target)
    
    print(f"Command: {cmd}")
    print(f"Exit code: {code}")
    print(f"Global target exists ({global_target}): {pass_global}")
    print(f"Local target exists ({local_target}): {pass_local}")
    
    assert code == 0, f"mkdir failed with error: {err}"
    assert pass_global, "Global skills directory does not exist"
    assert pass_local, "Local skills directory does not exist"
    print("Result: PASS\n")
    return {
        "command": cmd,
        "exit_code": code,
        "global_dir": global_target,
        "local_dir": local_target,
        "status": "PASS"
    }

def test_2_copy_commands():
    print("=== TEST 2: Copy Commands & Clean Copy Verification ===")
    src_dir = os.path.abspath("skills/insane-search")
    assert os.path.isdir(src_dir), f"Source directory {src_dir} missing"
    
    # Clean test isolated target to test fresh copy without prior file pollution
    test_clean_target = os.path.expanduser("~/.gemini/config/skills_clean_test_dir")
    if os.path.exists(test_clean_target):
        shutil.rmtree(test_clean_target)
    os.makedirs(test_clean_target, exist_ok=True)
    
    cmd_clean_copy = f"cp -r skills/insane-search {test_clean_target}/"
    code_clean, out_clean, err_clean = run_cmd(cmd_clean_copy)
    
    clean_dst = os.path.join(test_clean_target, "insane-search")
    
    # Also test standard README copy commands
    cmd_global_copy = "cp -r skills/insane-search ~/.gemini/config/skills/"
    code_global, out_global, err_global = run_cmd(cmd_global_copy)
    
    cmd_local_copy = "cp -r skills/insane-search .agents/skills/"
    code_local, out_local, err_local = run_cmd(cmd_local_copy)
    
    # Check diff on clean target vs source
    diff_code, diff_out, diff_err = run_cmd(f"diff -r {src_dir} {clean_dst}")
    
    # Check diff on local target vs source
    local_dst = os.path.abspath(".agents/skills/insane-search")
    diff_local_code, diff_local_out, diff_local_err = run_cmd(f"diff -r {src_dir} {local_dst}")
    
    print(f"Clean copy command: {cmd_clean_copy} -> Exit code {code_clean}")
    print(f"Clean copy diff result code: {diff_code} (0 means 100% identical)")
    print(f"Global copy command: {cmd_global_copy} -> Exit code {code_global}")
    print(f"Local copy command: {cmd_local_copy} -> Exit code {code_local}")
    print(f"Local copy diff result code: {diff_local_code}")
    
    # Cleanup clean test dir
    if os.path.exists(test_clean_target):
        shutil.rmtree(test_clean_target)
        
    assert code_clean == 0 and code_global == 0 and code_local == 0, "Copy command failed"
    assert diff_code == 0, f"Clean copy diff failed: {diff_out}"
    assert diff_local_code == 0, f"Local copy diff failed: {diff_local_out}"
    
    print("Result: PASS\n")
    return {
        "src_dir": src_dir,
        "global_copy_cmd": cmd_global_copy,
        "local_copy_cmd": cmd_local_copy,
        "clean_diff_exit_code": diff_code,
        "local_diff_exit_code": diff_local_code,
        "status": "PASS"
    }

def test_3_skill_md_frontmatter_and_triggers():
    print("=== TEST 3: SKILL.md Frontmatter & Slash Command / Trigger Verification ===")
    skill_path = os.path.abspath("skills/insane-search/SKILL.md")
    assert os.path.isfile(skill_path), f"SKILL.md file missing at {skill_path}"
    
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    assert content.startswith("---"), "SKILL.md does not start with YAML frontmatter delimiter '---'"
    parts = content.split("---", 2)
    assert len(parts) >= 3, "SKILL.md missing closing '---' for frontmatter"
    
    fm_raw = parts[1]
    fm = yaml.safe_load(fm_raw)
    
    skill_name = fm.get("name")
    skill_desc = fm.get("description", "")
    
    print(f"Parsed Skill Name: '{skill_name}'")
    assert skill_name == "insane-search", f"Expected skill name 'insane-search', got '{skill_name}'"
    
    # Verify slash command matching /insane-search in README files
    readme_en_path = os.path.abspath("README.md")
    readme_ko_path = os.path.abspath("README.ko.md")
    
    with open(readme_en_path, "r", encoding="utf-8") as f:
        readme_en = f.read()
        
    with open(readme_ko_path, "r", encoding="utf-8") as f:
        readme_ko = f.read()
        
    slash_cmd = f"/{skill_name}"
    assert slash_cmd in readme_en, f"Slash command {slash_cmd} not found in README.md"
    assert slash_cmd in readme_ko, f"Slash command {slash_cmd} not found in README.ko.md"
    print(f"Slash command '{slash_cmd}' verified in README.md and README.ko.md")
    
    # Parse triggers from README.md
    en_trig_match = re.search(r'\*\*Natural Prompt Triggers:\*\*\s*([^\n]+)', readme_en)
    assert en_trig_match, "Natural Prompt Triggers line not found in README.md"
    en_triggers = [t.strip('` ') for t in en_trig_match.group(1).split(',')]
    
    # Parse triggers from README.ko.md
    ko_trig_match = re.search(r'\*\*자연어 프롬프트 트리거:\*\*\s*([^\n]+)', readme_ko)
    assert ko_trig_match, "Natural prompt triggers line not found in README.ko.md"
    ko_triggers = [t.strip('` ') for t in ko_trig_match.group(1).split(',')]
    
    print(f"English Triggers ({len(en_triggers)}): {en_triggers}")
    print(f"Korean Triggers ({len(ko_triggers)}): {ko_triggers}")
    
    missing_en = [t for t in en_triggers if t not in skill_desc]
    missing_ko = [t for t in ko_triggers if t not in skill_desc]
    
    print(f"Missing EN triggers in SKILL.md: {missing_en}")
    print(f"Missing KO triggers in SKILL.md: {missing_ko}")
    
    assert len(missing_en) == 0, f"EN triggers missing in SKILL.md: {missing_en}"
    assert len(missing_ko) == 0, f"KO triggers missing in SKILL.md: {missing_ko}"
    
    print("Result: PASS\n")
    return {
        "skill_path": skill_path,
        "parsed_name": skill_name,
        "slash_command": slash_cmd,
        "en_triggers_count": len(en_triggers),
        "ko_triggers_count": len(ko_triggers),
        "missing_en": missing_en,
        "missing_ko": missing_ko,
        "status": "PASS"
    }

if __name__ == "__main__":
    r1 = test_1_directory_creation()
    r2 = test_2_copy_commands()
    r3 = test_3_skill_md_frontmatter_and_triggers()
    print("ALL TESTS PASSED SUCCESSFULLY!")
