from src.reminder_agent import ReminderAgent

agent = ReminderAgent()

result = agent.process_reminder(
    "Remind me to submit my assignment tomorrow at 9 PM",
    reference_datetime="2026-11-14T18:30:00+05:30"
)

print("AI Reminder Result:")
print(result)