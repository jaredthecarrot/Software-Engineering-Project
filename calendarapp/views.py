from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from swingtime import models as swingtime

# Display user calendar
def user_calendar(request):
    events = swingtime.Event.objects.all()  # Get all events for display
    return render(request, 'user_calendar.html', {'events': events})

# Delete event occurrence
def delete_event(request, occurrence_id):
    occurrence = get_object_or_404(swingtime.Occurrence, id=occurrence_id)

    if request.method == 'POST':
        # Delete the occurrence
        occurrence.delete()
        return redirect('user_calendar')  # Redirect back to the calendar view
    
    return render(request, 'confirm_delete.html', {'occurrence': occurrence})

# Create a new event
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        event_type_label = request.POST.get('event_type', 'General')  # Use "General" as a fallback
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        count = int(request.POST.get('count', 1))

        if not title or not start_time or not end_time:
            # Validate that required fields are not empty
            return render(request, 'create_event.html', {
                'error': 'Please fill in all required fields.',
                'title': title,
                'description': description,
                'event_type': event_type_label,
                'start_time': start_time,
                'end_time': end_time,
                'count': count
            })

        # Create EventType if it doesn't exist
        event_type, _ = swingtime.EventType.objects.get_or_create(
            abbr=event_type_label.lower(),
            label=event_type_label
        )

        # Create the Event
        event = swingtime.Event.objects.create(
            title=title,
            description=description,
            event_type=event_type
        )

        # Add occurrences
        event.add_occurrences(
            datetime.fromisoformat(start_time),
            datetime.fromisoformat(end_time),
            count=count
        )

        return redirect('user_calendar')

    return render(request, 'create_event.html')
