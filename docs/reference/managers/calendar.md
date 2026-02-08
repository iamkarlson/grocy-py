# Calendar Manager

Access Grocy's calendar in iCalendar format.

Access via `grocy.calendar`.

```python
# Get iCal data
ical = grocy.calendar.ical()
print(ical)

# Get a sharing link
link = grocy.calendar.sharing_link()
print(f"Share: {link}")
```

## Class Reference

::: grocy.managers.calendar.CalendarManager
    options:
      members_order: source
      show_source: false
