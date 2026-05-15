# MongoDB Collections

## users
- email (unique), full_name, password_hash, role, language, theme
- bill_threshold, notifications_enabled, created_at

## energy_readings
- user_id, live (voltage, current, power_kw), daily/weekly/monthly kWh
- estimated_bill, carbon_kg, appliances[], recorded_at

## predictions
- user_id, horizon, points[], peak_load_kw, confidence, created_at

## recommendations
- user_id, items[], created_at

## alerts
- user_id, type, message, severity, read, created_at

## password_resets
- user_id, email, status, created_at
