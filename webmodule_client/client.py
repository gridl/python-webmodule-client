from pyld import jsonld
import pystache
import request


class WebmoduleClient(object):
    """
    Top-level client that callers should instantiate first.

    Implemented as a class so as to use requests statefully and reuse TCP
    connections via its pool. Callers that choose to hang on to an instance
    of this class will automatically benefit from requests's connection pooling
    in this way.
    """

    def __init__(self):
        self.session = requests.Session()

    def get(self, url, options):
        """
        Fetch a URL known to repond with WebModule JSON(-LD).

        The options are passed to requests verbatim, so see requests docs for
        settings things like SSL options and headers.

        :param url: A URL to which an HTTP GET will be sent to get a WebModule
                    response.
        :param options: Dictionary-like object of keyword args to pass to
                        requests.
        :return:
        """
        r = self.session.get(url, **options)
        if r.ok:
            return Webmodule(r.json())
        else:
            raise Exception('Error {} fetching Webmodule {}: {} {}'
                            ''.format(r.status_code, url, r.text))


class Webmodule(object):
    def __init__(self, graph):
        self.graph = jsonld.frame(graph, {
            '@context': {
                '@vocab': 'http://www.bbc.co.uk/ontologies/webmodules/'
            },
            '@type': 'WebModule'
        })

    def render_templates(self):
        templates = {}
        for fragment_name in ['head', 'bodyFirst', 'bodyInline', 'bodyLast']:
            if fragment_name in self.graph:
                fragment = self.graph[fragment_name]
                if 'template' in fragment:
                    templates[fragment_name] = fragment['template']
                elif 'html' in fragment:
                    templates[fragment_name] = fragment['html']
        return templates

    def render_html(self, placeholders):
        htmls = {}
        for fragment_name in ['head', 'bodyFirst', 'bodyInline', 'bodyLast']:
            if fragment_name in self.graph:
                htmls[fragment_name] = pystache.render(
                        self.renderTemplates()[fragment_name], placeholders)

        return htmls
