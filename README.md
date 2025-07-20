# Work shift calendar helper

A python tool that helps workers with managing their shifts in their google calendar

## Installation

### Prerequisites

- Python 3.12 or higher
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/elizaluszczyk/work-calendar-helper
   ```

2. **Navigate to the project directory**
   ```bash
   cd work-calendar-helper
   ```

3. **Install the package**
   ```bash
   pip install .
   ```

## Usage

### Creating and Managing Shifts

Launch the shift planner TUI with:
```bash
work_cal planner <month number 1-12>
```

The interface consists of two main panels:
- **Left panel**: Shift editor for adding/modifying shift details
- **Right panel**: List view showing all days in the selected month

#### Adding Shifts
1. Select a day from the list on the right
2. Navigate to the editor panel (use `Tab` or mouse)
3. Fill in the shift details:
   - Shift name
   - Start time
   - End time
4. Optionally use a predefined template from your configuration to auto-fill fields - you can modify the default values
5. Click **Save** to store the shift

#### Managing Existing Shifts
- **Modify**: Select a day with an existing shift, edit the fields, and save
- **Remove**: Use the **Clear Shift** button to delete a saved shift

#### Navigation
- Use `Tab` to move between interface elements
- Use mouse for point-and-click navigation
- Press `Ctrl+Q` to exit and save all changes

All shifts are automatically saved to the location specified in your configuration file.

### Exporting to Calendar Format

Convert your saved shifts to an importable calendar file:
```bash
work_cal dump <filename.ics>
```

1. Use the interactive file selector (fzf) to choose which saved shift file to export
2. Press `Enter` to confirm your selection
3. The ICS file will be generated and saved
4. Import the generated `.ics` file into your preferred calendar application

Your shifts are now ready to view in any calendar app that supports the ICS format.


## Configuration File

The configuration file should be placed at `~/.config/cal_manager/config.toml` and uses TOML format.

### Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `worker_name` | String | Your name |
| `timezone` | String | Your local timezone (e.g., "Europe/Warsaw", "America/New_York") |
| `fzf_options` | String | Custom options for the fzf file selector interface |
| `month_dump_location` | String | Directory path where shift files will be saved |

### Shift Templates

Define reusable shift templates using `[[shift_types]]` sections. Each template can include:

| Field | Type | Description |
|-------|------|-------------|
| `name` | String | Display name for the shift template |
| `start_hour` | String | Start time in HH:MM format (24-hour) |
| `end_hour` | String | End time in HH:MM format (24-hour) |
| `allowed_week_days` | Array | Days of week when this shift is available (0=Monday, 6=Sunday) |

### Example Configuration

```toml
worker_name = "Eliza Łuszczyk"
timezone = "Europe/Warsaw"
fzf_options = "--height=~60%"
month_dump_location = "/home/eliza/.dump"

[[shift_types]]
name = "Shift - weekend"
start_hour = "11:00"
end_hour = "23:00"
allowed_week_days = [5, 6]  # Saturday and Sunday

[[shift_types]]
name = "Shift - even days"
start_hour = "13:00"
end_hour = "21:00"
allowed_week_days = [0, 2, 4]  # Monday, Wednesday, Friday

[[shift_types]]
name = "Shift - odd days"
start_hour = "13:00"
end_hour = "21:00"
allowed_week_days = [1, 3]  # Tuesday, Thursday
```

### Notes

- Week days are numbered 0-6 (Monday=0, Sunday=6)
- Times must be in 24-hour format (HH:MM)
- The configuration directory will be created automatically if it doesn't exist
- Templates with `allowed_week_days` will only be available on those specific days in the TUI
