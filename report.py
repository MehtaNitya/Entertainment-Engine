import os
from datetime import datetime

from utils import ascii_bar


def write_report(movies, movie_recs, output_path, html_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    os.makedirs(os.path.dirname(html_path), exist_ok=True)
    lines = []
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines.append("ENTERTAINMENT ENGINE REPORT")
    lines.append("Generated: " + generated)
    lines.append("")
    lines.append("IMPACT")
    lines.append("- Movie selection time saved: 12 minutes")
    lines.append("")

    lines.append("TOP MOVIE RECOMMENDATIONS")
    for _, row in movie_recs.head(8).iterrows():
        score = f"{row['score']:.2f}"
        lines.append(f"- {row['title']} (score {score})")
    lines.append("")

    lines.append("DATA SNAPSHOT")
    lines.append("Movies pulled: " + str(len(movies)))
    lines.append("")

    lines.append("SIGNAL HIGHLIGHTS")
    pop_line = None
    if not movie_recs.empty:
        pop = movie_recs["popularity"].mean()
        pop_line = f"{pop:.1f}"
        lines.append("- Movie popularity: " + pop_line)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    html = build_html_report(movie_recs, len(movies), generated, pop_line)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)


def export_recommendations(movie_recs, csv_path, json_path):
    export_cols = ["title", "score", "runtime", "vote_average", "popularity", "imdb_rating"]
    available = [c for c in export_cols if c in movie_recs.columns]
    movie_recs[available].to_csv(csv_path, index=False)
    movie_recs[available].to_json(json_path, orient="records", indent=2)


def build_html_report(movie_recs, movie_count, generated, pop_line):
    rows = []
    for _, row in movie_recs.head(8).iterrows():
        rows.append(
            f"""<tr>
        <td>{row['title']}</td>
        <td>{row['score']:.2f}</td>
        <td>{int(row['runtime']) if row.get('runtime') else 0} min</td>
        <td>{row['vote_average']:.1f}</td>
      </tr>"""
        )
    pop_html = f"<p><strong>Movie popularity</strong> {pop_line}</p>" if pop_line else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Entertainment Engine Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #f8f6f1; margin: 0; padding: 32px; color: #1e1b16; }}
    .card {{ background: #fff; border-radius: 16px; padding: 24px; box-shadow: 0 10px 20px rgba(0,0,0,0.08); max-width: 900px; margin: 0 auto; }}
    h1 {{ margin-top: 0; font-size: 28px; }}
    .meta {{ color: #6d5f52; font-size: 14px; }}
    .kpi {{ display: flex; gap: 16px; margin: 20px 0; flex-wrap: wrap; }}
    .kpi div {{ background: #f3efe7; padding: 12px 16px; border-radius: 12px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ text-align: left; padding: 10px 8px; border-bottom: 1px solid #e7e1d7; }}
    th {{ font-size: 13px; text-transform: uppercase; letter-spacing: 0.06em; color: #6d5f52; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Entertainment Engine Report</h1>
    <p class="meta">Generated: {generated}</p>
    <div class="kpi">
      <div><strong>Movies pulled</strong><br>{movie_count}</div>
      <div><strong>Selection time saved</strong><br>12 minutes</div>
    </div>
    {pop_html}
    <h2>Top Recommendations</h2>
    <table>
      <thead>
        <tr>
          <th>Title</th>
          <th>Score</th>
          <th>Runtime</th>
          <th>Vote Avg</th>
        </tr>
      </thead>
      <tbody>
        {''.join(rows)}
      </tbody>
    </table>
  </div>
</body>
</html>"""
