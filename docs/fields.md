# MyAnimeList Data Fields

This document summarizes the commonly used data fields when collecting anime and manga metadata from the MyAnimeList API.

## General work information

| Field | Data type | Description |
| --- | --- | --- |
| id | Integer | Unique identifier of the anime or manga on MyAnimeList. |
| title | String | Official title of the work. |
| main_picture | Object | Main image, usually containing `medium` and `large`. |
| alternative_titles | Object | Alternative titles including Japanese, English, and synonyms. |
| start_date | Date | Release start date. |
| end_date | Date | Release end date. |
| synopsis | String | Brief description of the content. |
| mean | Decimal | Average score given by users. |
| rank | Integer | Ranking based on average score. |
| popularity | Integer | Ranking based on popularity. |
| num_list_users | Integer | Number of users who have the title in their list. |
| num_scoring_users | Integer | Number of users who have rated the title. |
| nsfw | String | Level of sensitive content. |
| media_type | String | Release format, e.g. `tv`, `movie`, `ova`, `manga`, `novel`. |
| status | String | Publishing status, e.g. `finished_airing`, `currently_airing`, `not_yet_aired`. |
| genres | List of objects | Main genres, such as Action, Comedy, Romance. |
| related_anime | List of objects | Related anime entries. |
| related_manga | List of objects | Related manga entries. |
| recommendations | List of objects | Recommended works for the user. |

## Anime-specific details

| Field | Description |
| --- | --- |
| num_episodes | Total number of episodes. |
| start_season | Season and year of broadcast, e.g. `summer 2023`. |
| broadcast | Broadcasting schedule information. |
| source | Origin of the work, e.g. manga, light novel, original. |
| average_episode_duration | Average duration of each episode, measured in seconds. |
| rating | Age rating of the title. |
| studios | Production studios. |
| statistics | User viewing and scoring statistics. |

## Manga-specific details

| Field | Description |
| --- | --- |
| num_chapters | Total number of chapters. |
| num_volumes | Total number of volumes or tankōbon. |
| authors | Authors or illustrators; can include `first_name` and `last_name`. |
| serialization | Original magazine or publication source. |

## Notes

- Source reference: MyAnimeList API.
- Data may differ between anime and manga depending on the work type.
- Some fields are objects or arrays of objects and may require additional handling during storage or mapping.