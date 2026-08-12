# Lark Base schema and writes

## Contents

1. Recommended fields
2. Schema resolution
3. Deduplication
4. Two-phase writes
5. Field values

## Recommended fields

| Logical key | Suggested field name | Type | Required |
|---|---|---|---|
| `unique_key` | 唯一键 | text | yes |
| `platform` | 平台 | text/select | yes |
| `content_id` | 内容ID | text | yes |
| `content_kind` | 内容类型 | text/select | yes |
| `title` | 标题 | text | yes |
| `published_at` | 发布日期 | datetime | yes |
| `canonical_url` | 链接 | URL/text | yes |
| `author_name` | 作者 | text | yes |
| `author_stable_id` | 作者ID | text | recommended |
| `likes` | 点赞 | number | optional |
| `comments` | 评论 | number | optional |
| `favorites` | 收藏 | number | optional |
| `shares` | 分享 | number | optional |
| `views` | 播放 | number | optional |
| `caption` | 原始文案 | multiline text | recommended |
| `tags` | 标签 | multiline text | optional |
| `transcript` | 口播文案 | multiline text | recommended |
| `transcription_status` | 转写状态 | text/select | recommended |
| `error_message` | 失败原因 | multiline text | recommended |
| `discovered_at` | 发现时间 | datetime | recommended |

Use `field_map` in the working config to map logical keys to the user's actual fields. Do not assume Chinese field names.

## Schema resolution

1. Resolve a Base or Wiki URL through `lark-base` and reuse the returned real `base_token` and table ID.
2. Read the table and field list before writing.
3. Confirm writable field types and existing select options.
4. Do not write formula, lookup, system, or attachment fields as ordinary values.
5. If required fields are missing, ask before creating or changing schema.

Use user identity by default. Route authentication and missing-scope recovery through `lark-shared`; do not silently switch identities.

## Deduplication

Search `unique_key=<platform>:<content_id>` before creating a row. For legacy rows without `unique_key`, search the normalized canonical URL once. If a match exists, reuse its `record_id` for recovery or transcript retries.

Do not use title, publication time, or author name as the primary key.

## Two-phase writes

Phase A creates one metadata record with `transcription_status=pending` and saves the returned `record_id`.

Phase B updates exactly that `record_id`:

- success: write transcript and set `completed`;
- no speech/media: set `not_applicable`;
- failure: keep metadata, set `failed`, and write a concise error message.

Use upsert only when its key semantics are explicit and guaranteed to target `unique_key`. Otherwise search then create/update serially.

## Field values

- Preserve numbers as numbers after safely expanding visible suffixes such as `万`; leave unreliable values empty.
- Store times with timezone-aware source data, converting to the user's requested display timezone.
- Join hashtags with spaces unless the destination is a true multi-select field.
- Preserve published caption and recognized speech in different fields.
- Never put cookies, access tokens, local media paths, or internal error traces into the Base.
