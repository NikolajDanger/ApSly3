from typing import NamedTuple

from .Constants import EPISODES, CHALLENGES

class Sly3LocationData(NamedTuple):
  name: str
  code: int
  category: str

jobs_list = [
  (f"{ep} - {job}",       "Job")
  for ep, chapters in EPISODES.items()
  for jobs in chapters
  for job in jobs
]

purchases_list = [
  (f"ThiefNet {i+1:02}",  "Purchase")
  for i in range(37)
]

challenges_list = [
  (f"{ep} - {challenge} (MTC)", "Challenge")
  for ep, chapters in CHALLENGES.items()
  for challenges in chapters
  for challenge in challenges
]

location_list = jobs_list + purchases_list + challenges_list + [("All Bosses", "-")]

base_code = 8008135

location_dict = {
    name: Sly3LocationData(name, base_code+code, category)
    for code, (name, category) in enumerate(location_list)
}

location_groups = {
  key: {location.name for location in location_dict.values() if location.category == key}
  for key in [
    "Job",
    "Purchase",
    "Challenge"
  ]
}

location_groups.update({
  "Jobs":       location_groups["Job"],
  "Challenges": location_groups["Challenge"],
  "ThiefNet":   location_groups["Purchase"],
  "Operations": {n for n in location_groups["Job"] if "Operation:" in n},
})
for ep in EPISODES:
  location_groups[ep] = {
    loc.name for loc in location_dict.values()
    if loc.name.startswith(f"{ep} - ")
  }

def from_id(location_id: int) -> Sly3LocationData:
  matching = [location for location in location_dict.values() if location.code == location_id]
  if len(matching) == 0:
    raise ValueError(f"No location data for location id '{location_id}'")
  assert len(matching) < 2, f"Multiple locations data with id '{location_id}'. Please report."
  return matching[0]
