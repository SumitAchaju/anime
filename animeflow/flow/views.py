import requests
from django.http import HttpResponse
from django.shortcuts import render

from anime.models import Anime


def home_page(request):
    featured_animes = Anime.objects.order_by("-release_date")[:3]
    trending_animes = Anime.objects.order_by("-trending")[:6]
    popular_animes = Anime.objects.order_by("-popularity")[:6]
    recent_animes = Anime.objects.order_by("-created_at")[:6]
    action_animes = Anime.objects.filter(genres__title="Action").order_by("-release_date")[:6]
    top_views = Anime.objects.order_by("-views")[:6]

    context = {
        "featured_animes": featured_animes,
        "trending_animes": trending_animes,
        "popular_animes": popular_animes,
        "recent_animes": recent_animes,
        "action_animes": action_animes,
        "top_views": top_views,
    }

    return render(request, "index.html", context=context)


def proxy_file(request):
    url = request.GET.get("url")

    if not url:
        return HttpResponse(
            content="Missing URL parameter",
            status_code=400,
            content_type="text/plain",
            headers={"Access-Control-Allow-Origin": "*"}
        )
    try:
        # Fetch the .vtt file from the external URL
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return HttpResponse("Failed to fetch subtitle", status=502, content_type="text/plain")
    # Return the fetched content as a plain VTT file
    response = HttpResponse(
        content=resp.content,
        content_type="text/vtt"  # Important: tell browser it's a subtitle file
    )
    response["Content-Disposition"] = "inline"

    return response
