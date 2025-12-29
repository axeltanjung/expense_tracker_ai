from analytics.forecast import run_all_users
from analytics.behavior import run_behavior_scan
from analytics.dopamine import run_dopamine
from analytics.delayed import flag_if_impulse

print("Running Forecast Engine...")
run_all_users()

print("Running Behavior Engine...")
run_behavior_scan()

print("Running Dopamine Engine...")
run_dopamine()

print("All AI engines finished.")
