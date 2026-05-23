# MongoDB Collections

## users
| Field | Type | Description |
|-------|------|-------------|
| email | string | Unique login |
| password_hash | string | bcrypt hash |
| full_name | string | Display name |
| role | string | `user` \| `admin` |
| preferred_language | string | en, kn, hi, ta, te |
| theme | string | dark \| light |
| created_at | datetime | Registration time |

## energy_readings
Stored snapshots from simulation or IoT.

## predictions
Optional cache for ML outputs.

## alerts
User alerts (high usage, bill threshold, spikes).

## iot_readings
ESP32 / SCT-013 payloads when hardware is connected.

## password_resets
Forgot-password audit trail (demo).
