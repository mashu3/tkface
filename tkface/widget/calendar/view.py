"""
View and UI functionality for the Calendar widget.

This module provides UI creation, display updates, and user interaction
handling for the Calendar widget.
"""

import calendar
import datetime
import tkinter as tk
from typing import List

from ... import lang
from .style import DayColorContext, _determine_day_colors


def _create_container(calendar_instance):
    """Create the main container (single month or scrollable)."""
    is_single_month = calendar_instance.months == 1
    if is_single_month:
        calendar_instance.months_container = tk.Frame(
            calendar_instance,
            relief="flat",
            bd=1,
            bg=calendar_instance.theme_colors["background"],
        )
        calendar_instance.months_container.pack(
            fill="both", expand=True, padx=2, pady=2
        )
    else:
        # Create scrollable container for multiple months
        calendar_instance.canvas = tk.Canvas(
            calendar_instance, bg=calendar_instance.theme_colors["background"]
        )
        calendar_instance.scrollbar = tk.Scrollbar(
            calendar_instance,
            orient="horizontal",
            command=calendar_instance.canvas.xview,
        )
        calendar_instance.scrollable_frame = tk.Frame(
            calendar_instance.canvas, bg=calendar_instance.theme_colors["background"]
        )
        calendar_instance.scrollable_frame.bind(
            "<Configure>",
            lambda e: calendar_instance.canvas.configure(
                scrollregion=calendar_instance.canvas.bbox("all")
            ),
        )
        calendar_instance.canvas.create_window(
            (0, 0), window=calendar_instance.scrollable_frame, anchor="nw"
        )
        calendar_instance.canvas.configure(
            xscrollcommand=calendar_instance.scrollbar.set
        )
        # Pack scrollbar and canvas
        calendar_instance.scrollbar.pack(side="bottom", fill="x")
        calendar_instance.canvas.pack(side="top", fill="both", expand=True)
        # Configure grid weights for the scrollable frame
        for i in range(calendar_instance.grid_cols):
            calendar_instance.scrollable_frame.columnconfigure(i, weight=1)
        for i in range(calendar_instance.grid_rows):
            calendar_instance.scrollable_frame.rowconfigure(i, weight=1)
    return is_single_month


def _create_navigation_buttons(calendar_instance, center_frame, month_index):
    """Create navigation buttons for a month."""
    year_first = calendar_instance._is_year_first_in_format()  # pylint: disable=W0212
    # Define navigation items in order based on date format
    nav_items = (
        [
            (
                "year",
                "<<",
                ">>",
                calendar_instance._on_prev_year,  # pylint: disable=W0212
                calendar_instance._on_next_year,  # pylint: disable=W0212
            ),
            (
                "month",
                "<",
                ">",
                calendar_instance._on_prev_month,  # pylint: disable=W0212
                calendar_instance._on_next_month,  # pylint: disable=W0212
            ),
        ]
        if year_first
        else [
            (
                "month",
                "<",
                ">",
                calendar_instance._on_prev_month,  # pylint: disable=W0212
                calendar_instance._on_next_month,  # pylint: disable=W0212
            ),
            (
                "year",
                "<<",
                ">>",
                calendar_instance._on_prev_year,  # pylint: disable=W0212
                calendar_instance._on_next_year,  # pylint: disable=W0212
            ),
        ]
    )

    for (
        item_type,
        prev_text,
        next_text,
        prev_cmd,
        next_cmd,
    ) in nav_items:
        _create_navigation_item(
            calendar_instance,
            center_frame,
            month_index,
            item_type,
            prev_text,
            next_text,
            prev_cmd,
            next_cmd,
            year_first,
        )


def _create_navigation_item(  # pylint: disable=R0917
    calendar_instance,
    center_frame,
    month_index,
    item_type,
    prev_text,
    next_text,
    prev_cmd,
    next_cmd,
    year_first,
):
    """Create a single navigation item (prev button, label, next button)."""
    # Previous button
    prev_btn = tk.Label(
        center_frame,
        text=prev_text,
        font=calendar_instance._get_scaled_font(  # pylint: disable=W0212
            calendar_instance.theme_colors["navigation_font"]
        ),
        bg=calendar_instance.theme_colors["navigation_bg"],
        fg=calendar_instance.theme_colors["navigation_fg"],
        cursor="hand2",
    )
    prev_btn.pack(side="left", padx=(5, 0))
    prev_btn.bind("<Button-1>", lambda e, m=month_index, cmd=prev_cmd: cmd(m))
    prev_btn.bind(
        "<Enter>",
        lambda e, btn=prev_btn: btn.config(
            bg=calendar_instance.theme_colors["navigation_hover_bg"],
            fg=calendar_instance.theme_colors["navigation_hover_fg"],
        ),
    )
    prev_btn.bind(
        "<Leave>",
        lambda e, btn=prev_btn: btn.config(
            bg=calendar_instance.theme_colors["navigation_bg"],
            fg=calendar_instance.theme_colors["navigation_fg"],
        ),
    )

    # Label
    is_year = item_type == "year"
    label = tk.Label(
        center_frame,
        font=calendar_instance._get_scaled_font(  # pylint: disable=W0212
            ("TkDefaultFont", 9, "bold")
        ),
        relief="flat",
        bd=0,
        bg=calendar_instance.theme_colors["month_header_bg"],
        fg=calendar_instance.theme_colors["month_header_fg"],
        cursor="hand2" if not is_year else "",
    )

    if not is_year:
        # Ensure month header is clickable
        label.bind(
            "<Button-1>",
            lambda e, m=month_index: (
                calendar_instance._on_month_header_click(m)  # pylint: disable=W0212
            ),
        )
        label.bind(
            "<Enter>",
            lambda e, lbl=label: lbl.config(
                bg=calendar_instance.theme_colors["navigation_hover_bg"],
                fg=calendar_instance.theme_colors["navigation_hover_fg"],
            ),
        )
        label.bind(
            "<Leave>",
            lambda e, lbl=label: lbl.config(
                bg=calendar_instance.theme_colors["month_header_bg"],
                fg=calendar_instance.theme_colors["month_header_fg"],
            ),
        )
        calendar_instance.month_headers.append(label)
    else:
        calendar_instance.year_labels.append(label)
    label.pack(side="left", padx=2)

    # Next button
    next_btn = tk.Label(
        center_frame,
        text=next_text,
        font=calendar_instance._get_scaled_font(  # pylint: disable=W0212
            calendar_instance.theme_colors["navigation_font"]
        ),
        bg=calendar_instance.theme_colors["navigation_bg"],
        fg=calendar_instance.theme_colors["navigation_fg"],
        cursor="hand2",
    )
    next_btn.pack(
        side="left",
        padx=(
            0,
            (10 if item_type == ("year" if year_first else "month") else 5),
        ),
    )
    next_btn.bind("<Button-1>", lambda e, m=month_index, cmd=next_cmd: cmd(m))
    next_btn.bind(
        "<Enter>",
        lambda e, btn=next_btn: btn.config(
            bg=calendar_instance.theme_colors["navigation_hover_bg"],
            fg=calendar_instance.theme_colors["navigation_hover_fg"],
        ),
    )
    next_btn.bind(
        "<Leave>",
        lambda e, btn=next_btn: btn.config(
            bg=calendar_instance.theme_colors["navigation_bg"],
            fg=calendar_instance.theme_colors["navigation_fg"],
        ),
    )


def _create_month_header(calendar_instance, month_frame, month_index):
    """Create month header with navigation."""
    if not calendar_instance.show_month_headers:
        return

    header_frame = tk.Frame(
        month_frame, bg=calendar_instance.theme_colors["month_header_bg"]
    )
    header_frame.pack(fill="x", pady=(2, 0))

    nav_frame = tk.Frame(
        header_frame, bg=calendar_instance.theme_colors["month_header_bg"]
    )
    nav_frame.pack(expand=True, fill="x")

    center_frame = tk.Frame(
        nav_frame, bg=calendar_instance.theme_colors["month_header_bg"]
    )
    center_frame.pack(expand=True)

    _create_navigation_buttons(calendar_instance, center_frame, month_index)


def _create_widgets(calendar_instance):  # pylint: disable=W0212
    """Create the calendar widget structure."""
    # Set main frame background color
    calendar_instance.configure(bg=calendar_instance.theme_colors["background"])

    # Create container
    is_single_month = _create_container(calendar_instance)

    # Initialize label lists
    calendar_instance.year_labels = []
    calendar_instance.month_headers = []

    # Create month frames in grid layout
    for i in range(calendar_instance.months):
        row = i // calendar_instance.grid_cols
        col = i % calendar_instance.grid_cols

        if is_single_month:
            month_frame = tk.Frame(
                calendar_instance.months_container,
                relief="flat",
                bd=1,
                bg=calendar_instance.theme_colors["background"],
            )
            month_frame.pack(fill="both", expand=True, padx=2, pady=2)
        else:
            month_frame = tk.Frame(
                calendar_instance.scrollable_frame,
                relief="flat",
                bd=1,
                bg=calendar_instance.theme_colors["background"],
            )
            month_frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

        calendar_instance.month_frames.append(month_frame)

        # Create month header
        _create_month_header(calendar_instance, month_frame, i)

        # Calendar grid (including header)
        _create_calendar_grid(calendar_instance, month_frame, i)


def _create_calendar_grid(calendar_instance, month_frame, month_index):
    """Create the calendar grid for a specific month."""
    grid_frame = tk.Frame(month_frame, bg=calendar_instance.theme_colors["background"])
    grid_frame.pack(fill="both", expand=True, padx=2, pady=2)
    # Configure grid weights
    if calendar_instance.show_week_numbers:
        grid_frame.columnconfigure(0, weight=1)
        for i in range(7):
            grid_frame.columnconfigure(i + 1, weight=1)
    else:
        for i in range(7):
            grid_frame.columnconfigure(i, weight=1)
    # Configure row weights (header row + 6 week rows)
    grid_frame.rowconfigure(0, weight=0)  # Header row (no expansion)
    for week in range(6):  # Maximum 6 weeks
        grid_frame.rowconfigure(week + 1, weight=1)
    # Create day name headers (row 0)
    day_names = _get_day_names(calendar_instance, short=True)
    if calendar_instance.show_week_numbers:
        # Empty header for week number column
        empty_header = tk.Label(
            grid_frame,
            text="",
            font=calendar_instance._get_scaled_font(  # pylint: disable=W0212
                ("TkDefaultFont", 8)
            ),
            relief="flat",
            bd=0,
            bg=calendar_instance.theme_colors["day_header_bg"],
            fg=calendar_instance.theme_colors["day_header_fg"],
        )
        empty_header.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
    for day, day_name in enumerate(day_names):
        day_header = tk.Label(
            grid_frame,
            text=day_name,
            font=calendar_instance._get_scaled_font(  # pylint: disable=W0212
                calendar_instance.theme_colors["day_header_font"]
            ),
            relief="flat",
            bd=0,
            bg=calendar_instance.theme_colors["day_header_bg"],
            fg=calendar_instance.theme_colors["day_header_fg"],
        )
        col = day + 1 if calendar_instance.show_week_numbers else day
        day_header.grid(row=0, column=col, sticky="nsew", padx=1, pady=1)
    # Create labels for each week and day
    for week in range(6):  # Maximum 6 weeks
        # Week number label
        if calendar_instance.show_week_numbers:
            week_label = tk.Label(
                grid_frame,
                font=calendar_instance._get_scaled_font(  # pylint: disable=W0212
                    calendar_instance.theme_colors["week_number_font"]
                ),
                relief="flat",
                bd=0,
                bg=calendar_instance.theme_colors["week_number_bg"],
                fg=calendar_instance.theme_colors["week_number_fg"],
            )
            week_label.grid(row=week + 1, column=0, sticky="nsew", padx=1, pady=1)
            calendar_instance.week_labels.append(week_label)
        # Day labels (clickable)
        for day in range(7):
            day_label = tk.Label(
                grid_frame,
                font=calendar_instance._get_scaled_font(  # pylint: disable=W0212
                    calendar_instance.theme_colors["day_font"]
                ),
                relief="flat",
                bd=0,
                anchor="center",
                bg=calendar_instance.theme_colors["day_bg"],
                fg=calendar_instance.theme_colors["day_fg"],
                cursor="hand2",
            )
            col = day + 1 if calendar_instance.show_week_numbers else day
            day_label.grid(row=week + 1, column=col, sticky="nsew", padx=1, pady=1)
            # Store original colors for this label
            calendar_instance.original_colors[day_label] = {
                "bg": calendar_instance.theme_colors["day_bg"],
                "fg": calendar_instance.theme_colors["day_fg"],
            }
            # Bind click events
            day_label.bind(
                "<Button-1>",
                lambda e, m=month_index, w=week, d=day: (
                    calendar_instance._on_date_click(m, w, d)  # pylint: disable=W0212
                ),
            )
            day_label.bind(
                "<Enter>",
                lambda e, label=day_label: _on_mouse_enter(calendar_instance, label),
            )
            day_label.bind(
                "<Leave>",
                lambda e, label=day_label: _on_mouse_leave(calendar_instance, label),
            )
            calendar_instance.day_labels.append((month_index, week, day, day_label))


