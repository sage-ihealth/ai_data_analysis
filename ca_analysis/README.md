# CA Analysis

This folder contains analysis for Care Advocates (CAs) across 20 clinics.

## Files

### 1. find_ca_list.ipynb
Main notebook to find all CAs from the role_assignments collection.

**Query**:
```javascript
db.getCollection("role_assignments").find({
    'active': true,
    "roleType": "CA",
    "organizationId": ObjectId("xxx")
})
```

**Steps**:
1. Query all active CA role assignments for 20 organizations
2. Extract all unique member IDs
3. Get CA member details from members collection
4. Generate summary reports

**Outputs**:
- `ca_list_all.csv`: All CA assignments with full details
- `ca_unique_members.csv`: Unique CA members list
- `ca_by_organization.csv`: CAs grouped by organization
- `ca_member_ids.txt`: List of member ObjectIds for further queries

## Setup

Make sure your `.env` file has:
```
MONGO_DATABASE_URI=your_mongodb_connection_string
```

## Usage

1. Open `find_ca_list.ipynb`
2. Add your 20 organization IDs in cell 3
3. Run all cells
4. Check the output CSV files for results
