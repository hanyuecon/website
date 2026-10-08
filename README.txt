hanyuecon.com site files

index.html, research.html, media.html, teaching.html, cv.html   the five pages
style.css             shared styling for all pages
assets/Han_Yu_CV.pdf  your CV; replace this file to update it
assets/han-yu.jpg     your portrait; replace this file to change it

Upload everything in this folder to your GitHub repository.

Citation counts
citations.json               filled in automatically every Monday; do not edit
scripts/update_citations.py  fetches counts from your Google Scholar profile
.github/workflows/citations.yml  the weekly schedule
Requires a repository secret named SERPAPI_KEY (GitHub: Settings, Secrets and variables, Actions).
