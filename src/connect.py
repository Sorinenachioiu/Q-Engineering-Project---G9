import configparser
from quantuminspire.credentials import save_account
from quantuminspire.qiskit import QI
from qiskit_ibm_runtime import QiskitRuntimeService

def get_Q_Inspire_backend(verbose = False):
    config_file_path = './src/cfg/qi_settings.cfg'

    # Read the token from the configuration file
    try: 
        config = configparser.ConfigParser()
        config.read(config_file_path)
        token = config['Default']['token']
        backend_name = config['Default'].get('backend', 'QX single-node simulator')

        # Save the token persistently
        save_account(token)
        if verbose:
            print("Token saved successfully!")

        # Set authentication
        QI.set_authentication()
    except KeyError as e:
        print(f"Missing required field in configuration file: {e}")
    except Exception as e:
        print(f"Error: {e}")

    # Get the desired backend
    try:
        # Get all available backends
        backends = QI.backends()
        if verbose:
            print("Available backends:", backends)

        # Find the desired backend by name
        backend = None
        
        backend_dict = {b.name(): b for b in backends}
        backend = backend_dict.get(backend_name)

        if backend:
            print(f"Connected to backend: {backend}")
            return backend
        else:
            print(f"Backend '{backend_name}' is not available.")
    except Exception as e:
        print(f"Error: {e}")


def get_ibm_backend(verbose = False):
    # Path to the ibm_settings.cfg file
    config_file_path = './src/cfg/ibm_settings.cfg'

    # Read the configuration
    try: 
        config = configparser.ConfigParser()
        config.read(config_file_path)

        # Load API token and URL
        token = config['Default']['token']
        url = config['Default'].get('url', 'https://auth.quantum-computing.ibm.com/api')
        backend_name = config['Default'].get('backend', 'ibmq_qasm_simulator')      
    except KeyError as e:
        print(f"Missing required field in configuration file: {e}")
    except Exception as e:
        print(f"Error: {e}")

    try:

        QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)
        service = QiskitRuntimeService(channel="ibm_quantum")
        backend = service.least_busy(simulator=False, operational=True)
        print(f"Connected to backend: {backend}")
    except KeyError as e:
        print(f"Missing required field in configuration file: {e}")
    except Exception as e:
        print(f"Error: {e}")


def get_backend(backend_type , verbose = False):
    if backend_type == 'qi':
        return get_Q_Inspire_backend(verbose)
    elif backend_type == 'ibm':
        return get_ibm_backend(verbose)
    
    print("The backend type {backend_type} does not exist.")
    
