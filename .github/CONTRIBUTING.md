# Contributing

Thanks for helping improve Social Content Monitor Skills.

## Good contributions

- fixes for media download, extraction, or transcription
- safer and more reliable platform adapter guidance
- support for another authorized Lark integration or Agent client
- tests and reproducible examples
- documentation fixes based on a real installation problem

Do not submit CAPTCHA bypasses, fingerprint spoofing, private APIs, proxy rotation, cookie export, automated social interactions, or examples containing personal information.

## Before opening a pull request

1. Open or reference an Issue for changes that affect behavior or safety.
2. Keep each pull request focused on one problem.
3. Preserve the two-Skill separation unless the change has a clear architectural reason.
4. Keep user configuration and runtime state outside the Skill folders.
5. Update documentation when commands, dependencies, fields, or behavior change.
6. Run the validation commands below.

```bash
python3 scripts/validate_repository.py
python3 skills/social-content-monitor-to-lark/scripts/validate_config.py skills/social-content-monitor-to-lark/assets/config.example.json
python3 -m py_compile skills/video-audio-transcribe/scripts/*.py skills/social-content-monitor-to-lark/scripts/*.py
```

The repository validator uses only the Python standard library. It checks both Skill directories, their frontmatter, and the OpenAI client metadata files.

## Platform adapters

New platform guidance must identify the stable creator ID, creator-owned content surface, stable content ID, canonical URL, pinned-content rule, and authorized media-access policy. Test one normal item, one pinned item, and one unrelated recommended item before proposing scheduled use.

## Pull request notes

Describe what changed, why it is needed, how it was tested, and whether it affects authentication, files, network access, Lark data, or scheduling.
