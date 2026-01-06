# -*- coding: utf-8 -*-
"""
Script to complete the noshow.ipynb notebook with comprehensive analysis code.
This script will add all the necessary cells for analyzing no-show patterns from MongoDB.
Filters data for September 1, 2025 to October 31, 2025.
"""

import json
from datetime import datetime

# Read the existing notebook
notebook_path = "/Users/sagegu/Documents/multi-agent/ai_data_analysis/noshow/noshow.ipynb"

with open(notebook_path, 'r') as f:
    notebook = json.load(f)

# Remove the empty cell at the end
notebook['cells'] = notebook['cells'][:-1]

# Add new cells for the analysis

# Cell 1: Explore clinic_events collection
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# First, let's explore the clinic_events collection structure\n",
        "print(\"📊 Exploring clinic_events collection...\\n\")\n",
        "\n",
        "# Get total count\n",
        "total_count = clinic_events_collection.count_documents({})\n",
        "print(f\"Total clinic events in collection: {total_count:,}\\n\")\n",
        "\n",
        "# Get a sample document to understand the schema\n",
        "sample_doc = clinic_events_collection.find_one()\n",
        "if sample_doc:\n",
        "    print(\"Sample document fields:\")\n",
        "    for key in sample_doc.keys():\n",
        "        print(f\"  - {key}: {type(sample_doc[key]).__name__}\")\n",
        "    print(\"\\n\" + \"=\"*80 + \"\\n\")\n",
        "    print(\"Sample document:\")\n",
        "    import json\n",
        "    print(json.dumps(sample_doc, indent=2, default=str))"
    ]
})

# Cell 2: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 2: Query Clinic Events for Sept 1 - Oct 31, 2025"
    ]
})

# Cell 3: Query with date filter
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Query clinic events from MongoDB for the specified date range\n",
        "from datetime import datetime\n",
        "\n",
        "print(\"📥 Fetching clinic events from Sept 1 - Oct 31, 2025...\\n\")\n",
        "\n",
        "# Define date range\n",
        "start_date = datetime(2025, 9, 1)\n",
        "end_date = datetime(2025, 10, 31, 23, 59, 59)\n",
        "\n",
        "print(f\"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\\n\")\n",
        "\n",
        "# First, let's check what date field exists in the collection\n",
        "# Common field names: 'date', 'created_at', 'scheduled_date', 'appointment_date', etc.\n",
        "sample = clinic_events_collection.find_one()\n",
        "date_fields = [k for k in sample.keys() if 'date' in k.lower() or 'time' in k.lower() or 'created' in k.lower()]\n",
        "print(f\"Found potential date fields: {date_fields}\\n\")\n",
        "\n",
        "# Display the values of these date fields from the sample\n",
        "for field in date_fields:\n",
        "    print(f\"{field}: {sample.get(field)} (type: {type(sample.get(field)).__name__})\")"
    ]
})

# Cell 4: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 3: Filter Data by Date Range\n",
        "\n",
        "**Note:** Adjust the `date_field_name` below based on the actual field name from Step 2."
    ]
})

# Cell 5: Filter by date
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Based on the date fields found above, specify the correct field name\n",
        "# Common options: 'scheduled_date', 'appointment_date', 'created_at', 'date', etc.\n",
        "# ADJUST THIS BASED ON STEP 2 OUTPUT:\n",
        "date_field_name = 'scheduled_date'  # ⚠️ UPDATE THIS IF NEEDED\n",
        "\n",
        "# Query with date filter\n",
        "query = {\n",
        "    date_field_name: {\n",
        "        '$gte': start_date,\n",
        "        '$lte': end_date\n",
        "    }\n",
        "}\n",
        "\n",
        "print(f\"Querying with field: {date_field_name}\\n\")\n",
        "\n",
        "# Fetch filtered documents\n",
        "filtered_events = list(clinic_events_collection.find(query))\n",
        "\n",
        "# Convert to DataFrame\n",
        "df_events = pd.DataFrame(filtered_events)\n",
        "\n",
        "print(f\"✅ Loaded {len(df_events):,} clinic events for Sept-Oct 2025\\n\")\n",
        "print(f\"DataFrame shape: {df_events.shape}\\n\")\n",
        "print(\"Columns:\")\n",
        "print(df_events.columns.tolist())"
    ]
})

