import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('profile_results.csv')

# Filter out profiles with status 'validation_passed' to focus on problematic ones
df_filtered = df[df['status'] != 'validation_passed']

# Create flow chart data
profiles = []
statuses = []
colors = []

# Process profiles and extract info
for index, row in df_filtered.iterrows():
    name = row["profile_name"]
    parts = name.split("_")
    periodOfProfile = parts[1] if len(parts) > 1 else "unknown"
    kindOfProfile = parts[2] if len(parts) > 2 else "unknown"
    periodOfFunction = parts[3] if len(parts) > 3 else "unknown"
    kindOfFunction = parts[4] if len(parts) > 4 else "unknown"
    isLeapYear = row['is_leap_year'] if 'is_leap_year' in row else 'unknown'
    status = row['status']
    actualValue = row['actual_value']
    expectedValue = row['expected_value']
    
    # Create profile info display
    profile_info = f"<br>Profile Name: {name}<br>Period: {periodOfProfile}<br>Kind: {kindOfProfile}<br>Function:{kindOfFunction} <br>Function Period {periodOfFunction} <br>Actual: {actualValue}<br>Expected: {expectedValue} <br>Leap Year: {isLeapYear}"
    profiles.append(profile_info)
    statuses.append(status)
    
    # Color based on status
    if status == 'passed':
        colors.append('green')
    else:
        colors.append('red')

# Create Sankey diagram (flow chart)
# Get unique statuses for target nodes
unique_statuses = list(df_filtered['status'].unique())
source_nodes = list(range(len(profiles)))  # Profile indices
target_nodes = list(range(len(profiles), len(profiles) + len(unique_statuses)))  # Status categories

# Create labels for all nodes
all_labels = profiles + unique_statuses

# Create source and target lists for flows
sources = []
targets = []
values = []
link_colors = []

for i, status in enumerate(statuses):
    sources.append(i)  # From profile
    target_idx = len(profiles) + unique_statuses.index(status)
    targets.append(target_idx)  # To status category
    
    if status == 'passed':
        link_colors.append('rgba(0, 255, 0, 0.3)')  # Green with transparency
    else:
        link_colors.append('rgba(255, 0, 0, 0.3)')  # Red with transparency
    values.append(1)  # Each flow has value 1

# Create Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=all_labels,
        color=['lightblue' if i < len(profiles) else 'lightgreen' if 'passed' in all_labels[i] else 'lightcoral' for i in range(len(all_labels))]
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        color=link_colors
    )
)])

fig.update_layout(
    title_text="Profile Test Results Flow Chart (Excluding validation_passed)",
    font_size=10,
    height=max(600, len(profiles) * 30)
)

fig.show()
# save the figure as an HTML file
fig.write_html("failed.html")

# Print summary of filtered results
print(f"\nSUMMARY (Excluding validation_passed):")
print(f"Total profiles shown: {len(df_filtered)}")
print(f"Total profiles excluded (validation_passed): {len(df) - len(df_filtered)}")
for status in df_filtered['status'].unique():
    count = len(df_filtered[df_filtered['status'] == status])
    print(f"{status}: {count}")