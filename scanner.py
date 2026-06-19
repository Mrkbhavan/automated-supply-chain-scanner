import requests
import pandas as pd
import re
import json
import time


def get_real_time_osv_data(library_name, version, ecosystem):
    """Hits Google OSV API for 100% Genuine Real-Time Data"""
    url = "https://api.osv.dev/v1/query"
    payload = {"package": {"name": library_name, "ecosystem": ecosystem}}
    if version != 'latest': payload["version"] = version
        
    try:
        response = requests.post(url, json=payload, timeout=10).json()
        if 'vulns' in response:
            details = response['vulns'][0].get('details', '').lower()
            aliases = response['vulns'][0].get('aliases', []) 
            if any(x in details for x in ['rce', 'execute', 'remote', 'overflow', 'arbitrary']):
                return "❌ VULNERABLE", "CRITICAL", "🔴 REMOTE CODE EXECUTION", aliases
            elif any(x in details for x in ['leak', 'sql', 'auth', 'bypass', 'injection']):
                return "❌ VULNERABLE", "HIGH", "🟠 DATA LEAK / BYPASS", aliases
            else:
                return "❌ VULNERABLE", "MEDIUM", "🟡 SECURITY WEAKNESS", aliases
        else:
            return "✅ SAFE", "SAFE", "🟢 No Known Vulnerabilities", []
    except: return "⚠️ SCAN FAILED", "UNKNOWN", "API Error", []

