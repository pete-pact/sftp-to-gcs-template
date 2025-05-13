# SFTP to GCS Cloud Function Template

This repository contains a reusable Google Cloud Function integration that transfers the **latest file from an SFTP server to a Google Cloud Storage (GCS) bucket**. It's designed to be quickly replicated across customer implementations or internal projects.

---

## How to Use This Template

To create your own version of this integration:

### 1. Use the Template

1. Click the green "Use this template" button (top-right on GitHub).
2. Create a new repository in your GitHub account or organization.

This creates a fresh copy without linking back to the original (i.e. no forks).

---

## Configure Your Integration

Once you've created your copy:

### Files to Review and Update

| File Name                                     | Purpose                                                                   | 
|-----------------------------------------------|---------------------------------------------------------------------------|
| `main.py`                                     | Cloud Function logic (SFTP → GCS)                                         |
| `env_vars.json`                               | Environment variables (e.g. SFTP host, bucket name)                       |
| `requirements.txt`                            | Python dependencies                                                       |
| `.github/workflows/deploy.yml`                | GitHub Actions deployment script (must live in `.github/workflows`)       |
| `Technical_Guide_SFTP_to_GCS_Template.docx`   | Technical guide for the template                                          |

---

### Set Up GitHub Secrets

In your new GitHub repo, go to *Settings → Secrets → Actions* and add:

- `GCP_SA_KEY` — your GCP service account JSON key (for deploying the function)
- Ensure the secret name used for the SFTP password in Secret Manager matches what’s set in `deploy.yml` (e.g., `SFTP_PASSWORD_NAME`).

---

### Enable GCP Services

In your GCP project, make sure these APIs are enabled:

- Cloud Functions
- Cloud Build
- Secret Manager
- (Optional) Cloud Scheduler

Create the SFTP password secret:
