from connect import get_backend

# set as "ibm" to use ibm backend
# backend_type = "ibm"
backend_type = "qi"

backend = get_backend(backend_type, True)