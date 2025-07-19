import subprocess
import json
import pandas as pd
from datetime import datetime
import logging
import os

# Setup logging to provide detailed execution logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Set the HTTPS proxy to your local tunnel (e.g., 8889)
HTTPS_PROXY = "http://localhost:8889"

def run_command(cmd):
    """Runs a shell command using the HTTPS proxy and returns parsed JSON output or None on failure."""
    proxy_cmd = f"HTTPS_PROXY={HTTPS_PROXY} {cmd}"
    try:
        result = subprocess.run(proxy_cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout)
        else:
            logging.error(f"Command failed: {cmd}\n{result.stderr.strip()}")
            return None
    except Exception as e:
        logging.error(f"Exception running command: {cmd}\n{e}")
        return None

def get_current_context():
    """Fetches the current kubectl context in use."""
    proxy_cmd = f"HTTPS_PROXY={HTTPS_PROXY} kubectl config current-context"
    result = subprocess.run(proxy_cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0 and result.stdout:
        return result.stdout.strip()
    logging.error(f"Error fetching current context: {result.stderr.strip()}")
    return None

def get_namespaces(context):
    """Retrieves all namespaces from the given Kubernetes context."""
    cmd = f"kubectl --context {context} get namespaces -o json"
    data = run_command(cmd)
    return [ns['metadata']['name'] for ns in data.get('items', [])] if data else []

def get_rolebindings(context, namespace):
    """Retrieves all RoleBindings in a specific namespace."""
    cmd = f"kubectl --context {context} get rolebindings -n {namespace} -o json"
    return run_command(cmd)

def get_roles(context, namespace):
    """Retrieves all Roles in a specific namespace."""
    cmd = f"kubectl --context {context} get roles -n {namespace} -o json"
    return run_command(cmd)

def parse_iam_data(rolebindings_data, roles_data, namespace):
    """Matches RoleBindings to their corresponding Roles and prepares flattened output records."""
    records = []
    role_map = {role['metadata']['name']: role for role in roles_data.get('items', [])} if roles_data else {}

    for rb in rolebindings_data.get('items', []):
        rb_name = rb['metadata']['name']
        role_ref = rb['roleRef']
        subjects = rb.get('subjects', [])
        creation_timestamp = rb['metadata'].get('creationTimestamp', 'N/A')

        role_name = role_ref.get('name', 'N/A')
        role_details = role_map.get(role_name, {})
        rules = role_details.get('rules', [])

        # If there are no rules defined, still add the entry
        if not rules:
            records.append({
                "Namespace": namespace,
                "RoleBinding Name": rb_name,
                "Role Name": role_name,
                "Role Kind": role_ref.get('kind', 'N/A'),
                "Subjects Kind": ', '.join(s.get('kind', 'N/A') for s in subjects),
                "Subjects Name": ', '.join(s.get('name', 'N/A') for s in subjects),
                "API Groups": "N/A",
                "Resources": "N/A",
                "Verbs": "N/A",
                "Creation Timestamp": creation_timestamp,
            })
        else:
            # Flatten each rule from the role and append
            for rule in rules:
                records.append({
                    "Namespace": namespace,
                    "RoleBinding Name": rb_name,
                    "Role Name": role_name,
                    "Role Kind": role_ref.get('kind', 'N/A'),
                    "Subjects Kind": ', '.join(s.get('kind', 'N/A') for s in subjects),
                    "Subjects Name": ', '.join(s.get('name', 'N/A') for s in subjects),
                    "API Groups": ', '.join(rule.get('apiGroups', [])),
                    "Resources": ', '.join(rule.get('resources', [])),
                    "Verbs": ', '.join(rule.get('verbs', [])),
                    "Creation Timestamp": creation_timestamp,
                })
    return records

def main():
    """Main execution function that orchestrates the audit and generates the CSV output."""
    context = get_current_context()
    if not context:
        logging.error("Failed to retrieve current context. Exiting.")
        return

    logging.info(f"Using context: {context}")

    namespaces = get_namespaces(context)
    if not namespaces:
        logging.warning("No namespaces found.")
        return

    all_records = []

    for ns in namespaces:
        logging.info(f"Processing namespace: {ns}")
        rolebindings_data = get_rolebindings(context, ns)
        roles_data = get_roles(context, ns)

        if not rolebindings_data:
            logging.warning(f"No role bindings in namespace: {ns}")
        if not roles_data:
            logging.warning(f"No roles in namespace: {ns}")

        if rolebindings_data:
            all_records.extend(parse_iam_data(rolebindings_data, roles_data, ns))

    # Save results to CSV if any records found
    if all_records:
        df = pd.DataFrame(all_records)
        today = datetime.now().strftime("%Y-%m-%d")
        safe_context = context.replace("/", "_").replace(":", "_")
        filename = f"gke_iam_data_{safe_context}_{today}.csv"
        df.to_csv(filename, index=False)
        logging.info(f"IAM roles and bindings exported to {filename}")
    else:
        logging.warning("No data to export. CSV not created.")

# Entry point for script
if __name__ == "__main__":
    main()