def _get_day_names(
    calendar_instance, short: bool = False
) -> List[str]:  # pylint: disable=W0212
    """Get localized day names."""
    # Define base day names
    full_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    short_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    # Choose day list based on short parameter
    days = short_days if short else full_days
    # Shift days based on week_start
    if calendar_instance.week_start == "Sunday":
        # Move Sunday to the beginning
        days = days[-1:] + days[:-1]
    elif calendar_instance.week_start == "Saturday":
        # Move Saturday to the beginning
        days = days[-2:] + days[:-2]
    # Get translations and handle short names
    day_names = []
    for day in days:
        if short:
            # For short names, get full name translation first, then truncate
            full_name = full_days[short_days.index(day)]
            full_translated = lang.get(full_name, calendar_instance.winfo_toplevel())
            translated = (
                full_translated[:3] if len(full_translated) >= 3 else full_translated
            )
        else:
            translated = lang.get(day, calendar_instance.winfo_toplevel())
        day_names.append(translated)
    return day_names


def _get_month_name(
    calendar_instance, month: int, short: bool = False
) -> str:  # pylint: disable=W0212
    """Get localized month name."""
    # Define base month names
    full_months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    # Get the month name based on short parameter
    if short:
        # For short names, get full name translation first, then truncate
        full_name = full_months[month - 1]
        full_translated = lang.get(full_name, calendar_instance.winfo_toplevel())
        return full_translated[:3] if len(full_translated) >= 3 else full_translated
    month_name = full_months[month - 1]
    return lang.get(month_name, calendar_instance.winfo_toplevel())


def _on_mouse_enter(calendar_instance, label):  # pylint: disable=W0212
    """Handle mouse enter event."""
    # Only highlight if not already selected
    current_bg = label.cget("bg")
    if current_bg not in [
        calendar_instance.theme_colors["selected_bg"],
        calendar_instance.theme_colors["range_bg"],
    ]:
        # Store current colors before changing to hover
        if label not in calendar_instance.original_colors:
            calendar_instance.original_colors[label] = {
                "bg": current_bg,
                "fg": label.cget("fg"),
            }
        label.config(
            bg=calendar_instance.theme_colors["hover_bg"],
            fg=calendar_instance.theme_colors["hover_fg"],
        )


def _on_mouse_leave(calendar_instance, label):  # pylint: disable=W0212
    """Handle mouse leave event."""
    # Only restore if not selected
    current_bg = label.cget("bg")
    if (
        current_bg == calendar_instance.theme_colors["hover_bg"]
        and label in calendar_instance.original_colors
    ):
        # Restore original colors
        original = calendar_instance.original_colors[label]
        label.config(bg=original["bg"], fg=original["fg"])


