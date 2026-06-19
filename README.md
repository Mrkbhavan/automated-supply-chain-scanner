*# 🛡️ Automated Supply Chain Security Scanner

An advanced, zero-configuration **Software Composition Analysis (SCA)** tool. It performs deep signature-based content inspection to detect known vulnerabilities in external dependencies, transitive sub-libraries, and dynamically injected imports across any public GitHub repository.
**Signature-Based Deep Content Scanning:** Escapes the limits of file extensions. It reads the actual code logic to find hidden dependencies across any text-based file.

Powered by real-time intelligence from the **Google OSV (Open Source Vulnerability) API**.

## 🚀 True Capabilities (What it ACTUALLY does)

* **Signature-Based Deep Content Scanning:** Does not rely on mere file extensions. It reads the raw code across all text-based files to catch `import`, `require`, and `pip install` statements hidden anywhere in the project.

* **Transitive Dependency Resolver:** Goes beyond surface-level libraries. It parses lockfiles (`package-lock.json`, `Pipfile.lock`) to extract deeply nested sub-libraries that traditional scanners often miss.

* **Dynamic Import Catcher:** Employs smart regex to detect obfuscated or dynamically loaded modules like `importlib.import_module()`.

* **Zero-Touch Execution:** No GitHub personal access tokens (PAT) required. Uses direct raw content extraction to bypass standard API rate limits and authentication hurdles.

* **100% Real-Time Data:** Direct integration with Google OSV provides the absolute latest threat intel, including official **CVE & GHSA** identification numbers.

* **Enterprise Dashboard Reporting:** Automatically generates a styled HTML report featuring a metric dashboard (Total Scanned, Safe, Vulnerable) and severity-sorted results with CVE/GHSA bug tracking..

## 🛠️ Tech Stack & Requirements
* **Language:** Python 3.x
* **Core Libraries:** `requests` (for OSV/GitHub communication), `pandas` (for HTML data structuring).
* *(Built with standard native modules like `re`, `json`, and `time` for minimal footprint).*

## ⚙️ How to Run Locally

1. **Clone the repo:**
   
   git clone https://github.com/Mrkbhavan/Automated-Supply-Chain-Scanner.git
   cd Automated-Supply-Chain-Scanner
  
2. **Install dependencies:**
    
   pip install -r requirements.txt


3. **Execute the scanner**
    
   python scanner.py

   
   