# Cell 6: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 4: Preview the Data"
    ]
})

# Cell 7: Preview data
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Display first few rows\n",
        "print(\"First 5 rows of the data:\\n\")\n",
        "df_events.head()"
    ]
})

# Cell 8: Data info
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Basic data exploration\n",
        "print(\"📊 Data Information\\n\")\n",
        "print(\"=\" * 80)\n",
        "\n",
        "# Display basic info\n",
        "df_events.info()\n",
        "\n",
        "print(\"\\n\" + \"=\" * 80)\n",
        "print(\"\\nBasic Statistics:\")\n",
        "df_events.describe(include='all')"
    ]
})

# Cell 9: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 5: Identify Status/Attendance Fields"
    ]
})

# Cell 10: Check for status fields
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Check for status or attendance-related fields\n",
        "print(\"🔍 Looking for status/attendance fields...\\n\")\n",
        "\n",
        "# Common field names that might indicate status\n",
        "status_fields = [col for col in df_events.columns if any(keyword in col.lower() \n",
        "                 for keyword in ['status', 'attend', 'show', 'cancel', 'complete'])]\n",
        "\n",
        "if status_fields:\n",
        "    print(f\"Found potential status fields: {status_fields}\\n\")\n",
        "    for field in status_fields:\n",
        "        print(f\"\\n{'='*80}\")\n",
        "        print(f\"{field} - Unique values:\")\n",
        "        print(df_events[field].value_counts())\n",
        "        print(f\"\\nNull count: {df_events[field].isna().sum()}\")\n",
        "else:\n",
        "    print(\"No obvious status fields found. Showing all unique values for text columns:\\n\")\n",
        "    for col in df_events.columns:\n",
        "        if df_events[col].dtype == 'object' and df_events[col].nunique() < 20:\n",
        "            print(f\"\\n{'='*80}\")\n",
        "            print(f\"{col}:\")\n",
        "            print(df_events[col].value_counts())"
    ]
})

# Cell 11: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 6: Filter for No-Show Events\n",
        "\n",
        "**Note:** Based on the status field values above, identify the no-show indicator and update the code below."
    ]
})

# Cell 12: Identify no-show events
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Based on the exploration above, identify the status field and no-show value\n",
        "# ADJUST THESE BASED ON STEP 5 OUTPUT:\n",
        "status_field = 'status'  # ⚠️ UPDATE THIS IF NEEDED\n",
        "no_show_value = 'no_show'  # ⚠️ UPDATE THIS IF NEEDED (could be 'no-show', 'missed', 'absent', etc.)\n",
        "\n",
        "print(\"🎯 Filtering for no-show events...\\n\")\n",
        "\n",
        "# Check if the field exists\n",
        "if status_field in df_events.columns:\n",
        "    print(f\"Using field: {status_field}\")\n",
        "    print(f\"Looking for value: {no_show_value}\\n\")\n",
        "    \n",
        "    # Try to automatically detect no-show pattern\n",
        "    all_values = df_events[status_field].unique()\n",
        "    print(f\"All unique values in {status_field}:\")\n",
        "    for val in all_values:\n",
        "        count = (df_events[status_field] == val).sum()\n",
        "        print(f\"  - {val}: {count}\")\n",
        "    \n",
        "    # Filter for no-show\n",
        "    df_no_show = df_events[df_events[status_field] == no_show_value]\n",
        "    \n",
        "    print(f\"\\n📊 No-Show Statistics:\")\n",
        "    print(f\"Total events: {len(df_events):,}\")\n",
        "    print(f\"No-show events: {len(df_no_show):,}\")\n",
        "    if len(df_events) > 0:\n",
        "        print(f\"No-show rate: {len(df_no_show)/len(df_events)*100:.2f}%\")\n",
        "else:\n",
        "    print(f\"⚠️  Field '{status_field}' not found in data.\")\n",
        "    print(\"Please update the status_field variable based on Step 5 output.\")\n",
        "    df_no_show = pd.DataFrame()"
    ]
})

# Cell 13: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 7: Examine No-Show Records"
    ]
})

