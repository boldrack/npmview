from .npmview import NpmView, NpmData, Npm404Exception

def request_metadata(package_slug: str):
    npmview_o = NpmView()
    return npmview_o.request_metadata(package_slug)
