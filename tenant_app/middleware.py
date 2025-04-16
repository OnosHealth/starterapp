from django.utils.deprecation import MiddlewareMixin
from shared_app.models import SubTenant
import re

class SubTenantMiddleware(MiddlewareMixin):
    """
    This middleware extracts the subtenant from the URL path and sets it as a request attribute
    """
    def process_request(self, request):
        # Extract subtenant from URL path
        # Example: /api/members/ny or /api/members/ny/123
        pattern = r'/api/members/([a-zA-Z0-9_-]+)(?:/|$)'
        match = re.search(pattern, request.path)
        
        request.subtenant = None
        if match:
            subtenant_name = match.group(1)
            # Don't treat a numeric ID as a subtenant name (for direct member access)
            if not subtenant_name.isdigit():
                # Find the subtenant for the current client schema
                subtenants = SubTenant.objects.filter(name=subtenant_name)
                if subtenants.exists():
                    request.subtenant = subtenants.first()
        
        return None