# Cell 14: Display no-show records
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Display sample no-show records\n",
        "if not df_no_show.empty:\n",
        "    print(f\"Sample of {min(10, len(df_no_show))} no-show records:\\n\")\n",
        "    display(df_no_show.head(10))\n",
        "    \n",
        "    print(\"\\n\" + \"=\"*80)\n",
        "    print(\"\\nNo-Show DataFrame Info:\")\n",
        "    df_no_show.info()\n",
        "else:\n",
        "    print(\"⚠️  No no-show data available. Please check the filter in Step 6.\")"
    ]
})

# Cell 15: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 8: Analyze No-Show Reasons (if available)"
    ]
})

# Cell 16: Analyze reasons
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Check for reason fields\n",
        "if not df_no_show.empty:\n",
        "    print(\"📝 Looking for reason/note fields...\\n\")\n",
        "    \n",
        "    reason_fields = [col for col in df_no_show.columns if 'reason' in col.lower() \n",
        "                     or 'note' in col.lower() or 'comment' in col.lower() or 'remark' in col.lower()]\n",
        "    \n",
        "    if reason_fields:\n",
        "        print(f\"Found reason fields: {reason_fields}\\n\")\n",
        "        for field in reason_fields:\n",
        "            print(f\"\\n{'='*80}\")\n",
        "            print(f\"{field} - Top 10 reasons:\")\n",
        "            print(df_no_show[field].value_counts().head(10))\n",
        "            print(f\"\\nNull/Empty count: {df_no_show[field].isna().sum()}\")\n",
        "    else:\n",
        "        print(\"⚠️  No obvious reason fields found.\")\n",
        "        print(\"\\nAll available fields:\")\n",
        "        print(df_no_show.columns.tolist())\n",
        "else:\n",
        "    print(\"⚠️  No no-show data to analyze.\")"
    ]
})

# Cell 17: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 9: Temporal Analysis - By Day of Week"
    ]
})

# Cell 18: Day of week analysis
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Temporal analysis by day of week\n",
        "if not df_no_show.empty and date_field_name in df_no_show.columns:\n",
        "    print(\"📅 Analyzing no-shows by day of week...\\n\")\n",
        "    \n",
        "    # Ensure date field is datetime\n",
        "    if df_no_show[date_field_name].dtype != 'datetime64[ns]':\n",
        "        df_no_show['parsed_date'] = pd.to_datetime(df_no_show[date_field_name], errors='coerce')\n",
        "    else:\n",
        "        df_no_show['parsed_date'] = df_no_show[date_field_name]\n",
        "    \n",
        "    # Extract day of week\n",
        "    df_no_show['day_of_week'] = df_no_show['parsed_date'].dt.day_name()\n",
        "    \n",
        "    # Count by day of week\n",
        "    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']\n",
        "    day_counts = df_no_show['day_of_week'].value_counts()\n",
        "    day_counts = day_counts.reindex(day_order, fill_value=0)\n",
        "    \n",
        "    print(\"No-Shows by Day of Week:\")\n",
        "    print(day_counts)\n",
        "    \n",
        "    # Calculate percentages\n",
        "    print(\"\\nPercentage Distribution:\")\n",
        "    print((day_counts / day_counts.sum() * 100).round(2))\n",
        "else:\n",
        "    print(\"⚠️  Cannot perform temporal analysis - no data or date field missing.\")"
    ]
})

# Cell 19: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 10: Temporal Analysis - By Date"
    ]
})

# Cell 20: Date analysis
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Temporal analysis by date\n",
        "if not df_no_show.empty and 'parsed_date' in df_no_show.columns:\n",
        "    print(\"📅 Analyzing no-shows by date...\\n\")\n",
        "    \n",
        "    # Extract date (without time)\n",
        "    df_no_show['date_only'] = df_no_show['parsed_date'].dt.date\n",
        "    \n",
        "    # Count by date\n",
        "    date_counts = df_no_show['date_only'].value_counts().sort_index()\n",
        "    \n",
        "    print(f\"No-shows across {len(date_counts)} different dates\\n\")\n",
        "    print(\"Top 10 dates with most no-shows:\")\n",
        "    print(date_counts.head(10))\n",
        "    \n",
        "    print(\"\\nDates with fewest no-shows:\")\n",
        "    print(date_counts.tail(10))\n",
        "else:\n",
        "    print(\"⚠️  Cannot perform date analysis.\")"
    ]
})

# Cell 21: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 11: Visualizations - Overall No-Show Rate"
    ]
})

