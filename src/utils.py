import pandas as pd

def format_vehicle_status(vehicle_id, route, arrival, predicted_turnaround):
    status = "✅" if predicted_turnaround <= 120 else "⚠️" if predicted_turnaround <= 180 else "🚨"
    return f"  {vehicle_id:10} {route:20} {arrival:10} {predicted_turnaround:>6} min  {status}"

def calculate_fleet_efficiency(predictions_df):
    avg_turnaround = predictions_df['predicted_turnaround'].mean()
    on_time = (predictions_df['predicted_turnaround'] <= 120).sum()
    total = len(predictions_df)
    efficiency = (on_time / total) * 100
    
    return {
        'average_turnaround': round(avg_turnaround, 1),
        'on_time_count': on_time,
        'total_vehicles': total,
        'efficiency_percent': round(efficiency, 1)
    }

def generate_daily_report(predictions_df):
    stats = calculate_fleet_efficiency(predictions_df)
    
    report = f"""
═══════════════════════════════════════════════════════════════════
   LOGISTICS TURNAROUND — DAILY FORECAST REPORT
═══════════════════════════════════════════════════════════════════

  📅 Date: {pd.Timestamp.now().strftime('%Y-%m-%d')}
  🚛 Fleet Size: {stats['total_vehicles']} vehicles

───────────────────────────────────────────────────────────────────
  SUMMARY
───────────────────────────────────────────────────────────────────

  Average Turnaround:     {stats['average_turnaround']} min
  On-Time Vehicles:       {stats['on_time_count']}/{stats['total_vehicles']} ({stats['efficiency_percent']}%)
  Delayed Vehicles:       {stats['total_vehicles'] - stats['on_time_count']}/{stats['total_vehicles']} ({100 - stats['efficiency_percent']}%)

═══════════════════════════════════════════════════════════════════
"""
    return report
