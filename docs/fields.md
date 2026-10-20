# MyAnimeList Data Fields

This document summarizes the commonly used fields and nested subfields when collecting anime and manga metadata from the MyAnimeList API.

## Overview

The dataset includes shared fields used by both anime and manga, as well as additional fields specific to each type. Some values are plain scalars, while others are nested objects or arrays that may require normalization during storage or mapping.

## General work information

| Field | Data type | Description |
| --- | --- | --- |
| `id` | Integer | Unique identifier of the anime or manga on MyAnimeList. |
| `title` | String | Official title of the work. |
| `main_picture` | Object | Main image metadata, commonly containing `medium` and `large` URLs. |
| `alternative_titles` | Object | Alternative titles including Japanese, English, and synonyms. |
| `start_date` | Date | Release start date. |
| `end_date` | Date | Release end date. |
| `synopsis` | String | Brief description of the content. |
| `mean` | Decimal | Average score given by users. |
| `rank` | Integer | Ranking based on average score. |
| `popularity` | Integer | Ranking based on popularity. |
| `num_list_users` | Integer | Number of users who have added the title to their list. |
| `num_scoring_users` | Integer | Number of users who have rated the title. |
| `nsfw` | String | Content sensitivity level. |
| `media_type` | String | Release format such as `tv`, `movie`, `ova`, `manga`, or `novel`. |
| `status` | String | Publishing status such as `finished_airing`, `currently_airing`, or `not_yet_aired`. |
| `genres` | List of objects | Main genres, such as Action, Comedy, or Romance. |
| `related_anime` | List of objects | Related anime entries. |
| `related_manga` | List of objects | Related manga entries. |
| `recommendations` | List of objects | Recommended works for the user. |

## Anime-specific details

| Field | Data type | Description |
| --- | --- | --- |
| `num_episodes` | Integer | Total number of episodes. |
| `start_season` | String/Object | Season and year of broadcast, for example `summer 2023`. |
| `broadcast` | Object | Broadcasting schedule details. |
| `source` | String | Origin of the work, such as manga, light novel, or original content. |
| `average_episode_duration` | Integer | Average episode duration measured in seconds. |
| `rating` | String | Age rating of the title. |
| `studios` | List of objects | Production studios associated with the work. |
| `statistics` | Object | User viewing and scoring statistics. |

## Manga-specific details

| Field | Data type | Description |
| --- | --- | --- |
| `num_chapters` | Integer | Total number of chapters. |
| `num_volumes` | Integer | Total number of volumes or tankōbon. |
| `authors` | List of objects | Authors or illustrators; each item may include `first_name` and `last_name`. |
| `serialization` | String/Object | Original magazine or publication source. |

## Common nested subfields

| Parent field | Subfields | Notes |
| --- | --- | --- |
| `main_picture` | `medium`, `large` | Main poster image in different sizes. |
| `pictures` | `medium`, `large` | Image gallery items; same structure as `main_picture`. |
| `alternative_titles` | `synonyms`, `en`, `ja` | Common aliases and localized names. |
| `genres` | `id`, `name` | Genre metadata. |
| `related_anime` | `node`, `relation_type`, `relation_type_formatted` | Related anime entries, where `node` contains nested work metadata. |
| `related_manga` | `node`, `relation_type`, `relation_type_formatted` | Related manga entries. |
| `recommendations` | `node`, `num_recommendations` | Recommended works returned by the API. |
| `node` | `id`, `title`, `main_picture`, `alternative_titles` | Reused structure in list endpoints and nested result objects. |
| `start_season` | `year`, `season` | Broadcast season and year. |
| `broadcast` | `day_of_week`, `start_time` | Programming schedule details. |
| `studios` | `id`, `name` | Production studio information. |
| `statistics` | `status`, `score` | Aggregated user watch and score statistics. |
| `authors` | `first_name`, `last_name` | Author names as returned by MAL. |
| `serialization` | `name` | Source publication or magazine. |
| `magazines` | `id`, `name` | Magazine or publication metadata. |

``Important``: The `id` subfield is always returned along with its parent field, even if you have explicitly declare it

## Notes

- Source reference: MyAnimeList API.
- Data can vary between anime and manga depending on the work type.
- Some fields are nested objects or arrays and may need custom handling during storage, normalization, and mapping.
- This document is intended as a practical field checklist, not a complete schema definition for every possible response.