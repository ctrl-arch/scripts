# GKE IAM RoleBindings & Roles Extractor

This script connects to your active GKE cluster context via `kubectl`, extracts all RoleBindings and their associated Roles across every namespace, and generates a flattened CSV file for auditing access and permissions.

---

### What It Does

- Uses your **current** Kubernetes context (`kubectl config current-context`)
- Iterates over all namespaces
- Pulls:
  - `RoleBindings` and their subjects
  - Matching `Roles` and their `rules` (apiGroups, resources, verbs)
- Outputs a consolidated CSV report with each rule mapped clearly

---

### How It Works

1. You manually open a local tunnel to your cluster.
2. The script uses `HTTPS_PROXY` (default: `http://localhost:8889`) to route kubectl calls.
3. Retrieves RoleBindings and Roles.
4. Flattens and merges data for export.

---

### Prerequisites

- Python 3.8+
- `kubectl` installed and configured
- Local tunnel open (`kubectl proxy`, or company-specific port-forward setup)
- Proxy port (e.g. 8889) configured in the script

---

### Running the Script

```bash
python gke_iam_pull.py
```

---

### Output

A CSV file will be generated with a name like:

```
gke_iam_data_my-cluster-context_2025-07-18.csv
```

#### Output CSV Fields

| Column             | Description                                                     |
|--------------------|-----------------------------------------------------------------|
| Namespace          | Kubernetes namespace name                                       |
| RoleBinding Name   | Name of the RoleBinding                                         |
| Role Name          | Linked Role’s name                                              |
| Role Kind          | Usually Role or ClusterRole                                     |
| Subjects Kind      | Comma-separated list of subject types (User, ServiceAccount, etc.) |
| Subjects Name      | Comma-separated list of subject names                           |
| API Groups         | Comma-separated list of API groups granted access               |
| Resources          | Comma-separated list of Kubernetes resources                    |
| Verbs              | Allowed operations (e.g., get, list, update)                    |
| Creation Timestamp | When the RoleBinding was created                                |
