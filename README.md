# suave_rebetmc

## Docker

To build the img you need to create a github personal access token to read access to private repos, then log in to gh with gh cli

```Bash
gh auth login
```

```Bash
docker build --secret id=gh_token,src=<(gh auth token) -t suave-rebetmc:dev .
```