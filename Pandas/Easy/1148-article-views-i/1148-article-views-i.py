import pandas as pd

def article_views(views: pd.DataFrame) -> pd.DataFrame:

    avoa = views[views['author_id'] == views['viewer_id']]
    ua = avoa["author_id"].unique()
    return pd.DataFrame({"id" : sorted(ua) })

    