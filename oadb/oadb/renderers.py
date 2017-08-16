from rest_framework.renderers import AdminRenderer


class AdapterAdminRenderer(AdminRenderer):
    template = 'oadb/admin.html'

