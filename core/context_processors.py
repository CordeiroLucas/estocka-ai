from django.conf import settings

def project_version(request):
    """
    Retorna a versão do projeto para o contexto dos templates.
    """
    return {
        'APP_VERSION': settings.VERSION
    }