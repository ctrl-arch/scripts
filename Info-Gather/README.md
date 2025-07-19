# Info Puller

This repository contains a collection of Python scripts that automate the retrieval of infrastructure-related data from cloud environments like Google Cloud Platform (GCP) and Kubernetes Engine (GKE).

### Folder Structure

- `gke/`
  - `iam/`: Pulls IAM RoleBindings and Roles across all namespaces in the selected GKE context.
  - `acls/`: (Planned) Will contain scripts to fetch and analyze ACLs or network policies in GKE clusters.
- `gcp/`: (Planned) Scripts that fetch resource usage, IAM policies, service account information, etc., directly from GCP.

---

### Typical Use Case

These scripts are useful for:
- Cloud Security Audits
- IAM and RBAC analysis
- Compliance checks
- Visualizing access permissions across clusters and services

> All scripts for GKE are designed to work through a local HTTPS tunnel proxy and retrieve live data from your environment.

---
