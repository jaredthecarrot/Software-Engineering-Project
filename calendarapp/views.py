from django.shortcuts import render, redirect
from datetime import datetime
from swingtime import models as swingtime

# Display user calendar
def user_calendar(request):
    events = swingtime.Event.objects.all()  # Get all events for display
    return render(request, 'user_calendar.html', {'events': events})

# Create a new event
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        event_type_label = request.POST.get('event_type')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        count = int(request.POST.get('count', 1))

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
