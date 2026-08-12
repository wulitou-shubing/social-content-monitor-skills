# Platform adapter contract

## Contents

1. Adapter output
2. Candidate verification
3. Platform-specific guidance
4. Adding another platform

## Adapter output

Every platform adapter must normalize a creator and candidate into this logical shape before storage:

```json
{
  "platform": "douyin",
  "content_id": "stable-platform-id",
  "canonical_url": "https://platform.example/content/stable-platform-id",
  "content_kind": "video",
  "author_name": "Creator display name",
  "author_stable_id": "stable-account-id",
  "title": "Short display title",
  "caption": "Full published caption",
  "tags": ["#topic"],
  "published_at": "2026-01-02T15:04:05+08:00",
  "metrics": {
    "likes": null,
    "comments": null,
    "favorites": null,
    "shares": null,
    "views": null
  },
  "is_pinned": false,
  "has_transcribable_media": true
}
```

Use `null` for values that are unavailable or unreliable. Never infer engagement counts.

Generate `title` from the platform's explicit title when present. Otherwise use the first suitable short sentence from `caption`; retain the full caption separately.

## Candidate verification

Accept a candidate only when all of these are true:

1. It came from the target profile's creator-owned content list/tab, not search, recommendations, related content, collections from other creators, or comments.
2. It is not marked pinned unless the user explicitly monitors pinned changes.
3. The detail page's author name is compatible with the configured account name.
4. The detail page's stable author ID or canonical profile link exactly matches the configured stable account identity.
5. The canonical content URL and content ID belong to the same item.

If stable author identity cannot be verified, discard the candidate and request manual review. Do not relax verification to fill a quota.

## Platform-specific guidance

### Douyin

- Use the profile's “作品” area.
- Normalize detail links to `https://www.douyin.com/video/<aweme_id>` when available.
- Treat `sec_user_id` as the preferred stable account identity.
- Exclude recommendation rails, search results, and collection recommendations.
- Authenticated downloading may require user-approved browser cookies; browsing alone does not grant permission to export cookies.

### Xiaohongshu

- Use the creator profile's note/work grid.
- Normalize notes to the stable note ID and canonical note URL.
- Verify the detail author's profile link or stable user ID against the configured creator.
- Notes may be image, text, video, or mixed media. Only send video/audio with audible speech to transcription.
- Store the note title and full description separately when both exist.

### TikTok

- Use the creator's own video grid and stable username/account identifier.
- Normalize to the canonical video URL and platform video ID.
- Do not confuse suggested videos with creator-owned content.

### YouTube

- Prefer an official connector/API or channel feed when available.
- Distinguish videos, Shorts, live streams, and community posts.
- Use channel ID and video ID as stable identities.

## Adding another platform

Document these five decisions before enabling a new adapter:

1. Canonical profile URL and stable author ID.
2. Creator-owned content surface.
3. Stable content ID and canonical content URL.
4. Pinned/sponsored/reposted content rules.
5. Media download and authentication policy.

Test the adapter manually on at least one normal item, one pinned item, and one unrelated recommended item before scheduling it.
