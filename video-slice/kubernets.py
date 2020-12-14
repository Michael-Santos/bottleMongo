from kubernetes import client, config
from bottle import run, template, get, post, request, install, response

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.AppsV1Api()
#v1.patch_namespaced_deployment_scale("nginx-deployment", "default", "4")

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


@post('/num_replicas/<num_replicas>')
def index(num_replicas):
    print(num_replicas)
    return "sucesso"

install(EnableCors())
run(host='localhost', port=8082)
    