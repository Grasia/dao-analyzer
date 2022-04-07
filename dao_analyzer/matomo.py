class Matomo:
    def __init__(self, matomo_url=None, site_id=None):
        self.matomo_url = matomo_url
        self.site_id = site_id

        if not matomo_url:
            raise ValueError("matomo_url has to be set")
        if type(site_id) != int:
            raise ValueError("site_id has to be an integer")

    def get_js(self) -> str:
        return f"""
            var _paq = window._paq = window._paq || [];
            /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
            _paq.push(['trackPageView']);
            _paq.push(['enableLinkTracking']);
            (function() {{
                var u="{self.matomo_url}";
                _paq.push(['setTrackerUrl', u+'matomo.php']);
                _paq.push(['setSiteId', '{self.site_id}']);
                var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
                g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
            }})();
            """

    def get_script(self) -> str:
        return f"""
            <!-- Matomo -->
            <script>
            {self.get_js()}
            </script>
            <!-- End Matomo Code -->
        """