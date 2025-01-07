# Explanation
In here you need to add two config (.cfg) files, with your own token. The token can be obtained by going to your own account on the respective website.


One for connecting to the ibm backend and one for connecting to the quantum inspire one.

## Files format

The file for the IBM backend should look like this ( with name ibm_settings.cfg):
```
[Default]
token = "!YOUR_IBM_TOKEN!"
url = https://auth.quantum-computing.ibm.com/api
backend = ibmq_qasm_simulator
```


The file for the QI backend should look like this ( with name qi_settings.cfg):
```
[Default]
token = "!YOUR_QI_TOKEN!"   
backend_name = QX single-node simulator
```