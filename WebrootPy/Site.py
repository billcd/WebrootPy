from .Tools import to_webroot_json, webroot_json_to_properties


class Site:
    site_id = None
    site_name = None
    seats = None
    comments = None
    billing_cycle = None
    billing_date = None
    global_policies = None
    global_overrides = None
    policy_id = None
    emails = None
    trial = None
    modules = []
    raw = None
    account_key_code = None
    total_endpoints = None

    def __init__(self, site_id=None, json_data=None):
        self.site_id = site_id

        if json_data:
            self.raw = json_data
            webroot_json_to_properties(self, json_data)

    def __str__(self):
        return to_webroot_json(self)