def _update_display(calendar_instance):  # pylint: disable=W0212
    """Update the calendar display."""
    if not calendar_instance.winfo_exists():
        return
    # Check if in year view mode
    if calendar_instance.year_view_mode:
        _update_year_view(calendar_instance)
        return
    week_label_index = 0
    for month_offset in range(calendar_instance.months):
        # Get display date using existing helper
        display_date = calendar_instance._get_display_date(  # pylint: disable=W0212
            month_offset
        )
        display_year = display_date.year
        display_month = display_date.month
        # Update year and month headers
        if calendar_instance.show_month_headers:
            _update_month_headers(
                calendar_instance, month_offset, display_year, display_month
            )
        # Update day name headers
        children = calendar_instance.month_frames[month_offset].winfo_children()
        if calendar_instance.show_month_headers and len(children) > 1:
            days_frame = children[1]
        else:
            days_frame = children[0]
        _update_day_name_headers(calendar_instance, days_frame)
        # Get calendar data efficiently using monthrange
        _, _last_day = calendar.monthrange(display_year, display_month)
        month_days = list(
            calendar_instance.cal.itermonthdays(display_year, display_month)
        )
        # Update week numbers
        if calendar_instance.show_week_numbers:
            week_label_index = _update_week_numbers(
                calendar_instance, display_year, display_month, week_label_index
            )
        # Update day labels
        _update_day_labels(
            calendar_instance, month_offset, display_year, display_month, month_days
        )
        # Update week label index for next month
        if calendar_instance.show_week_numbers:
            week_label_index += 6


def _update_month_headers(
    calendar_instance, month_offset: int, display_year: int, display_month: int
):
    """Update year and month headers."""
    if hasattr(calendar_instance, "year_labels") and month_offset < len(
        calendar_instance.year_labels
    ):
        year_label = calendar_instance.year_labels[month_offset]
        year_label.config(text=str(display_year))
    if hasattr(calendar_instance, "month_headers") and month_offset < len(
        calendar_instance.month_headers
    ):
        month_label = calendar_instance.month_headers[month_offset]
        month_label.config(
            text=_get_month_name(calendar_instance, display_month, short=True)
        )


def _update_day_name_headers(calendar_instance, days_frame):
    """Update day name headers."""
    day_names = _get_day_names(calendar_instance, short=True)
    # Find day header labels and update them
    day_header_index = 0
    for child in days_frame.winfo_children():
        if isinstance(child, tk.Label) and child.cget("text") == "":
            # Skip empty header (week number column)
            continue
        if isinstance(child, tk.Label):
            # This is a day header
            if day_header_index < len(day_names):
                child.config(text=day_names[day_header_index])
                day_header_index += 1


def _update_day_labels(
    calendar_instance,
    month_offset: int,
    display_year: int,
    display_month: int,
    month_days,
):
    """Update day labels for a specific month."""
    for week in range(6):
        for day in range(7):
            day_index = week * 7 + day
            # Find the corresponding label
            for m, w, d, label in calendar_instance.day_labels:
                if m == month_offset and w == week and d == day:
                    _update_single_day_label(
                        calendar_instance,
                        label,
                        display_year,
                        display_month,
                        week,
                        day,
                        day_index,
                        month_days,
                    )
                    break


def _update_single_day_label(  # pylint: disable=R0917
    calendar_instance,
    label,
    display_year: int,
    display_month: int,
    week: int,
    day: int,
    day_index: int,
    month_days,
):
    """Update a single day label."""
    if day_index < len(month_days):
        day_num = month_days[day_index]
        if day_num == 0:
            # Empty day - show previous/next month days
            _set_adjacent_month_day(
                calendar_instance, label, display_year, display_month, week, day
            )
        else:
            # Valid day
            label.config(text=str(day_num))
            # Set colors
            _set_day_colors(
                calendar_instance, label, display_year, display_month, day_num
            )
    else:
        # Beyond month days
        _set_adjacent_month_day(
            calendar_instance, label, display_year, display_month, week, day
        )