# Cell 22: Overall visualization
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Create visualizations\n",
        "if not df_no_show.empty:\n",
        "    print(\"📊 Creating Visualizations\\n\")\n",
        "    \n",
        "    # 1. Overall No-Show Rate\n",
        "    fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n",
        "    \n",
        "    # Pie chart\n",
        "    total_events = len(df_events)\n",
        "    no_show_count = len(df_no_show)\n",
        "    attended_count = total_events - no_show_count\n",
        "    \n",
        "    axes[0].pie([attended_count, no_show_count], \n",
        "                labels=['Attended', 'No-Show'],\n",
        "                autopct='%1.1f%%',\n",
        "                colors=['#2ecc71', '#e74c3c'],\n",
        "                startangle=90)\n",
        "    axes[0].set_title('Overall Attendance vs No-Show\\n(Sept-Oct 2025)', fontsize=14, fontweight='bold')\n",
        "    \n",
        "    # Bar chart\n",
        "    axes[1].bar(['Attended', 'No-Show'], [attended_count, no_show_count], \n",
        "                color=['#2ecc71', '#e74c3c'])\n",
        "    axes[1].set_ylabel('Count', fontsize=12)\n",
        "    axes[1].set_title('Event Counts', fontsize=14, fontweight='bold')\n",
        "    axes[1].grid(axis='y', alpha=0.3)\n",
        "    \n",
        "    # Add count labels on bars\n",
        "    for i, (label, count) in enumerate(zip(['Attended', 'No-Show'], [attended_count, no_show_count])):\n",
        "        axes[1].text(i, count, f'{count:,}', ha='center', va='bottom', fontweight='bold')\n",
        "    \n",
        "    plt.tight_layout()\n",
        "    plt.show()\n",
        "    \n",
        "else:\n",
        "    print(\"⚠️  No data available for visualization.\")"
    ]
})

# Cell 23: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 12: Visualizations - No-Shows by Day of Week"
    ]
})

# Cell 24: Day of week visualization
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Day of week visualization\n",
        "if not df_no_show.empty and 'day_of_week' in df_no_show.columns:\n",
        "    plt.figure(figsize=(14, 6))\n",
        "    \n",
        "    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']\n",
        "    day_counts = df_no_show['day_of_week'].value_counts()\n",
        "    day_counts = day_counts.reindex(day_order, fill_value=0)\n",
        "    \n",
        "    plt.bar(day_counts.index, day_counts.values, color='#3498db')\n",
        "    plt.xlabel('Day of Week', fontsize=12)\n",
        "    plt.ylabel('No-Show Count', fontsize=12)\n",
        "    plt.title('No-Shows by Day of Week (Sept-Oct 2025)', fontsize=14, fontweight='bold')\n",
        "    plt.grid(axis='y', alpha=0.3)\n",
        "    plt.xticks(rotation=45)\n",
        "    \n",
        "    # Add count labels\n",
        "    for i, (day, count) in enumerate(zip(day_counts.index, day_counts.values)):\n",
        "        plt.text(i, count, str(count), ha='center', va='bottom', fontweight='bold')\n",
        "    \n",
        "    plt.tight_layout()\n",
        "    plt.show()\n",
        "else:\n",
        "    print(\"⚠️  Cannot create day of week visualization.\")"
    ]
})

# Cell 25: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 13: Visualizations - No-Show Reasons (if available)"
    ]
})

# Cell 26: Reasons visualization
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Reasons visualization (if available)\n",
        "if not df_no_show.empty and reason_fields:\n",
        "    reason_field = reason_fields[0]\n",
        "    \n",
        "    # Get top 10 reasons\n",
        "    top_reasons = df_no_show[reason_field].value_counts().head(10)\n",
        "    \n",
        "    if len(top_reasons) > 0:\n",
        "        plt.figure(figsize=(14, 6))\n",
        "        plt.barh(range(len(top_reasons)), top_reasons.values, color='#e67e22')\n",
        "        plt.yticks(range(len(top_reasons)), top_reasons.index)\n",
        "        plt.xlabel('Count', fontsize=12)\n",
        "        plt.ylabel('Reason', fontsize=12)\n",
        "        plt.title('Top 10 Reasons for No-Shows (Sept-Oct 2025)', fontsize=14, fontweight='bold')\n",
        "        plt.grid(axis='x', alpha=0.3)\n",
        "        \n",
        "        # Add count labels\n",
        "        for i, count in enumerate(top_reasons.values):\n",
        "            plt.text(count, i, f' {count}', va='center', fontweight='bold')\n",
        "        \n",
        "        plt.tight_layout()\n",
        "        plt.show()\n",
        "else:\n",
        "    print(\"⚠️  No reason data available for visualization.\")"
    ]
})

