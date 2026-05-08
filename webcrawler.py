"""
Reservation status checker for:
https://events.spieleautorenzunft.de/event/s2026

Polls the Alf.io public API every 10 minutes and prints a summary
of ticket categories with availability. Plays a sound and sends a
desktop notification if new slots open up.
"""

import time
import json
import datetime
import sys
import copy

try:
    import requests
except ImportError:
    print("Missing dependency: requests\n  pip install requests")
    sys.exit(1)

# ── Configuration ─────────────────────────────────────────────────────────────
print("init config")
EVENT_SHORT_NAME = "s2026"
BASE_URL         = "https://events.spieleautorenzunft.de"
API_URL          = f"{BASE_URL}/api/v2/public/event/{EVENT_SHORT_NAME}"
POLL_INTERVAL    = 600          # seconds (10 minutes)
NOTIFY           = True         # set False to disable desktop notifications
# ─────────────────────────────────────────────────────────────────────────────


def fetch_event_info() -> dict:
    """Fetch full event info from the Alf.io public API."""
    headers = {"Accept": "application/json"}
    resp = requests.get(API_URL, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()


def fetch_ticket_categories() -> list[dict]:
    """
    Alf.io exposes ticket categories (with availability) at
    /api/v2/public/event/<short-name>/ticket-categories
    Falls back to the top-level event payload if that endpoint 404s.
    """
    headers = {"Accept": "application/json"}
    cats_url = f"{API_URL}/ticket-categories"
    resp = requests.get(cats_url, headers=headers, timeout=15)

    if resp.status_code == 200:
        data = resp.json()
        # Alf.io returns {"ticketCategories": [...]} or just a list
        if isinstance(data, list):
            return data
        return data.get("ticketCategories", data.get("categories", []))

    # Fallback: some Alf.io versions embed categories in the event payload
    event = fetch_event_info()
    return event.get("ticketCategories", [])


def summarise(categories: list[dict]) -> dict[str, dict]:
    """Return a dict keyed by category name with availability info."""
    summary = {}
    for cat in categories:
        name      = cat.get("name", cat.get("description", "Unknown"))
        available = cat.get("availableTickets", cat.get("availability", {}).get("available", None))
        sold_out  = cat.get("soldOutOrLimitReached", False)
        expired   = cat.get("expired", False)

        summary[name] = {
            "available": available,
            "sold_out":  sold_out,
            "expired":   expired,
        }
    return summary


def play_kde_sound():
    """
    Play an alert sound on KDE Plasma / Arch Linux.
    Tries multiple methods in order of preference:
      1. paplay  (PipeWire/PulseAudio) with a KDE system sound
      2. pw-play (PipeWire native)
      3. aplay   (ALSA fallback)
      4. terminal bell (last resort)
    """
    import subprocess, os
 
    # Common KDE / freedesktop sound locations
    sound_candidates = [
        # KDE Plasma notification sound
        "/usr/share/sounds/freedesktop/stereo/message.oga",
        "/usr/share/sounds/freedesktop/stereo/bell.oga",
        "/usr/share/sounds/KDE-Im-Message-In.ogg",
        "/usr/share/sounds/KDE-Sys-Warning.ogg",
        # Generic ALSA wav fallback
        "/usr/share/sounds/alsa/Front_Right.wav",
    ]
 
    sound_file = next((f for f in sound_candidates if os.path.exists(f)), None)
 
    played = False
    if sound_file:
        for player in (["paplay", sound_file], ["pw-play", sound_file]):
            try:
                result = subprocess.run(player, timeout=5,
                                        capture_output=True, check=False)
                if result.returncode == 0:
                    played = True
                    break
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue
 
        # aplay only works for .wav
        if not played and sound_file.endswith(".wav"):
            try:
                subprocess.run(["aplay", "-q", sound_file],
                               timeout=5, check=False)
                played = True
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass
 
    # Play three rapid terminal bells as a fallback
    if not played:
        for _ in range(3):
            print("\a", end="", flush=True)
            time.sleep(0.25)


def desktop_notify(title: str, message: str):
    """
    Send an urgent, hard-to-miss KDE Plasma desktop notification
    via kdialog (pops up a dialog box) AND notify-send (notification centre).
    Also plays a sound.
    """
    import subprocess
 
    # 1. Play sound first so it fires even if the popup is slow
    while True: 
        play_kde_sound()
        time.sleep(1)
 
    # 2. notify-send with urgency=critical and a long timeout (0 = no expiry)
    #    -u critical makes KDE show it persistently and with a red/orange badge
    try:
        subprocess.run(
            [
                "notify-send",
                "--urgency=critical",
                "--expire-time=0",          # stays until dismissed
                "--icon=dialog-warning",
                "--app-name=ReservationChecker",
                "--hint=string:desktop-entry:dialog-warning",
                title,
                message,
            ],
            check=False,
        )
    except FileNotFoundError:
        pass  # notify-send not installed – kdialog below will still fire
 
    # 3. kdialog popup – this raises a real window that steals focus on KDE
    try:
        subprocess.Popen(
            ["kdialog", "--title", title, "--msgbox", message],
        )
    except FileNotFoundError:
        pass  # kdialog not installed (unlikely on KDE but handled gracefully)


def print_summary(summary: dict[str, dict], changed_names: list[str]):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #print(f"\n{'─'*55}")
    print(f"  Check at {now}")
    #print(f"{'─'*55}")
    for name, info in summary.items():
        status_parts = []
        if info["expired"]:
            status_parts.append("EXPIRED")
        elif info["sold_out"]:
            status_parts.append("SOLD OUT")
        else:
            avail = info["available"]
            if avail is None:
                status_parts.append("availability unknown")
            elif avail == 0:
                status_parts.append("SOLD OUT")
            else:
                status_parts.append(f" {avail} available")

        flag = "   CHANGED" if name in changed_names else ""
        print(f"  {name}: {', '.join(status_parts)}{flag}")
    #print(f"{'─'*55}")


def main():
    print(f"Monitoring: {BASE_URL}/event/{EVENT_SHORT_NAME}")
    print(f"Polling every {POLL_INTERVAL // 60} minutes. Press Ctrl+C to stop.\n")

    previous_summary: dict[str, dict] = {'Autoren/Designer Ticket': {'available': 0, 'sold_out': True, 'expired': False}, 'Publisher/Agency Ticket': {'available': 161, 'sold_out': False, 'expired': False}, 'Media Ticket': {'available': None, 'sold_out': False, 'expired': False}, 'Park Ticket': {'available': 10, 'sold_out': False, 'expired': False}}



    while True:
        try:
            categories = fetch_ticket_categories()

            if not categories:
                print(f"[{datetime.datetime.now():%H:%M:%S}] Warning: no categories returned.")
            else:
                #print(json.dumps(categories,sort_keys=True, indent=4))
                current_summary = summarise(categories)
                #current_summary = {'Autoren/Designer Ticket': {'available': 5, 'sold_out': False, 'expired': False}, 'Publisher/Agency Ticket': {'available': 161, 'sold_out': False, 'expired': False}, 'Media Ticket': {'available': None, 'sold_out': False, 'expired': False}, 'Park Ticket': {'available': 0, 'sold_out': True, 'expired': False}}

                changed_names   = []

                if previous_summary is not None:
                    for name, info in current_summary.items():
                        prev = previous_summary.get(name)
                        if prev is None:
                            changed_names.append(name)
                            continue
                        # Alert when a previously sold-out / unknown category gains availability
                        prev_avail = prev.get("available") or 0
                        curr_avail = info.get("available") or 0
                        if (prev["sold_out"] and not info["sold_out"]) or (curr_avail > prev_avail > 0):
                            print(name)
                            changed_names.append(name)
                #print(current_summary)
                print_summary(current_summary, changed_names)

                if changed_names and NOTIFY:
                    msg = "Slots opened: " + ", ".join(changed_names)
                    desktop_notify("Reservation Alert", msg)
                    # Also beep in the terminal
                    print("\a", end="", flush=True)

                previous_summary = copy.deepcopy(current_summary)

        except requests.exceptions.HTTPError as e:
            print(f"[{datetime.datetime.now():%H:%M:%S}] HTTP error: {e}")
        except requests.exceptions.ConnectionError:
            print(f"[{datetime.datetime.now():%H:%M:%S}] Connection error - will retry.")
        except Exception as e:
            print(f"[{datetime.datetime.now():%H:%M:%S}] Unexpected error: {e}")

        print(f"Next check in {POLL_INTERVAL // 60} min")
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    print("entering main")
    main()
