```bash
curl -L \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/repos/DimaKuprikhin/test-repository/contents
```

```bash
curl -L https://raw.githubusercontent.com/DimaKuprikhin/test-repository/master/main.cpp
```

```bash
curl -L \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    https://api.github.com/repos/gabime/spdlog/contents/
```

https://github.com/gabime/spdlog

```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/DimaKuprikhin/test-repository/zipball/3095bb03f38fe0500a9d94c4602f93d99e30bb5e" \
  --output ./repo.zip
```

```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/OWNER/REPO/git/ref/REF
```

```bash
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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"\
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/Dimakuprikhin/test-repositor
```
