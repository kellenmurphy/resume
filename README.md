# resume

LaTeX source for Kellen J. Murphy's resume.

## Building locally

Requires [Docker](https://docs.docker.com/get-docker/).

```bash
docker run --rm -v "$(pwd):/workdir" -w /workdir ghcr.io/xu-cheng/texlive-full pdflatex resume.tex
```

Output: `resume.pdf`

## CI

On every push to `main`, a GitHub Actions workflow:

1. Builds `resume.pdf` using the same Docker image as the local build
2. Uploads the PDF as a workflow artifact (Actions tab → latest run → **Artifacts**)
3. Pushes `resume.pdf` to [kellenmurphy.github.io](https://github.com/kellenmurphy/kellenmurphy.github.io)
