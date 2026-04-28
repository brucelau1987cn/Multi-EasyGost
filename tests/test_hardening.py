#!/usr/bin/env python3
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
script = (root / "gost.sh").read_text()
service = (root / "gost.service").read_text()

def test_repository_branch_urls_follow_default_v2():
    assert 'repo_branch="v2"' in script
    assert 'repo_raw_base="https://raw.githubusercontent.com/brucelau1987cn/Multi-EasyGost/${repo_branch}"' in script
    assert 'Multi-EasyGost/master' not in script
    assert '${repo_raw_base}/gost.sh' in script
    assert '${repo_raw_base}/gost.service' in script
    assert '${repo_raw_base}/config.json' in script


def test_install_restores_rawconf_once_and_downloads_required_files_safely():
    assert script.count('if [ -f /tmp/gost_rawconf_bak ]; then') == 1
    assert 'install -m 0644 gost.service /usr/lib/systemd/system/gost.service' in script
    assert 'install -m 0644 config.json /etc/gost/config.json' in script
    assert 'rm -rf "$(pwd)"/gost.sh' not in script


def test_cron_and_delete_inputs_are_validated():
    assert 'valid_hour_interval "$cronhr"' in script
    assert 'valid_hour_of_day "$cronhr"' in script
    assert 'valid_positive_integer "$numdelete"' in script
    assert 'sed -i "${numdelete}d" "$raw_conf_path"' in script


def test_config_generation_quotes_paths_and_handles_empty_rawconf():
    assert '[[ ! -s "$raw_conf_path" ]]' in script
    assert 'awk \'END{print NR}\' "$raw_conf_path"' in script
    assert 'sed -n "${i}p" "$raw_conf_path"' in script
    assert 'for ((i = 1; i <= count_line; i++)); do' in script


def test_ss2022_route_generation_is_consistent_for_multiple_rules():
    first_rule = 'ss2022://${ss2022_method}:${ss2022_psk_val}@:${s_port}?ipsk=${ss2022_ipsk_val}'
    assert script.count(first_rule) == 2
    assert '"ss2022://$d_ip:$s_port@:$d_port"' not in script


def test_systemd_service_runs_as_root_without_dynamic_user_and_has_safe_permissions():
    assert 'User=root' in service
    assert 'DynamicUser=true' not in service
    mode = (root / 'gost.service').stat().st_mode & 0o777
    assert mode == 0o644, oct(mode)

if __name__ == "__main__":
    tests = [v for k, v in globals().items() if k.startswith('test_')]
    for t in tests:
        t()
    print(f"{len(tests)} regression checks passed")
