# Deploy a Linebot on GCP (Cloud Function)

## Init
1. Set env vars :
    - LINE_CHANNEL_SECRET
    - LINE_CHANNEL_ACCESS_TOKEN
2. Deploy codes, and don't forget to set "callback" as the entry.
3. Go to the permitions tab.
4. Add a new permition with "allUsers" as Role, "Cloud Functions Invoker" as policy.