def _update_week_numbers(
    calendar_instance, display_year: int, display_month: int, week_label_index: int
) -> int:
    """Update week numbers for a specific month."""
    # Reuse existing calendar object for efficiency
    month_calendar = calendar_instance.cal.monthdatescalendar(
        display_year, display_month
    )
    for week in range(6):
        if week_label_index + week < len(calendar_instance.week_labels):
            week_label = calendar_instance.week_labels[week_label_index + week]
            if week < len(month_calendar):
                # Get the week dates
                week_dates = month_calendar[week]
                # Check if this week contains days from the current month
                week_has_month_days = any(
                    date.year == display_year and date.month == display_month
                    for date in week_dates
                )
                if week_has_month_days:
                    # For ISO week numbers, we need to use the Monday of the week
                    # as the reference date for week number calculation
                    reference_date = (
                        calendar_instance._get_week_ref_date(  # pylint: disable=W0212
                            week_dates
                        )
                    )
                    week_num = reference_date.isocalendar()[1]
                    week_label.config(text=str(week_num))
                else:
                    week_label.config(text="")
            else:
                week_label.config(text="")
    return week_label_index


def _set_adjacent_month_day(  # pylint: disable=R0917
    calendar_instance, label, year: int, month: int, week: int, day: int
):
    """Set display for adjacent month days."""
    # Calculate the date for this position using datetime arithmetic
    first_day = datetime.date(year, month, 1)
    # Get the first day of the week for this month efficiently
    first_weekday = calendar_instance._get_week_start_offset(  # pylint: disable=W0212
        first_day
    )
    # Calculate the date for this position
    days_from_start = week * 7 + day - first_weekday
    clicked_date = first_day + datetime.timedelta(days=days_from_start)
    # Check if the date is valid (not in current month) using calendar module
    _, last_day = calendar.monthrange(year, month)
    current_month_start = datetime.date(year, month, 1)
    current_month_end = datetime.date(year, month, last_day)
    if clicked_date < current_month_start or clicked_date > current_month_end:
        # Adjacent month day
        label.config(
            text=str(clicked_date.day),
            bg=calendar_instance.theme_colors["adjacent_day_bg"],
            fg=calendar_instance.theme_colors["adjacent_day_fg"],
        )
    else:
        # Empty day
        label.config(
            text="",
            bg=calendar_instance.theme_colors["day_bg"],
            fg=calendar_instance.theme_colors["day_fg"],
        )


def _set_day_colors(
    calendar_instance, label, year: int, month: int, day: int
):  # pylint: disable=W0212
    """Set colors for a specific day."""
    # Create context for color determination
    context = DayColorContext(
        theme_colors=calendar_instance.theme_colors,
        selected_date=calendar_instance.selected_date,
        selected_range=calendar_instance.selected_range,
        today=datetime.date.today(),
        today_color=calendar_instance.today_color,
        today_color_set=calendar_instance.today_color_set,
        day_colors=calendar_instance.day_colors,
        holidays=calendar_instance.holidays,
        date_obj=datetime.date(year, month, day),
        year=year,
        month=month,
        day=day,
    )

    # Get colors based on various conditions
    colors = _determine_day_colors(context)

    # Apply colors
    label.config(bg=colors.bg, fg=colors.fg)
    # Update original colors for hover effect restoration
    if label in calendar_instance.original_colors:
        calendar_instance.original_colors[label] = {"bg": colors.bg, "fg": colors.fg}