def ultimate_beast_v4():
    print("=" * 75)
    print(" 🛡️ BEAST 4.0: DYNAMIC CATCHER & TRANSITIVE DEPENDENCY SCANNER ")
    print("=" * 75)
    
    repo_url = input("🔗 Enter Public GitHub Repo URL: ").strip()
    
    try:
        parts = repo_url.replace("https://github.com/", "").strip("/").split("/")
        user, repo = parts[0], parts[1]
    except:
        print("[!] URL Error!")
        return

    print(f"\n[*] Deep Scanning {user}/{repo}...")
    
    branch = "main"
    tree_url = f"https://api.github.com/repos/{user}/{repo}/git/trees/main?recursive=1"
    res = requests.get(tree_url).json()
    if 'message' in res and 'Not Found' in res['message']:
        branch = "master"
        tree_url = f"https://api.github.com/repos/{user}/{repo}/git/trees/master?recursive=1"
        res = requests.get(tree_url).json()

    if 'tree' not in res:
        print("[!] Access Denied or Empty Repo.")
        return

    ignore_exts = ('.png', '.jpg', '.mp4', '.mp3', '.exe', '.dll', '.zip', '.pdf', '.bin', '.ico', '.csv')
    targets = [f['path'] for f in res['tree'] if not f['path'].lower().endswith(ignore_exts)]
    
    print(f"[+] Ultra-Crawler Active: Inspecting {len(targets)} files (Including Lockfiles)...")

    extracted_libs = []
    
    for path in targets:
        raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{path}"
        try: content = requests.get(raw_url, timeout=5).text
        except: continue
            
        # --- 1. DYNAMIC & STANDARD SIGNATURES ---
        # Catches normal AND dynamic imports: importlib.import_module('pandas'), __import__('flask')
        dyn_matches = re.findall(r'(?:import_module|__import__)\s*\(\s*[\'"]([a-zA-Z0-9\-_]+)[\'"]', content)
        for lib in dyn_matches:
            if lib.lower() not in ['os', 'sys', 're', 'time']:
                extracted_libs.append((lib.lower(), 'latest', 'PyPI', path + ' (Dynamic)'))

        pip_matches = re.findall(r'(?:pip|pip3)\s+install\s+([a-zA-Z0-9\-_]+)(?:[>=<]+)?([0-9\.]+)?', content)
        for lib, ver in pip_matches:
            extracted_libs.append((lib.lower(), ver if ver else 'latest', 'PyPI', path))
            
        import_matches = re.findall(r'(?:^|\n)\s*(?:import|from)\s+([a-zA-Z0-9\-_]+)', content)
        for lib in import_matches:
            if lib.lower() not in ['os', 'sys', 're', 'time', 'math', 'json', 'random', 'datetime', 'string', 'warnings']:
                extracted_libs.append((lib.lower(), 'latest', 'PyPI', path))

        # --- 2. DEEP TRANSITIVE RESOLVER (Lockfiles) ---
        if 'package-lock.json' in path:
            try:
                lock_data = json.loads(content)
                # Extracts deeply nested sub-libraries in Node.js
                deps = lock_data.get('dependencies', {})
                for dep_name, dep_info in deps.items():
                    extracted_libs.append((dep_name, dep_info.get('version', 'latest'), 'npm', path + ' (Sub-Library)'))
            except: pass
            
        elif 'Pipfile.lock' in path:
            try:
                lock_data = json.loads(content)
                # Extracts exact versions of Python sub-libraries
                deps = lock_data.get('default', {})
                for dep_name, dep_info in deps.items():
                    ver = dep_info.get('version', '').strip('=')
                    extracted_libs.append((dep_name, ver if ver else 'latest', 'PyPI', path + ' (Sub-Library)'))
            except: pass

    unique_libs = list(set(extracted_libs))
    if not unique_libs:
        print("\n[!] No external libraries detected.")
        return

    print(f"\n[+] Extraction Complete! Found {len(unique_libs)} libraries (including Sub-Libraries). Hitting OSV API...")

    all_findings = []
    for name, ver, eco, path in unique_libs:
        status, severity, risk, aliases = get_real_time_osv_data(name, ver, eco)
        cve_number = ", ".join([a for a in aliases if a.startswith('CVE') or a.startswith('GHSA')][:2]) if aliases else "None"

        all_findings.append({
            "Source": path,
            "Library Name": name,
            "Version": ver,
            "Ecosystem": eco,
            "Security Status": status,
            "Severity": severity,
            "Threat Impact": risk,
            "Bug ID": cve_number
        })
        time.sleep(0.1)

    if all_findings:
        df = pd.DataFrame(all_findings)
        sev_map = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, 'UNKNOWN': 4, 'SAFE': 5}
        df['sort'] = df['Severity'].map(sev_map)
        df = df.sort_values('sort').drop('sort', axis=1)

        total_libs = len(df)
        vuln_libs = len(df[df['Security Status'] == '❌ VULNERABLE'])
        safe_libs = total_libs - vuln_libs
        report_name = f"Beast_v4_Audit_{repo}.html"
        
        style = """<style>
            body { font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; padding: 20px; color: #333;}
            .header { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: white; padding: 25px; text-align: center; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
            .dashboard { display: flex; gap: 20px; margin-top: 20px; }
            .card { background: white; padding: 20px; border-radius: 10px; flex: 1; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
            table { width: 100%; border-collapse: collapse; margin-top: 25px; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); font-size: 14px;}
            th { background: #1e293b; color: white; padding: 12px; text-align: left; }
            td { padding: 10px; border-bottom: 1px solid #e2e8f0; }
            .VULN { color: #dc2626; font-weight: bold; }
            .STATUS-SAFE { color: #16a34a; font-weight: bold; }
            .badge-crit { background: #dc2626; color:white; padding: 3px 8px; border-radius: 12px; font-weight:bold;}
            .badge-safe { background: #16a34a; color:white; padding: 3px 8px; border-radius: 12px; font-weight:bold;}
        </style>"""

        html_content = f"""
        <html><head>{style}</head><body>
        <div class='header'>
            <h1 style="margin:0;">🛡️ Advanced Supply Chain & Transitive Dependency Scanner</h1>
            <p>Target: <b>{user}/{repo}</b> | Scanner: Deep Content + Sub-Library Resolver</p>
        </div>
        <div class='dashboard'>
            <div class='card' style='border-bottom: 4px solid #475569;'><h2>{total_libs}</h2><p>Total Libs & Sub-Libs</p></div>
            <div class='card' style='border-bottom: 4px solid #16a34a;'><h2>{safe_libs}</h2><p>✅ Safe & Verified</p></div>
            <div class='card' style='border-bottom: 4px solid #dc2626;'><h2>{vuln_libs}</h2><p>❌ Vulnerable Found</p></div>
        </div>
        """
        
        raw_html = df.to_html(index=False, escape=False)
        raw_html = raw_html.replace('❌ VULNERABLE', '<span class="VULN">❌ VULNERABLE</span>')
        raw_html = raw_html.replace('✅ SAFE', '<span class="STATUS-SAFE">✅ SAFE</span>')
        raw_html = raw_html.replace('CRITICAL', '<span class="badge-crit">CRITICAL</span>')
        raw_html = raw_html.replace('<td>SAFE</td>', '<td><span class="badge-safe">SAFE</span></td>')

        html_content += raw_html + "</body></html>"
        with open(report_name, "w", encoding="utf-8") as f: f.write(html_content)

        print(f"\n[+] SCAN COMPLETE! Download your deep audit report.")
        

ultimate_beast_v4()