# Cell 27: Section header
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 14: Summary of Key Findings"
    ]
})

# Cell 28: Summary
notebook['cells'].append({
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# Summary of findings\n",
        "print(\"=\"*80)\n",
        "print(\"📋 KEY FINDINGS - NO-SHOW ANALYSIS (Sept 1 - Oct 31, 2025)\")\n",
        "print(\"=\"*80)\n",
        "\n",
        "if not df_no_show.empty:\n",
        "    print(f\"\\n1. OVERALL STATISTICS:\")\n",
        "    print(f\"   • Total clinic events: {len(df_events):,}\")\n",
        "    print(f\"   • No-show events: {len(df_no_show):,}\")\n",
        "    print(f\"   • Attended events: {len(df_events) - len(df_no_show):,}\")\n",
        "    print(f\"   • No-show rate: {len(df_no_show)/len(df_events)*100:.2f}%\")\n",
        "    \n",
        "    if 'day_of_week' in df_no_show.columns:\n",
        "        print(f\"\\n2. TEMPORAL PATTERNS:\")\n",
        "        day_counts = df_no_show['day_of_week'].value_counts()\n",
        "        print(f\"   • Highest no-show day: {day_counts.index[0]} ({day_counts.values[0]} events)\")\n",
        "        print(f\"   • Lowest no-show day: {day_counts.index[-1]} ({day_counts.values[-1]} events)\")\n",
        "    \n",
        "    if reason_fields and not df_no_show[reason_fields[0]].isna().all():\n",
        "        print(f\"\\n3. COMMON REASONS:\")\n",
        "        top_reasons = df_no_show[reason_fields[0]].value_counts().head(5)\n",
        "        for i, (reason, count) in enumerate(top_reasons.items(), 1):\n",
        "            pct = count/len(df_no_show)*100\n",
        "            print(f\"   {i}. {reason}: {count} ({pct:.1f}%)\")\n",
        "    \n",
        "    print(f\"\\n4. DATA QUALITY:\")\n",
        "    print(f\"   • Complete records: {df_no_show.notna().all(axis=1).sum():,}\")\n",
        "    print(f\"   • Records with missing data: {df_no_show.isna().any(axis=1).sum():,}\")\n",
        "    \n",
        "else:\n",
        "    print(\"\\n⚠️  Unable to generate findings - no no-show data identified.\")\n",
        "    print(\"Please review the data exploration sections above to manually identify no-show events.\")\n",
        "\n",
        "print(\"\\n\" + \"=\"*80)"
    ]
})

# Cell 29: Recommendations section
notebook['cells'].append({
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## Step 15: Recommendations\n",
        "\n",
        "Based on the analysis above, here are recommendations for reducing no-shows:\n",
        "\n",
        "### Current Handling Procedures\n",
        "*To be documented based on operational knowledge*\n",
        "\n",
        "### Data-Driven Recommendations\n",
        "\n",
        "1. **Target High-Risk Days**\n",
        "   - Focus reminder efforts on days with highest no-show rates\n",
        "   - Consider overbooking strategies for high-risk time slots\n",
        "\n",
        "2. **Address Common Reasons**\n",
        "   - Develop specific interventions for top no-show reasons\n",
        "   - Improve pre-appointment communication\n",
        "\n",
        "3. **Enhanced Tracking**\n",
        "   - Track patient no-show history\n",
        "   - Create risk scores for future appointments\n",
        "\n",
        "4. **Process Improvements**\n",
        "   - Streamline rescheduling process\n",
        "   - Implement automated reminder systems\n",
        "   - Consider waitlist management"
    ]
})

# Write the updated notebook
with open(notebook_path, 'w') as f:
    json.dump(notebook, f, indent=1)

print(f"✅ Successfully updated {notebook_path}")
print(f"Total cells: {len(notebook['cells'])}")
print(f"\\nThe notebook now includes step-by-step analysis for Sept 1 - Oct 31, 2025 data.")