def _create_year_view_content(calendar_instance):  # pylint: disable=W0212
    """Create year view content with 3x4 month grid."""
    # Set main frame background color
    calendar_instance.configure(bg=calendar_instance.theme_colors["background"])
    # Year header with navigation
    if calendar_instance.show_navigation:
        header_frame = tk.Frame(
            calendar_instance, bg=calendar_instance.theme_colors["month_header_bg"]
        )
        header_frame.pack(fill="x", pady=(5, 0))
        nav_frame = tk.Frame(
            header_frame, bg=calendar_instance.theme_colors["month_header_bg"]
        )
        nav_frame.pack(expand=True, fill="x")
        center_frame = tk.Frame(
            nav_frame, bg=calendar_instance.theme_colors["month_header_bg"]
        )
        center_frame.pack(expand=True)
        # Previous year button
        prev_btn = tk.Label(
            center_frame,
            text="<<",
            font=calendar_instance._get_scaled_font(  # pylint: disable=W0212
                calendar_instance.theme_colors["navigation_font"]
            ),
            bg=calendar_instance.theme_colors["navigation_bg"],
            fg=calendar_instance.theme_colors["navigation_fg"],
            cursor="hand2",
        )
        prev_btn.pack(side="left", padx=(5, 0))
        prev_btn.bind(
            "<Button-1>",
            lambda e: calendar_instance._on_prev_year_view(),  # pylint: disable=W0212
        )
        prev_btn.bind(
            "<Enter>",
            lambda e, btn=prev_btn: btn.config(
                bg=calendar_instance.theme_colors["navigation_hover_bg"],
                fg=calendar_instance.theme_colors["navigation_hover_fg"],
            ),
        )
        prev_btn.bind(
            "<Leave>",
            lambda e, btn=prev_btn: btn.config(
                bg=calendar_instance.theme_colors["navigation_bg"],
                fg=calendar_instance.theme_colors["navigation_fg"],
            ),
        )
        # Year label
        calendar_instance.year_view_year_label = tk.Label(
            center_frame,
            text=str(calendar_instance.year),
            font=(
                calendar_instance._get_scaled_font(  # pylint: disable=W0212
                    ("TkDefaultFont", 12, "bold")
                )
            ),
            relief="flat",
            bd=0,
            bg=calendar_instance.theme_colors["month_header_bg"],
            fg=calendar_instance.theme_colors["month_header_fg"],
        )
        calendar_instance.year_view_year_label.pack(side="left", padx=10)
        # Next year button
        next_btn = tk.Label(
            center_frame,
            text=">>",
            font=calendar_instance._get_scaled_font(  # pylint: disable=W0212
                calendar_instance.theme_colors["navigation_font"]
            ),
            bg=calendar_instance.theme_colors["navigation_bg"],
            fg=calendar_instance.theme_colors["navigation_fg"],
            cursor="hand2",
        )
        next_btn.pack(side="left", padx=(0, 10))
        next_btn.bind(
            "<Button-1>",
            lambda e: calendar_instance._on_next_year_view(),  # pylint: disable=W0212
        )
        next_btn.bind(
            "<Enter>",
            lambda e, btn=next_btn: btn.config(
                bg=calendar_instance.theme_colors["navigation_hover_bg"],
                fg=calendar_instance.theme_colors["navigation_hover_fg"],
            ),
        )
        next_btn.bind(
            "<Leave>",
            lambda e, btn=next_btn: btn.config(
                bg=calendar_instance.theme_colors["navigation_bg"],
                fg=calendar_instance.theme_colors["navigation_fg"],
            ),
        )
    # Create month grid (3x4) in the year view window
    month_grid_frame = tk.Frame(
        calendar_instance, bg=calendar_instance.theme_colors["background"]
    )
    month_grid_frame.pack(fill="both", expand=True, padx=2, pady=2)
    # Configure grid weights
    for i in range(4):
        month_grid_frame.columnconfigure(i, weight=1)
    for i in range(3):
        month_grid_frame.rowconfigure(i, weight=1)
    # Create month buttons
    calendar_instance.year_view_labels = []
    for month in range(1, 13):
        row = (month - 1) // 4
        col = (month - 1) % 4
        month_name = _get_month_name(calendar_instance, month, short=True)
        month_label = tk.Label(
            month_grid_frame,
            text=month_name,
            font=(
                calendar_instance._get_scaled_font(  # pylint: disable=W0212
                    ("TkDefaultFont", 10, "bold")
                )
            ),
            relief="flat",
            bd=1,
            bg=calendar_instance.theme_colors["day_bg"],
            fg=calendar_instance.theme_colors["day_fg"],
            cursor="hand2",
        )
        month_label.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        # Highlight current month
        if month == calendar_instance.month:
            month_label.config(
                bg=calendar_instance.theme_colors["selected_bg"],
                fg=calendar_instance.theme_colors["selected_fg"],
            )
        # Bind click events
        month_label.bind(
            "<Button-1>",
            lambda e, m=month: (
                calendar_instance._on_year_view_month_click(m)  # pylint: disable=W0212
            ),
        )
        month_label.bind(
            "<Enter>",
            lambda e, label=month_label: _on_year_view_mouse_enter(
                calendar_instance, label
            ),
        )
        month_label.bind(
            "<Leave>",
            lambda e, label=month_label: _on_year_view_mouse_leave(
                calendar_instance, label
            ),
        )
        calendar_instance.year_view_labels.append((month, month_label))


def _on_year_view_mouse_enter(calendar_instance, label):
    """Handle mouse enter event in year view."""
    current_bg = label.cget("bg")
    if current_bg != calendar_instance.theme_colors["selected_bg"]:
        label.config(
            bg=calendar_instance.theme_colors["hover_bg"],
            fg=calendar_instance.theme_colors["hover_fg"],
        )


def _on_year_view_mouse_leave(calendar_instance, label):
    """Handle mouse leave event in year view."""
    current_bg = label.cget("bg")
    if current_bg == calendar_instance.theme_colors["hover_bg"]:
        # Check if this is the current month
        for month, month_label in calendar_instance.year_view_labels:
            if month_label == label:
                if month == calendar_instance.month:
                    label.config(
                        bg=calendar_instance.theme_colors["selected_bg"],
                        fg=calendar_instance.theme_colors["selected_fg"],
                    )
                else:
                    label.config(
                        bg=calendar_instance.theme_colors["day_bg"],
                        fg=calendar_instance.theme_colors["day_fg"],
                    )
                break


def _update_year_view(calendar_instance):  # pylint: disable=W0212
    """Update year view display."""
    if hasattr(calendar_instance, "year_view_year_label"):
        calendar_instance.year_view_year_label.config(text=str(calendar_instance.year))
    # Update month labels
    for month, label in calendar_instance.year_view_labels:
        # Reset to default colors
        label.config(
            bg=calendar_instance.theme_colors["day_bg"],
            fg=calendar_instance.theme_colors["day_fg"],
        )
        # Highlight current month
        if month == calendar_instance.month:
            label.config(
                bg=calendar_instance.theme_colors["selected_bg"],
                fg=calendar_instance.theme_colors["selected_fg"],
            )


def _recreate_widgets(calendar_instance):  # pylint: disable=W0212
    """Recreate all widgets while preserving current settings."""
    # Store current settings
    current_day_colors = calendar_instance.day_colors.copy()
    current_holidays = calendar_instance.holidays.copy()
    current_show_week_numbers = calendar_instance.show_week_numbers
    current_year_view_mode = calendar_instance.year_view_mode
    # Destroy all existing widgets completely
    if hasattr(calendar_instance, "canvas"):
        calendar_instance.canvas.destroy()
    if hasattr(calendar_instance, "scrollbar"):
        calendar_instance.scrollbar.destroy()
    if hasattr(calendar_instance, "year_container"):
        calendar_instance.year_container.destroy()
    # Clear all lists
    calendar_instance.month_frames.clear()
    calendar_instance.day_labels.clear()
    calendar_instance.week_labels.clear()
    calendar_instance.original_colors.clear()
    calendar_instance.year_view_labels.clear()
    # Restore settings
    calendar_instance.day_colors = current_day_colors
    calendar_instance.holidays = current_holidays
    calendar_instance.show_week_numbers = current_show_week_numbers
    calendar_instance.year_view_mode = current_year_view_mode
    # Recreate everything
    if calendar_instance.year_view_mode:
        _create_year_view_content(calendar_instance)
    else:
        _create_widgets(calendar_instance)
        _update_display(calendar_instance)
    # Update DPI scaling after recreation
    try:
        calendar_instance.update_dpi_scaling()
    except (OSError, ValueError, AttributeError) as e:
        calendar_instance.logger.debug(
            "Failed to update DPI scaling during recreation: %s", e
        )
